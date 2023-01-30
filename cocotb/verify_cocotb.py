#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path
from fnmatch import fnmatch
from datetime import datetime
import random
from pathlib import Path
import shutil
import threading
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import logging 
import xml.etree.ElementTree as ET
from collections import namedtuple
import yaml
from scripts.verify_cocotb.RunRegression import RunRegression

iverilog = True
vcs = False
coverage = False
checkers = False
zip_waves = True
caravan = False 
html_mail =f""
tests_pass = "Pass:"
SEED = None
wave_gen = True
sdf_setup = False
LINT = False
ARM = False
sky =fnmatch(os.getenv('PDK'),'sky*')
def go_up(path, n):
    for i in range(n):
        path = os.path.dirname(path)
    return path
# search pattern in file
def search_str(file_path, word):
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # check if string present in a file
        if word in content:
            return "passed"
        else:
            return "failed"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def change_str(str,new_str,file_path):
    # Read in the file
    with open(file_path, 'r') as file :
        filedata = file.read()

    filedata = filedata.replace(str, new_str)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)


class main():
    def __init__(self,args) -> None:
        self.args         = args
        self.check_valid_args()
        self.set_tag()
        design_info = self.get_design_info()
        self.set_paths(design_info)
        self.set_args(design_info)
        self.set_config_script()
        RunRegression(self.args,self.paths)
        if args.emailto is not None:
            self.send_mail(args.emailto)

    def check_valid_args(self):
        if all(v is  None for v in [self.args.regression, self.args.test, self.args.testlist]):
            raise EnvironmentError("Should provide at least one of the following options regression, test or testlist for more info use --help")
        if self.args.sim is not None:
            if not set(self.args.sim).issubset(["RTL","GL","GL_SDF"]):
                raise ValueError(f"{self.args.sim} isnt a correct value for -sim it should be one or combination of the following RTL, GL or GL_SDF")
    def set_tag(self):
        if self.args.tag is None:
            if self.args.regression is not None:
                self.args.tag = f'{self.regression}_t{datetime.now().strftime("%d_%b_%H_%M_%S.%f")}'
            else: 
                self.args.tag = f'run_{datetime.now().strftime("%d_%b_%H_%M_%S_%f")[:-4]}'
        Path(f"sim/{self.args.tag}").mkdir(parents=True, exist_ok=True)
        print(f"Run tag: {self.args.tag}")

    def set_paths(self,design_info):
        if not os.path.exists(design_info["CARAVEL_ROOT"])  or not os.path.exists(design_info["MCW_ROOT"]) :
            raise NotADirectoryError (f"CARAVEL_ROOT or MCW_ROOT are not defined CARAVEL_ROOT:{design_info['CARAVEL_ROOT']} MCW_ROOT:{design_info['MCW_ROOT']}")
        if not os.path.exists(design_info["PDK_ROOT"]):
            raise NotADirectoryError (f"PDK_ROOT is not a directory PDK_ROOT:{design_info['PDK_ROOT']}")
        Paths = namedtuple("Paths","CARAVEL_ROOT MCW_ROOT PDK_ROOT CARAVEL_VERILOG_PATH VERILOG_PATH CARAVEL_PATH FIRMWARE_PATH COCOTB_PATH")
        CARAVEL_VERILOG_PATH = f"{design_info['CARAVEL_ROOT']}/verilog"
        VERILOG_PATH = f"{design_info['MCW_ROOT']}/verilog"
        CARAVEL_PATH = f"{CARAVEL_VERILOG_PATH}"
        if self.args.arm:
            FIRMWARE_PATH = f"{design_info['MCW_ROOT']}/verilog/dv/fw"
        else:
            FIRMWARE_PATH = f"{design_info['MCW_ROOT']}/verilog/dv/firmware"
        COCOTB_PATH = os.getcwd()
        self.paths = Paths(design_info["CARAVEL_ROOT"],design_info['MCW_ROOT'],design_info["PDK_ROOT"],CARAVEL_VERILOG_PATH,VERILOG_PATH,CARAVEL_PATH,FIRMWARE_PATH ,COCOTB_PATH )

    def set_args(self,design_info):
        if self.args.clk is None: 
            self.args.clk = design_info["clk"]

        self.args.caravan = design_info["caravan"]

        if self.args.sim is None: 
            self.args.sim= ["RTL"]

        if self.args.corner == None: 
            self.args.corner= ["nom-t"]

        if "sky130" in design_info['PDK'] : 
            self.args.pdk = "sky130"
        elif "gf180" in design_info['PDK'] : 
            self.args.pdk = "gf180"

        self.args.iverilog = False
        if self.args.vcs is None: 
            self.args.iverilog = True

    def set_config_script(self):
        new_config_path = f'{self.paths.COCOTB_PATH}/sim/{self.args.tag}/configs.py'
        shutil.copyfile(f'{self.paths.COCOTB_PATH}/scripts/config_script_tamplate.py', new_config_path)
        change_str(str="replace by clock",new_str=f"{self.args.clk}",file_path=new_config_path)
        change_str(str="replace by max number of errer",new_str=self.args.maxerr,file_path=new_config_path)
        change_str(str="replace sky enable",new_str=f"{sky}",file_path=new_config_path)
        change_str(str="replace CARAVEL_ROOT",new_str=f"\"{os.getenv('CARAVEL_ROOT')}\"",file_path=new_config_path)
        change_str(str="replace MCW_ROOT",new_str=f"\"{os.getenv('MCW_ROOT')}\"",file_path=new_config_path)
        change_str(str="replace PDK_ROOT",new_str=f"\"{os.getenv('PDK_ROOT')}\"",file_path=new_config_path)
        change_str(str="replace PDK",new_str=f"\"{os.getenv('PDK')}\"",file_path=new_config_path)

    def send_mail(self,mails):
        #get commits 
        showlog = f"{self.paths.COCOTB_PATH}/sim/{self.args.tag}/git_show.log"
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
        mail_sub += html_mail
        mail_sub += f"<p>best regards, </p></body></html>"
        # print(mail_sub)
        msg = MIMEMultipart("alternative", None, [ MIMEText(mail_sub,'html')])
        msg['Subject'] = f'{tests_pass} {self.TAG} run results'
        msg['From'] = "verification@efabless.com"
        msg['To'] = ", ".join(mails)
        docker = False
        if docker: 
            mail_command = f'echo "{mail_sub}" | mail -a "Content-type: text/html;" -s "{msg["Subject"]}" {mails[0]}'
            docker_command = f"docker run -it -u $(id -u $USER):$(id -g $USER) efabless/dv:mail sh -c '{mail_command}'"
            print(docker_command)
            os.system(docker_command)
        else:
            # Send the message via our own SMTP server.
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()

    def get_design_info(self):
        yalm_file = open("design_info.yalm", 'r')
        design_info = yaml.safe_load(yalm_file)
        return design_info


