
#!/usr/bin/python3

from datetime import datetime
import os
import sys
from fnmatch import fnmatch
from pathlib import Path
import tarfile
import shutil
import xml.etree.ElementTree as ET
from scripts.verify_cocotb.RunTest import change_str
from scripts.verify_cocotb.RunTest import bcolors
class Test: 
    max_name_size=1
    unknown_count=0
    passed_count =0
    failed_count =0
    def __init__(self,name,sim,corner,args,paths):
        self.name = name
        self.sim = sim
        self.corner = corner
        self.args  = args
        self.paths = paths
        self.hex_dir = f"{self.paths.SIM_PATH}/hex_files/"
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
    
    def set_test_macros(self):
        testmacros = [f'SIM=\\\"{self.sim}\\\"',f'TESTNAME=\\\"{self.name}\\\"',f'FTESTNAME=\\\"{self.full_name}\\\"']
        if(self.sim=="GL"):
            testmacros.append('GL')
        elif(self.sim=="GL_SDF"):
            testmacros.extend(['ENABLE_SDF','GL_SDF','GL',f'SDF_POSTFIX=\\\"{self.corner[-1]}{self.corner[-1]}\\\"',f'CORNER=\\\"{self.corner[0:3]}\\\"'])
        testmacros.append(f'CORNER_{self.corner[0:3]}')

        # special tests 
        if self.name == "la":
            testmacros.append ('LA_TESTING')

        user_gpio_tests = ("gpio_all_o_user","gpio_all_i_user","gpio_all_i_pu_user","gpio_all_i_pd_user","gpio_all_bidir_user")
        if self.name in user_gpio_tests:
            testmacros.append ('GPIO_TESTING')   

        if self.name == "user_address_space":
            testmacros.append('ADDR_SPACE_TESTING')

        if "user_ram" in self.name: 
            testmacros.append(f'USE_USER_WRAPPER')

        self.macros = self.args.macros + testmacros

        if self.name == "user_address_space":
            self.macros.remove('COCOTB_SIM') # using debug register in this test isn't needed
    
    def set_user_project(self):
        if not self.args.user_test:
            user_project = f" {self.paths.COCOTB_PATH}/RTL/debug_regs.v {self.paths.COCOTB_PATH}/RTL/__user_project_wrapper.v {self.paths.COCOTB_PATH}/RTL/__user_project_gpio_example.v {self.paths.COCOTB_PATH}/RTL/__user_project_la_example.v {self.paths.COCOTB_PATH}/RTL/__user_project_addr_space_project.v"
            if self.args.caravan:
                user_project = f" {self.paths.COCOTB_PATH}/RTL/__user_analog_project_wrapper.v"
            if self.args.vcs:
                user_project = user_project.replace("{","-v {")
        else: 
            user_include = f"{self.paths.USER_PROJECT_ROOT}/verilog/includes/includes.rtl.caravel_user_project"
            user_project = f" -f {user_include}"
            if self.args.vcs:
                user_project=""
                lines = open(user_include, 'r').readlines()
                for line in lines: 
                    if line.startswith("-v"):
                        user_project += line.replace("$(USER_PROJECT_VERILOG)",f"{self.paths.USER_PROJECT_ROOT}/verilog")
        return user_project.replace("\n","")

    def start_of_test(self):
        print(f"Start running test: {bcolors.OKGREEN  } {self.full_name} {bcolors.ENDC}")
        self.start_time_t = datetime.now()
        self.create_logs()
        self.create_module_trail()
        shutil.copyfile(f'{self.paths.COCOTB_PATH}/pli.tab',f'{self.test_dir}/pli.tab')
        self.set_test_macros()
        self.set_linker_script()
        self.start_time = self.start_time_t.strftime("%H:%M:%S(%a)")
        self.status   = "running"

    def end_of_test(self):
        self.status   = "done"
        self.endtime   = datetime.now().strftime("%H:%M:%S(%a)")
        self.duration = ("%.10s" % (datetime.now() - self.start_time_t))
        self.seed = self.get_seed()
        Test.unknown_count -=1 
        is_pass = self.check_test_pass()
        self.passed   = is_pass[0]
        Path(f'{self.test_dir}/{self.passed}').touch()
        if is_pass[1]:
            Test.passed_count +=1
            print(f"{bcolors.OKGREEN }Test: {self.sim}-{self.name} has passed{bcolors.ENDC}")
        else: 
            Test.failed_count +=1
            print(f"{bcolors.FAIL }Test: {self.sim}-{self.name} has Failed please check logs under {bcolors.ENDC}{bcolors.OKCYAN }{self.test_dir}{bcolors.ENDC}")
        if self.args.lint: 
            self.create_lint_log()
        if is_pass[1] and self.args.zip_passed:
            self.tar_large_files()
        shutil.copyfile(f'{self.hex_dir}/{self.name}.hex',f'{self.test_dir}/{self.name}.hex')
        self.set_rerun_script()
        

    # create and open full terminal log to be able to use it before run the test
    def create_logs(self):
        os.makedirs(f"{self.paths.SIM_PATH}/{self.args.tag}/{self.full_name}",exist_ok=True)
        self.test_dir = f"{self.paths.SIM_PATH}/{self.args.tag}/{self.full_name}"
        self.test_log=f"{self.test_dir}/{self.name}.log"
        # self.test_log=open(test_log, "w")
        self.full_log=f"{self.test_dir}/full.log"
        self.full_terminal = open(self.full_log, "w")

    def create_lint_log(self):
            lint_file = open(f'{self.test_dir}/lint.log', "w")
            lint_line = False
            with open(f'{self.test_dir}/test.log', 'r') as f:
                for line in f.readlines():
                    if 'Lint' in line:
                        lint_file.write(line)
                        lint_line=True
                    elif lint_line:
                        lint_file.write(line)
                        if line.strip() == "": # line emptry
                            lint_line = False


    def tar_large_files(self):
            file_obj= tarfile.open(f"{self.test_dir}/waves_logs.tar","w")
            #Add other files to tar file
            if self.args.vcs:
                file_obj.add(f"{self.test_dir}/analysis.log")
                os.remove(f"{self.test_dir}/analysis.log")
                file_obj.add(f"{self.test_dir}/test.log")
                os.remove(f"{self.test_dir}/test.log")
            file_obj.add(f"{self.test_dir}/full.log")
            os.remove(f"{self.test_dir}/full.log")

            for root, dirs, files in os.walk(f"{self.test_dir}"):
                for file in files:
                    if file.endswith(".vcd") or file.endswith(".vpd"):
                        file_obj.add(f"{self.test_dir}/{file}")
                        os.remove(f"{self.test_dir}/{file}")
                    if file == "simv": 
                        file_obj.add(f"{self.test_dir}/{file}")
                        os.remove(f"{self.test_dir}/{file}")
                for dir in dirs: 
                    file_obj.add(f"{self.test_dir}/{dir}")
                    shutil.rmtree(f"{self.test_dir}/{dir}")

            file_obj.close()

    def check_test_pass(self):
        pass_pattern = "Test passed with (0)criticals (0)errors"
        with open(self.full_log, 'r') as file:
            # read all content of a file
            content = file.read()
            # check if string present in a file
            if pass_pattern in content:
                return ("passed",True)
            else:
                return ("failed",False)
    
    def get_seed(self):
        seed = "unknown"
        seed_file = f"{self.test_dir}/seed.xml"
        if not os.path.exists(seed_file): 
            return seed
        seed_tree = ET.parse(seed_file)
        root = seed_tree.getroot()
        for property in root.iter('property'):
            if property.attrib["name"] == "random_seed":
                seed = property.attrib["value"]
                return seed
        return seed


    def set_rerun_script(self):
        to_remove = ["-no_wave"]
        remove_argument(to_remove,"-t")
        remove_argument(to_remove,"-r")
        remove_argument(to_remove,"-tag")
        command = ' '.join([arg for arg in sys.argv if arg not in to_remove])
        command += f" -test {self.name} -tag {self.args.tag}/{self.full_name}/rerun -seed {self.get_seed()}  -sim {self.sim} -corner {self.corner} "
        shutil.copyfile(f'{self.paths.COCOTB_PATH}/scripts/rerun_script_tamplate.py', f"{self.test_dir}/rerun.py")
        change_str(str="replace by test command",new_str=f"{command}",file_path=f"{self.test_dir}/rerun.py")
        change_str(str="replace by cocotb path",new_str=f"{self.paths.COCOTB_PATH}",file_path=f"{self.test_dir}/rerun.py")
        change_str(str="replace by mgmt Root",new_str=f"{os.getenv('MCW_ROOT')}",file_path=f"{self.test_dir}/rerun.py")
        change_str(str="replace by caravel Root",new_str=f"{os.getenv('CARAVEL_ROOT')}",file_path=f"{self.test_dir}/rerun.py")
        change_str(str="replace by orignal rerun script",new_str=f"{self.test_dir}/rerun.py",file_path=f"{self.test_dir}/rerun.py")
        change_str(str="replace by new rerun script",new_str=f"{self.test_dir}/rerun/{self.full_name}/rerun.py",file_path=f"{self.test_dir}/rerun.py")

    def create_module_trail(self):
            f = open(f"{self.test_dir}/module_trail.py",'w')
            f.write(f"from os import path\n")
            f.write(f"import sys\n")
            if self.args.user_test:
                f.write(f"sys.path.append(path.abspath('{self.paths.USER_PROJECT_ROOT}/verilog/dv/cocotb'))\nfrom cocotb_tests import *\n")
            else:
                f.write(f"sys.path.append(path.abspath('{self.paths.COCOTB_PATH}'))\nfrom caravel_tests import *\n")
    
    def set_linker_script(self):
        linker_script_orginal = f"{self.paths.FIRMWARE_PATH}/sections.lds" if not self.args.arm else f"{self.paths.FIRMWARE_PATH}/link.ld"
        self.linker_script_file = f"{self.test_dir}/linker_script.lds"
        shutil.copyfile(f'{linker_script_orginal}', self.linker_script_file)
        if self.args.arm: 
            return
        if "mem_dff2_" in self.name: 
            change_str(str="> dff2 ",new_str="> dff ",file_path=self.linker_script_file)
            change_str(str="ORIGIN(dff2)",new_str="ORIGIN(dff)",file_path=self.linker_script_file)
            change_str(str="LENGTH(dff2)",new_str="LENGTH(dff)",file_path=self.linker_script_file)
        elif "mem_dff_" in self.name: 
            change_str(str="> dff ",new_str="> dff2 ",file_path=self.linker_script_file)
            change_str(str="> dff\n",new_str="> dff2\n",file_path=self.linker_script_file)
            change_str(str="ORIGIN(dff)",new_str="ORIGIN(dff2)",file_path=self.linker_script_file)
            change_str(str="LENGTH(dff)",new_str="LENGTH(dff2)",file_path=self.linker_script_file)



def remove_argument(to_remove,patt):
    test_name = False
    for arg in sys.argv: 
        if arg == patt:
            test_name =True 
            to_remove.append(patt)
        elif test_name: 
            if arg[0] == "-": 
                test_name =False
            else: 
                to_remove.append(arg)
