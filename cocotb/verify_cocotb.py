#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from fnmatch import fnmatch
from datetime import datetime
from pathlib import Path
import smtplib
import socket
from collections import namedtuple
import yaml
from scripts.verify_cocotb.RunRegression import RunRegression
import re
import fileinput

def check_valid_mail_addr(address):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat,address):
        print(f"valid mail {address}")
        return True
    print(f"invalid mail {address}")
    return False
class main():
    def __init__(self,args) -> None:
        self.args         = args
        self.check_valid_args()
        self.set_tag()
        design_info = self.get_design_info()
        self.set_paths(design_info)
        self.set_args(design_info)
        self.set_config_script(design_info)
        RunRegression(self.args,self.paths)

    def check_valid_args(self):
        if all(v is  None for v in [self.args.regression, self.args.test, self.args.testlist]):
            raise EnvironmentError("Should provide at least one of the following options regression, test or testlist for more info use --help")
        if self.args.sim is not None:
            if not set(self.args.sim).issubset(["RTL","GL","GL_SDF"]):
                raise ValueError(f"{self.args.sim} isnt a correct value for -sim it should be one or combination of the following RTL, GL or GL_SDF")
    def set_tag(self):
        if self.args.tag is None:
            if self.args.regression is not None:
                self.args.tag = f'{self.regression}_{datetime.now().strftime("%d_%b_%H_%M_%S_%f")[:-4]}'
            else: 
                self.args.tag = f'run_{datetime.now().strftime("%d_%b_%H_%M_%S_%f")[:-4]}'
        Path(f"sim/{self.args.tag}").mkdir(parents=True, exist_ok=True)
        print(f"Run tag: {self.args.tag}")

    def set_paths(self,design_info):
        if not os.path.exists(design_info["CARAVEL_ROOT"])  or not os.path.exists(design_info["MCW_ROOT"]) :
            raise NotADirectoryError (f"CARAVEL_ROOT or MCW_ROOT not a correct directory CARAVEL_ROOT:{design_info['CARAVEL_ROOT']} MCW_ROOT:{design_info['MCW_ROOT']}")
        if not os.path.exists(f'{design_info["PDK_ROOT"]}/{design_info["PDK"]}'):
            raise NotADirectoryError (f"PDK_ROOT/PDK is not a directory PDK_ROOT:{design_info['PDK_ROOT']}/{design_info['PDK']}")
        self.args.user_test = False 
        if design_info["USER_PROJECT_ROOT"] != "None":
            self.args.user_test = True 
            if not os.path.exists(design_info["USER_PROJECT_ROOT"]) :
                raise NotADirectoryError (f"USER_PROJECT_ROOT is not a directory USER_PROJECT_ROOT:{design_info['USER_PROJECT_ROOT']}")
            else: 
                self.configure_user_files(design_info["USER_PROJECT_ROOT"])
        Paths = namedtuple("Paths","CARAVEL_ROOT MCW_ROOT PDK_ROOT PDK CARAVEL_VERILOG_PATH VERILOG_PATH CARAVEL_PATH FIRMWARE_PATH COCOTB_PATH USER_PROJECT_ROOT")
        CARAVEL_VERILOG_PATH = f"{design_info['CARAVEL_ROOT']}/verilog"
        VERILOG_PATH = f"{design_info['MCW_ROOT']}/verilog"
        CARAVEL_PATH = f"{CARAVEL_VERILOG_PATH}"
        if self.args.arm:
            FIRMWARE_PATH = f"{design_info['MCW_ROOT']}/verilog/dv/fw"
        else:
            FIRMWARE_PATH = f"{design_info['MCW_ROOT']}/verilog/dv/firmware"
        COCOTB_PATH = os.getcwd()
        self.paths = Paths(design_info["CARAVEL_ROOT"],design_info['MCW_ROOT'],design_info["PDK_ROOT"],design_info["PDK"],CARAVEL_VERILOG_PATH,VERILOG_PATH,CARAVEL_PATH,FIRMWARE_PATH ,COCOTB_PATH,design_info["USER_PROJECT_ROOT"] )

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
        if not self.args.vcs: 
            self.args.iverilog = True

        if self.args.emailto is None: 
            self.args.emailto = [mail_addr for  mail_addr in design_info["emailto"] if check_valid_mail_addr(mail_addr)]
        else : 
            if not check_valid_mail_addr(self.args.emailto): 
                self.args.emailto = [[mail_addr for  mail_addr in self.args.emailto if check_valid_mail_addr(mail_addr)]] # if mail input aren't a valid mail will ignore it

    def configure_user_files(self,user_path):
        file = f"{user_path}/verilog/dv/cocotb/cocotb_includes.py"
        with open(file, 'r') as f:
            # read a list of lines into data
            page  = f.readlines()
            for num,line in enumerate(page): 
                if "sys.path.append(path.abspath(" in line:
                    page[num] = f"sys.path.append(path.abspath('{os.getcwd()}'))\n"
            file_w = open(file,"w")
            file_w.write("".join(page))
            file_w.close()

    def set_config_script(self,design_info):
        new_config_path = f'{self.paths.COCOTB_PATH}/sim/{self.args.tag}/configs.yalm'
        design_configs = dict(clock=self.args.clk,max_err=self.args.maxerr,PDK=self.args.pdk)
        design_configs.update(dict(CARAVEL_ROOT=self.paths.CARAVEL_ROOT,MCW_ROOT=self.paths.MCW_ROOT,PDK_ROOT=f'{self.paths.PDK_ROOT}/{design_info["PDK"]}'))
        with open(new_config_path, 'w') as file:
            yaml.dump(design_configs, file)



    def get_design_info(self):
        yalm_file = open("design_info.yalm", 'r')
        design_info = yaml.safe_load(yalm_file)
        return design_info


