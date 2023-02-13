#!/usr/bin/python3

from datetime import datetime
import os
import sys
from subprocess import PIPE, run
import json
from fnmatch import fnmatch
from scripts.verify_cocotb.RunTest import RunTest
from scripts.verify_cocotb.Test import Test
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import socket
import yaml

class RunRegression: 
    def __init__(self,args,paths) -> None:
        self.args  = args
        self.paths = paths
        self.total_start_time = datetime.now()
        self.write_command_log()
        self.write_git_log()
        with open(f'{self.paths.COCOTB_PATH}/tests.json') as f:
            self.tests_json = json.load(f)
            self.tests_json = self.tests_json["Tests"]
        self.set_common_macros()
        self.get_tests()
        self.run_regression()
        self.send_mail()

    def set_common_macros(self):
        if self.args.macros is None:
            self.args.macros =list()
        simulation_macros = ["USE_POWER_PINS","UNIT_DELAY=#1","COCOTB_SIM"]
        paths_macros      = [f'MAIN_PATH=\\\"{self.paths.COCOTB_PATH}\\\"',f'TAG=\\\"{self.args.tag}\\\"',f'CARAVEL_ROOT=\\\"{os.getenv("CARAVEL_ROOT")}\\\"']
        if self.args.pdk is not "gf180":
            simulation_macros.append("FUNCTIONAL")

        if self.args.caravan:
            simulation_macros.append(f'CARAVAN') 

        if not self.args.no_wave:
            simulation_macros.append(f'WAVE_GEN')

        if self.args.sdf_setup:
            simulation_macros.append(f'MAX_SDF')

        if self.args.cov:
            simulation_macros.append(f'COVERAGE')
        if self.args.checkers_en:
            simulation_macros.append(f'CHECKERS')
            
        if self.args.iverilog:
            simulation_macros.append(f'IVERILOG')
        elif (self.args.vcs): 
            simulation_macros.append(f'VCS')

        simulation_macros.append(self.args.pdk)   
        if self.args.arm: 
            simulation_macros.extend(['ARM','AHB'])   

        self.args.macros += simulation_macros + paths_macros


    def get_tests(self):
        self.tests = list()
        self.passed_tests = 0
        self.failed_tests = 0
        # regression 
        if self.args.regression is not None:
            sim_types = ("RTL","GL","GL_SDF")
            for test,test_elements in self.tests_json.items():
                if fnmatch(test,"_*"): # skip comments
                        continue
                if self.args.pdk not in test_elements["PDK"]:
                        continue # test is not valid for this pdk
                for sim_type in sim_types:
                    if sim_type =="GL_SDF": 
                        if self.args.regression in test_elements[sim_type]: 
                            for corner in self.args.corner: 
                                self.add_new_test(test_name=test,sim_type = sim_type,corner = corner)
                    else: 
                        if self.args.regression in test_elements[sim_type]: 
                                self.add_new_test(test_name=test,sim_type = sim_type,corner = "-")
            if (len(self.tests)==0):
                print(f"fatal:{self.args.regression} is not a valid regression name please input a valid regression \ncheck tests.json for more info")
                sys.exit()
        #test
        if self.args.test is not None:
            if isinstance(self.args.test,list):
                for test in self.args.test:
                    if isinstance(self.args.sim,list):
                        for sim_type in self.args.sim:
                            if sim_type =="GL_SDF": 
                                for corner in self.corners: 
                                    self.add_new_test(test_name=test,sim_type = sim_type, corner = corner)
                            else: self.add_new_test(test_name=test,sim_type = sim_type,corner = self.args.corner[0])
                    else:
                        if sim_type =="GL_SDF": 
                            for corner in self.corners: 
                                self.add_new_test(test_name=test,sim_type = sim_type, corner = corner)
                        else: self.add_new_test(test_name=test,sim_type = sim_type,corner = self.args.corner[0])

            else:
                if self.args.test in self.tests_json:
                    if isinstance(self.args.sim,list):
                        for sim_type in self.args.sim:
                            self.add_new_test(test_name=self.args.test,sim_type = sim_type,corner = self.args.corner[0])
                    else:
                        self.add_new_test(test_name=self.args.test,sim_type = self.args.sim,corner = self.args.corner[0])
        if self.args.testlist is not None:
            for testlist in self.args.testlist:
                self.get_testlist(testlist)

        self.update_run_log()
        # exit()

    def add_new_test(self,test_name,sim_type,corner):
        self.tests.append(Test(test_name,sim_type,corner,self.args,self.paths))

    def get_testlist(self,testlist_f): 
        directory = os.path.dirname(testlist_f)
        testlist_f = open(testlist_f, 'r')
        testlist = yaml.safe_load(testlist_f)
        if "includes" in testlist: 
            for include in testlist["includes"]:
                if directory == '':
                    self.get_testlist(f"{include}")
                else:
                    self.get_testlist(f"{directory}/{include}")
        for test in testlist["Tests"]:
            data = {'test_name':test["name"],'sim_type' :"RTL",'corner':self.args.corner[0]}
            if "sim" in test: 
                data['sim_type'] = test["sim"]
            if "corner" in test: 
                data["corner"] = test["corner"]
            self.add_new_test(**data)

    def run_regression(self):
        threads = list()
        for test in self.tests:
                    if self.args.iverilog: #threading
                        # x = threading.Thread(target=self.test_run_function,args=(test,sim_type,corner))
                        # threads.append(x)
                        # x.start()
                        # time.sleep(10)
                        self.test_run_function(test)
                    else: 
                        self.test_run_function(test)
        # for index, thread in enumerate(threads):
        #     thread.join()

        if self.args.cov:
            if self.args.vcs:
                self.generate_cov()
            #merge functional coverage
            merge_fun_cov_command = f"docker run -it -u $(id -u $USER):$(id -g $USER) -v {self.cocotb_path}:{self.cocotb_path}  efabless/dv:cocotb sh -c 'cd {self.cocotb_path} && python3 scripts/merge_coverage.py -p {self.cocotb_path}/sim/{self.args.tag}'"
            self.full_terminal = open(f"{self.cocotb_path}/sim/{self.args.tag}/command.log", "a")
            self.full_terminal.write(f"\n\ndocker command for merge functional coverage:\n% ")
            self.full_terminal.write(os.path.expandvars(merge_fun_cov_command)+"\n")
            self.full_terminal.close()
            os.system(merge_fun_cov_command)
                
    def test_run_function(self,test):
        self.update_run_log()
        RunTest(self.args,self.paths,test)
        self.update_run_log()


    def generate_cov(self):
        os.chdir(f"{self.cocotb_path}/sim/{self.args.tag}")
        os.system(f"urg -dir RTL*/*.vdb -format both -show tests -report coverageRTL/")
        # os.system(f"urg -dir GL*/*.vdb -format both -show tests -report coverageGL/")
        # os.system(f"urg -dir SDF*/*.vdb -format both -show tests -report coverageSDF/")
        os.chdir(self.cocotb_path)

    def update_run_log(self):
        file_name=f"sim/{self.args.tag}/runs.log"
        f = open(file_name, "w")
        name_size = self.tests[0].max_name_size
        f.write(f"{'Test':<{name_size}} {'status':<10} {'start':<15} {'end':<15} {'duration':<13} {'p/f':<8} {'seed':<10} \n")
        for test in self.tests:
            f.write(f"{test.full_name:<{name_size}} {test.status:<10} {test.start_time:<15} {test.endtime:<15} {test.duration:<13} {test.passed:<8} {test.seed:<10}\n")
        f.write(f"\n\nTotal: ({test.passed_count})passed ({test.failed_count})failed ({test.unknown_count})unknown  ({('%.10s' % (datetime.now() - self.total_start_time))})time consumed ")
        f.close()

    def write_command_log(self):
        file_name=f"sim/{self.args.tag}/command.log"
        f = open(file_name, "w")
        f.write(f"command used to run this sim:\n% ")
        f.write(f"{' '.join(sys.argv)}")
        f.close()
  
    def write_git_log(self):
        file_name=f"sim/{self.args.tag}/repos_info.log"
        f = open(file_name, "w")
        f.write( f"{'#'*4} Caravel repo info {'#'*4}\n")
        f.write( f"Repo: {run(f'cd {self.paths.CARAVEL_ROOT};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( f"Branch name: {run(f'cd {self.paths.CARAVEL_ROOT};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( run(f'cd {self.paths.CARAVEL_ROOT};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)

        f.write( f"\n\n{'#'*4} Caravel Managment repo info {'#'*4}\n")
        f.write( f"Repo: {run(f'cd {self.paths.MCW_ROOT};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( f"Branch name: {run(f'cd {self.paths.MCW_ROOT};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( run(f'cd {self.paths.MCW_ROOT};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)

        if self.args.user_test: 
            f.write( f"\n\n{'#'*4} User repo info {'#'*4}\n")
            f.write( f"Repo: {run(f'cd {self.paths.USER_PROJECT_ROOT};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
            f.write( f"Branch name: {run(f'cd {self.paths.USER_PROJECT_ROOT};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
            f.write( run(f'cd {self.paths.USER_PROJECT_ROOT};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)

        f.write( f"\n\n{'#'*4} caravel-dynamic-sims repo info {'#'*4}\n")
        f.write( f"Repo: {run(f'cd {self.paths.COCOTB_PATH};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( f"Branch name: {run(f'cd {self.paths.COCOTB_PATH};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( run(f'cd {self.paths.COCOTB_PATH};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)
        f.close()

    def send_mail(self):
        if self.args.emailto is None: 
            return
        #get commits 
        showlog = f"{self.paths.COCOTB_PATH}/sim/{self.args.tag}/repos_info.log"
        with open(showlog, 'rb') as fp:
            first_commit = True
            for line in fp:
                if fnmatch(str(line,"utf-8"),"commit*"):
                    for word in line.split():
                        if first_commit:
                            caravel_commit = str(word,"utf-8")
                        else: 
                            mgmt_commit = str(word,"utf-8")
                    first_commit = False


        tag = f"{self.paths.COCOTB_PATH}/sim/{self.args.tag}"
        mail_sub = ("<html><head><style>table {border-collapse: collapse;width: 50%;} th, td {text-align: left;padding: 8px;} tr:nth-child(even) {background-color: #D6EEEE;}"
                    f"</style></head><body><h2>Run info:</h2> <table border=2 bgcolor=#D6EEEE> "
                    f"<th>location</th> <th><strong>{socket.gethostname()}</strong>:{tag}</th> <tr>  "
                    f"<th> caravel commit</th> <th><a href='https://github.com/efabless/caravel/commit/{caravel_commit}'>{caravel_commit}<a></th> <tr>  " 
                    f"<th>caravel_mgmt_soc_litex commit</th> <th><a href='https://github.com/efabless/caravel_mgmt_soc_litex/commit/{mgmt_commit}'>{mgmt_commit}<a></th> <tr> </table> ") 
        mail_sub += self.set_html_test_table()
        mail_sub += f"<p>best regards, </p></body></html>"
        # print(mail_sub)
        msg = MIMEMultipart("alternative", None, [ MIMEText(mail_sub,'html')])
        all_pass = (self.tests[0].failed_count == 0 and self.tests[0].unknown_count == 0)
        if all_pass:
            msg['Subject'] = f'Pass: {self.args.tag} run results'
        else: 
            msg['Subject'] = f'Fail: {self.args.tag} run results'
        msg['From'] = "verification@efabless.com"
        msg['To'] = ", ".join(self.args.emailto)
        docker = False
        if docker: 
            mail_command = f'echo "{mail_sub}" | mail -a "Content-type: text/html;" -s "{msg["Subject"]}" {self.args.emailto[0]}'
            docker_command = f"docker run -it -u $(id -u $USER):$(id -g $USER) efabless/dv:mail sh -c '{mail_command}'"
            print(docker_command)
            os.system(docker_command)
        else:
            # Send the message via our own SMTP server.
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()
    

    def set_html_test_table(self):
        html_test_table =f"<h2>Tests Table:</h2><table border=2 bgcolor=#D6EEEE>"
        html_test_table += f"<th>Test</th> <th>duration</th> <th>status</th> <th>seed</th> <tr> "
        for test in self.tests:
            if test.passed == "passed":
                html_test_table += f"<th>{test.full_name}</th><th>{test.duration}</th> <th style='background-color:#16EC0C'> {test.passed} </th><th>{test.seed}</th><tr>"
            else:
                html_test_table += f"<th>{test.full_name}</th><th>{test.duration}</th> <th style='background-color:#E50E0E'> {test.passed} </th><th>{test.seed}</th><tr>"
        html_test_table += "</table>"
        html_test_table += (f"<h2>Total status Table:</h2><table border=2 bgcolor=#D6EEEE><th>Passed</th> <th>failed</th> <th>unknown</th> <th>duration</th> <tr>"
                      f"<th style='background-color:#16EC0C' >{test.passed_count}</th> <th style='background-color:#E50E0E' >{test.failed_count} </th> "
                      f"<th style='background-color:#14E5F2'>{test.unknown_count}</th> <th>{('%.10s' % (datetime.now() - self.total_start_time))}</th> <tr></table>")
        return html_test_table