import argparse
parser = argparse.ArgumentParser(description='Run cocotb tests')
parser.add_argument('-regression','-r', help='name of regression can found in tests.json')
parser.add_argument('-test','-t', nargs='+' ,help='name of test if no --sim provided RTL will be run <takes list as input>')
parser.add_argument('-sim', nargs='+' ,help='Simulation type to be run RTL,GL&GL_SDF provided only when run -test <takes list as input>')
parser.add_argument('-testlist','-tl', help='path of testlist to be run ')
parser.add_argument('-tag', help='provide tag of the run default would be regression name and if no regression is provided would be run_<random float>_<timestamp>_')
parser.add_argument('-maxerr', help='max number of errors for every test before simulation breaks default = 3')
parser.add_argument('-vcs','-v',action='store_true', help='use vcs as compiler if not used iverilog would be used')
parser.add_argument('-cov',action='store_true', help='enable code coverage')
parser.add_argument('-checkers_en',action='store_true', help='enable whitebox models checkers and coverage no need to use -cov ')
parser.add_argument('-corner','-c', nargs='+' ,help='Corner type in case of GL_SDF run has to be provided')
parser.add_argument('-keep_pass_unzip',action='store_true', help='Normally the waves and logs of passed tests would be zipped. Using this option they wouldn\'t be zipped')
parser.add_argument('-emailto','-mail', nargs='+' ,help='mails to send results to when results finish')
parser.add_argument('-seed' ,help='run with specific seed')
parser.add_argument('-no_wave',action='store_true', help='disable dumping waves')
parser.add_argument('-sdf_setup',action='store_true', help='targeting setup violations by taking the sdf mamximum values')
parser.add_argument('-clk', help='define the clock period in ns default defined at design_info.yalm')
parser.add_argument('-lint',action='store_true', help='generate lint log -v must be used')
parser.add_argument('-arm',action='store_true', help='generate lint log -v must be used')
args = parser.parse_args()
if (args.vcs) : 
    iverilog = False
    vcs = True
if args.cov: 
    coverage = True
if args.checkers_en: 
    checkers = True
    coverage = True

if args.keep_pass_unzip: 
    zip_waves = False
if args.seed != None: 
    SEED = args.seed
if args.no_wave: 
    wave_gen = False
if args.sdf_setup: 
    sdf_setup = True
if args.maxerr == None:
    args.maxerr ="3"
if args.lint: 
    LINT = True
if args.arm: 
    ARM = True

# Arguments = namedtuple("Arguments","regression test sim corner testlist tag maxerr vcs cov checker_en  keep_pass_unzip caravan emailto seed no_wave clk lint arm sdf_setup")
# arg = Arguments(args.regression ,args.test ,args.sim ,args.corner ,args.testlist ,args.tag ,args.maxerr ,args.vcs ,args.cov ,args.checkers_en  ,args.keep_pass_unzip ,args.caravan ,args.emailto ,args.seed ,args.no_wave ,args.clk ,args.lint ,args.arm ,args.sdf_setup)
print(args)
print(f"regression:{args.regression}, test:{args.test}, testlist:{args.testlist} sim: {args.sim}")
main(args)






"""
verilator_command = (f"verilator {macros} --vpi --public-flat-rw --prefix Vtop"
                            f" -LDFLAGS \"-Wl,-rpath,$(cocotb-config --prefix)/cocotb/libs"
                            f"-L$(cocotb-config --prefix)/cocotb/libs -lcocotbvpi_verilator -lgpi -lcocotb -lgpilog -lcocotbutils \" $(cocotb-config --share)/lib/verilator/verilator.cpp "
                            f"-y {VERILOG_PATH}/includes/includes.rtl.caravel  --cc -o sim_build/sim.vvp caravel_top.sv")




"""