import argparse
parser = argparse.ArgumentParser(description='Run cocotb tests')
parser.add_argument('-regression','-r', help='name of regression can found in tests.json')
parser.add_argument('-test','-t', nargs='+' ,help='name of test if no --sim provided RTL will be run <takes list as input>')
parser.add_argument('-sim', nargs='+' ,help='Simulation type to be run RTL,GL&GL_SDF provided only when run -test <takes list as input>')
parser.add_argument('-testlist','-tl',nargs='+', help='path of testlist to be run ')
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
parser.add_argument('-macros',nargs='+', help='Add addtional verilog macros for the design ')
args = parser.parse_args()
# Arguments = namedtuple("Arguments","regression test sim corner testlist tag maxerr vcs cov checker_en  keep_pass_unzip caravan emailto seed no_wave clk lint arm sdf_setup")
# arg = Arguments(args.regression ,args.test ,args.sim ,args.corner ,args.testlist ,args.tag ,args.maxerr ,args.vcs ,args.cov ,args.checkers_en  ,args.keep_pass_unzip ,args.caravan ,args.emailto ,args.seed ,args.no_wave ,args.clk ,args.lint ,args.arm ,args.sdf_setup)
# print(args)
print(f"regression:{args.regression}, test:{args.test}, testlist:{args.testlist} sim: {args.sim}")
main(args)






"""
verilator_command = (f"verilator {macros} --vpi --public-flat-rw --prefix Vtop"
                            f" -LDFLAGS \"-Wl,-rpath,$(cocotb-config --prefix)/cocotb/libs"
                            f"-L$(cocotb-config --prefix)/cocotb/libs -lcocotbvpi_verilator -lgpi -lcocotb -lgpilog -lcocotbutils \" $(cocotb-config --share)/lib/verilator/verilator.cpp "
                            f"-y {VERILOG_PATH}/includes/includes.rtl.caravel  --cc -o sim_build/sim.vvp caravel_top.sv")




"""