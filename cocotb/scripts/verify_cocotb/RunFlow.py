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
class RunFLow():
    def __init__(self,args) -> None:
        self.args         = args
        self.cocotb_path = self.args.cocotb_path
        self.check_valid_args()
        design_info = self.get_design_info()
        self.set_paths(design_info)
        self.set_tag()
        self.set_args(design_info)
        self.set_config_script(design_info)
        RunRegression(self.args,self.paths)

    def check_valid_args(self):
        if all(v is  None for v in [self.args.regression, self.args.test, self.args.testlist]):
            raise EnvironmentError("Should provide at least one of the following options regression, test or testlist for more info use --help")
        if self.args.sim is not None:
            print(type(self.args.sim))
            if not self.args.sim in ["RTL","GL","GL_SDF"]:
                raise ValueError(f"{self.args.sim} isnt a correct value for -sim it should be one or combination of the following RTL, GL or GL_SDF")
    def set_tag(self):
        if self.args.tag is None:
            if self.args.regression is not None:
                self.args.tag = f'{self.args.regression}_{datetime.now().strftime("%d_%b_%H_%M_%S_%f")[:-4]}'
            else: 
                self.args.tag = f'run_{datetime.now().strftime("%d_%b_%H_%M_%S_%f")[:-4]}'
        Path(f"{self.paths.SIM_PATH}/{self.args.tag}").mkdir(parents=True, exist_ok=True)
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
        Paths = namedtuple("Paths","CARAVEL_ROOT MCW_ROOT PDK_ROOT PDK CARAVEL_VERILOG_PATH VERILOG_PATH CARAVEL_PATH FIRMWARE_PATH COCOTB_PATH USER_PROJECT_ROOT SIM_PATH")
        CARAVEL_VERILOG_PATH = f"{design_info['CARAVEL_ROOT']}/verilog"
        VERILOG_PATH = f"{design_info['MCW_ROOT']}/verilog"
        CARAVEL_PATH = f"{CARAVEL_VERILOG_PATH}"
        if self.args.arm:
            FIRMWARE_PATH = f"{design_info['MCW_ROOT']}/verilog/dv/fw"
        else:
            FIRMWARE_PATH = f"{design_info['MCW_ROOT']}/verilog/dv/firmware"
        COCOTB_PATH = self.args.cocotb_path
        SIM_PATH = f"{COCOTB_PATH}/sim" if self.args.sim_path is None else f"{self.args.sim_path}/sim"
        self.paths = Paths(design_info["CARAVEL_ROOT"],design_info['MCW_ROOT'],design_info["PDK_ROOT"],design_info["PDK"],CARAVEL_VERILOG_PATH,VERILOG_PATH,CARAVEL_PATH,FIRMWARE_PATH ,COCOTB_PATH,design_info["USER_PROJECT_ROOT"],SIM_PATH)

    def set_args(self,design_info):
        if self.args.clk is None: 
            self.args.clk = design_info["clk"]

        if self.args.maxerr is None: 
            self.args.maxerr = 3
            
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
            self.args.emailto = [mail_addr for  mail_addr in design_info["emailto"] if mail_addr is not None and check_valid_mail_addr(mail_addr)]
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
        new_config_path = f'{self.paths.COCOTB_PATH}/sim/{self.args.tag}/configs.yaml'
        design_configs = dict(clock=self.args.clk,max_err=self.args.maxerr,PDK=self.args.pdk)
        design_configs.update(dict(CARAVEL_ROOT=self.paths.CARAVEL_ROOT,MCW_ROOT=self.paths.MCW_ROOT,PDK_ROOT=f'{self.paths.PDK_ROOT}/{design_info["PDK"]}'))
        with open(new_config_path, 'w') as file:
            yaml.dump(design_configs, file)



    def get_design_info(self):
        yaml_file = open(f"{self.cocotb_path}/design_info.yaml", 'r')
        design_info = yaml.safe_load(yaml_file)
        return design_info


class CocotbArgs():
    def __init__(self,test=None,sim=None,testlist=None,tag=None,maxerr =3,corner=None,seed=None,no_wave=False,clk=25,vcs=False,zip_passed=False,emailto=None,sdf_setup=None,macros=None,sim_path=None,cocotb_root=".") -> None:
        self.regression  = None
        self.test        = test
        self.sim         = sim
        self.testlist    = testlist
        self.tag         = tag 
        self.maxerr      = maxerr
        self.vcs         = vcs
        self.corner      = corner
        self.zip_passed  = zip_passed
        self.emailto     = emailto
        self.seed        = seed
        self.no_wave     = no_wave
        self.sdf_setup   = sdf_setup
        self.clk         = clk
        self.macros      = macros
        self.sim_path    = sim_path
        self.cocotb_path = cocotb_root
        # dev only
        self.cov         = None
        self.checkers_en = None
        self.lint        = None
        self.arm         = None

    def argparse_to_CocotbArgs(self,args):
        self.regression  = args.regression 
        self.test        = args.test       
        self.sim         = args.sim        
        self.testlist    = args.testlist   
        self.tag         = args.tag        
        self.maxerr      = args.maxerr     
        self.vcs         = args.vcs        
        self.corner      = args.corner     
        self.zip_passed  = args.zip_passed 
        self.emailto     = args.emailto    
        self.seed        = args.seed       
        self.no_wave     = args.no_wave    
        self.sdf_setup   = args.sdf_setup  
        self.clk         = args.clk        
        self.macros      = args.macros     
        self.sim_path    = args.sim_path   
        self.cov         = args.cov        
        self.checkers_en = args.checkers_en
        self.lint        = args.lint       
        self.arm         = args.arm        
