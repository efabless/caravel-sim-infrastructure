#!/usr/bin/python3

from datetime import datetime
import os
import sys
from subprocess import PIPE, run
import json
import collections
from fnmatch import fnmatch
from collections import namedtuple
from scripts.verify_cocotb.RunTest import RunTest

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
        self.get_tests()
        self.run_regression()

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
                    if test in self.tests_json:
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
        # testlist TODO: add logic for test list
        if self.args.testlist is not None:
            print(f'fatal: code for test list isnt added yet')
            sys.exit()
        self.update_run_log()

    def add_new_test(self,test_name,sim_type,corner):
        self.tests.append(Test(test_name,sim_type,corner))

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
        f.write(f"\n\nTotal: ({self.passed_tests})passed ({self.failed_tests})failed ({test.unknown_count})unknown  ({('%.10s' % (datetime.now() - self.total_start_time))})time consumed ")
        f.close()

    def update_html_mail(self):
        html_mail =f"<h2>Tests Table:</h2><table border=2 bgcolor=#D6EEEE>"
        html_mail += f"<th>Test</th> <th>duration</th> <th>status</th> <th>seed</th> <tr> "
        for test in self.tests:
            if test.passed == "passed":
                html_mail += f"<th>{test.full_name}</th><th>{test.duration}</th> <th style='background-color:#16EC0C'> {test.passed} </th><th>{test.seed}</th><tr>"
            else:
                html_mail += f"<th>{test.full_name}</th><th>{test.duration}</th> <th style='background-color:#E50E0E'> {test.passed} </th><th>{test.seed}</th><tr>"
        html_mail += "</table>"
        html_mail += (f"<h2>Total status Table:</h2><table border=2 bgcolor=#D6EEEE><th>Passed</th> <th>failed</th> <th>unknown</th> <th>duration</th> <tr>"
                      f"<th style='background-color:#16EC0C' >{self.passed_tests}</th> <th style='background-color:#E50E0E' >{self.failed_tests} </th> "
                      f"<th style='background-color:#14E5F2'>{test.unknown_count}</th> <th>{('%.10s' % (datetime.now() - self.total_start_time))}</th> <tr></table>")

    def write_command_log(self):
        file_name=f"sim/{self.args.tag}/command.log"
        f = open(file_name, "w")
        f.write(f"command used to run this sim:\n% ")
        f.write(f"{' '.join(sys.argv)}")
        f.close()
  
    def write_git_log(self):
        file_name=f"sim/{self.args.tag}/git_show.log"
        f = open(file_name, "w")
        f.write( f"{'#'*4} Caravel repo info {'#'*4}\n")
        f.write( f"Repo: {run(f'cd {self.paths.CARAVEL_ROOT};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( f"Branch name: {run(f'cd {self.paths.CARAVEL_ROOT};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( run(f'cd {self.paths.CARAVEL_ROOT};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)
        f.write( f"\n\n{'#'*4} Caravel Managment repo info {'#'*4}\n")
        f.write( f"Repo: {run(f'cd {self.paths.MCW_ROOT};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( f"Branch name: {run(f'cd {self.paths.MCW_ROOT};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( run(f'cd {self.paths.MCW_ROOT};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)
        f.write( f"\n\n{'#'*4} caravel-dynamic-sims repo info {'#'*4}\n")
        f.write( f"Repo: {run(f'cd {self.paths.COCOTB_PATH};basename -s .git `git config --get remote.origin.url`', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( f"Branch name: {run(f'cd {self.paths.COCOTB_PATH};git symbolic-ref --short HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout}")
        f.write( run(f'cd {self.paths.COCOTB_PATH};git show --quiet HEAD', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout)
        f.close()

class Test: 
    max_name_size=1
    unknown_count=0
    passed_count =0
    failed_count =0
    def __init__(self,name,sim,corner):
        self.name = name
        self.sim = sim
        self.corner = corner
        self.init_test()
    
    def init_test(self):
        self.start_time = "-"
        self.duration = "-"
        self.status   = "pending"
        self.endtime   = "-"
        self.passed   = "-"
        self.seed   = "-"
        self.full_name = f"{self.sim}-{self.name}"
        if self.sim == "GL_SDF":
            self.full_name = f"{self.sim}-{self.name}-{self.corner}"
        if len(self.full_name) > Test.max_name_size-4: 
            Test.max_name_size = len(self.full_name)+4
        Test.unknown_count +=1 
            
    def start_of_test(self):
        self.start_time_t = datetime.now()
        self.start_time = self.start_time_t.strftime("%H:%M:%S(%a)")
        self.status   = "running"

    def end_of_test(self):
        self.status   = "done"
        self.endtime   = datetime.now().strftime("%H:%M:%S(%a)")
        self.duration = ("%.10s" % (datetime.now() - self.start_time_t))
        Test.unknown_count -=1 
        #TODO add pass and failed logic counter
    