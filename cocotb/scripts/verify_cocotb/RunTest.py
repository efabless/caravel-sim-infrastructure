import os 
import sys
class RunTest:
    def __init__(self,args,paths,test) -> None:
        self.args  = args
        self.paths = paths
        self.test  = test
        self.create_log_file()
        self.test.start_of_test()
        self.hex_generate()
        # self.runTest()
        self.test.end_of_test()

    # create and open full terminal log to be able to use it before run the test
    def create_log_file(self):
        os.makedirs(f"sim/{self.args.tag}/{self.test.full_name}",exist_ok=True)
        self.sim_path = f"sim/{self.args.tag}/{self.test.full_name}"
        terminal_log=f"{self.sim_path}/fullTerminal.log"
        test_log=f"{self.sim_path}/{self.test.name}.log"
        self.test_log=open(test_log, "w")
        self.full_file=f"{self.sim_path}/full.log"
        self.full_terminal = open(self.full_file, "w")

    def hex_riscv32_command_gen(self): 
        GCC_PATH = "/foss/tools/riscv-gnu-toolchain-rv32i/217e7f3debe424d61374d31e33a091a630535937/bin/"
        GCC_PREFIX = "riscv32-unknown-linux-gnu"
        GCC_COMPILE = f"{GCC_PATH}/{GCC_PREFIX}"
        SOURCE_FILES = f"{self.paths.FIRMWARE_PATH}/crt0_vex.S {self.paths.FIRMWARE_PATH}/isr.c"
        LINKER_SCRIPT = f"-Wl,-Bstatic,-T,{self.paths.FIRMWARE_PATH}/sections.lds,--strip-debug "
        CPUFLAGS = f"-g -march=rv32i -mabi=ilp32 -D__vexriscv__ -ffreestanding -nostdlib"
        includes = f"-I{self.paths.VERILOG_PATH}/dv/firmware -I{self.paths.VERILOG_PATH}/dv/generated  -I{self.paths.VERILOG_PATH}/dv/ -I{self.paths.VERILOG_PATH}/common"
        elf_command = (f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
                 f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}")
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f"sed -ie 's/@10/@00/g' {self.hex_dir}/{self.test.name}.hex"
        return {"elf":elf_command,"lst":lst_command,"hex":hex_command,"sed":sed_command}

    def hex_arm_command_gen(self): 
        GCC_COMPILE = f"arm-none-eabi"
        SOURCE_FILES = f"{self.paths.FIRMWARE_PATH}/cm0_start.s"
        LINKER_SCRIPT = f"-T {self.paths.FIRMWARE_PATH}/link.ld"
        CPUFLAGS = f"-O2 -Wall -nostdlib -nostartfiles -ffreestanding -mcpu=cortex-m0 -Wno-unused-value"
        includes = f"-I{self.paths.FIRMWARE_PATH}"
        elf_command = (f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
                 f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}")
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f"sed -ie 's/@10/@00/g' {self.hex_dir}/{self.test.name}.hex"
        return {"elf":elf_command,"lst":lst_command,"hex":hex_command,"sed":sed_command}

    def hex_generate(self):
        #open docker 
        test_path =self.test_path()
        if not os.path.exists(f"{self.paths.COCOTB_PATH}/hex_files"):
            os.makedirs(f"{self.paths.COCOTB_PATH}/hex_files") # Create a new hex_files directory because it does not exist 
        self.hex_dir = f"{self.paths.COCOTB_PATH}/hex_files/"
        self.c_file = f"{test_path}/{self.test.name}.c"
        test_dir = f"{self.paths.VERILOG_PATH}/dv/tests-caravel/mem" # linker script include // TODO: to fix this in the future from the mgmt repo
        if self.args.arm : 
            commands = self.hex_arm_command_gen()
        else: 
            commands = self.hex_riscv32_command_gen()

        docker_command = f"docker run -u $(id -u $USER):$(id -g $USER) -it -v {self.paths.COCOTB_PATH}:{self.paths.COCOTB_PATH} -v {self.paths.CARAVEL_ROOT}:{self.paths.CARAVEL_ROOT} -v {self.paths.MCW_ROOT}:{self.paths.MCW_ROOT} efabless/dv:latest sh -c 'cd {test_dir} && {commands['elf']} && {commands['lst']} && {commands['hex']} && {commands['sed']} '"
        if not self.args.arm : # TODO add arm processor to docker
            hex_gen_state = os.system(docker_command)
        else:
            hex_gen_state = os.system(f" {commands['elf']} && {commands['lst']} && {commands['hex']} && {commands['sed']}")
        self.full_terminal.write("docker for hex command:\n% ")
        self.full_terminal.write(os.path.expandvars(docker_command)+"\n")
        self.full_terminal.write("elf file generation command:\n% ")
        self.full_terminal.write(os.path.expandvars(commands['elf'])+"\n")
        self.full_terminal.write("hex file generation command:\n% ")
        self.full_terminal.write(os.path.expandvars(commands['lst'])+"\n% ")
        self.full_terminal.write(os.path.expandvars(commands['hex'])+"\n")
        self.full_terminal.write(os.path.expandvars(commands['hex'])+"\n")
        self.full_terminal.close()
        if hex_gen_state != 0 :
            raise RuntimeError (f"Error when generating hex")
        

    def test_path(self):
        test_name = self.test.name
        test_name += ".c"
        tests_path = os.path.abspath(f"{self.paths.COCOTB_PATH}/tests")
        test_file =  self.find(test_name,tests_path)
        test_path = os.path.dirname(test_file)
        return (test_path)


    def runTest(self):
        self.full_test_name = f"{self.sim_type}-{self.test_name}"
        os.environ["COCOTB_RESULTS_FILE"] = f"{self.sim_path}/seed.xml"
        if (self.sim_type=="GL_SDF"):
            self.full_test_name =  f"{self.sim_type}-{self.test_name}-{self.corner}"
        os.environ["TESTFULLNAME"] = f"{self.full_test_name}"
        if (self.args.iverilog): self.runTest_iverilog()
        elif(self.args.vcs): self.runTest_vcs()
        self.get_seed()
        self.set_rerun_script()


    def get_seed(self):
        self.seed = "unknown"
        seed_tree = ET.parse(f'{self.sim_path}/seed.xml')
        root = seed_tree.getroot()
        for property in root.iter('property'):
            if property.attrib["name"] == "random_seed":
                self.seed = property.attrib["value"]

    def set_rerun_script(self):
        command = f"python3 verify_cocotb.py -t {self.test_name} -sim {self.sim_type} -corner {self.corner} -keep_pass_unzip -tag {self.args.tag}/{self.full_test_name}/rerun -seed {self.seed}"
        if vcs : command +=" -v "
        if coverage: command += " -cov "
        if checkers: command += " -checkers_en "
        if caravan: command += " -caravan "
        shutil.copyfile(f'{self.paths.COCOTB_PATH}/scripts/rerun_script_tamplate.py', f"{self.sim_path}/rerun.py")
        change_str(str="replace by test command",new_str=f"{command}",file_path=f"{self.sim_path}/rerun.py")
        change_str(str="replace by cocotb path",new_str=f"{self.paths.COCOTB_PATH}",file_path=f"{self.sim_path}/rerun.py")
        change_str(str="replace by mgmt Root",new_str=f"{os.getenv('MCW_ROOT')}",file_path=f"{self.sim_path}/rerun.py")
        change_str(str="replace by caravel Root",new_str=f"{os.getenv('CARAVEL_ROOT')}",file_path=f"{self.sim_path}/rerun.py")
        change_str(str="replace by orignal rerun script",new_str=f"{self.sim_path}/rerun.py",file_path=f"{self.sim_path}/rerun.py")
        change_str(str="replace by new rerun script",new_str=f"{self.sim_path}rerun/{self.full_test_name}/rerun.py",file_path=f"{self.sim_path}/rerun.py")

    def caravel_macros(self,is_vcs=False):
        macroslist = ["FUNCTIONAL",f'SIM=\\\"{self.sim_type}\\\"',"USE_POWER_PINS","UNIT_DELAY=#1",f'MAIN_PATH=\\\"{self.paths.COCOTB_PATH}\\\"']
        macroslist.extend([f'TESTNAME=\\\"{self.test_name}\\\"',f'TAG=\\\"{os.getenv("RUNTAG")}\\\"',"COCOTB_SIM",f'FTESTNAME=\\\"{self.full_test_name}\\\"'])
        macroslist.extend([f'CARAVEL_ROOT=\\\"{os.getenv("CARAVEL_ROOT")}\\\"'])
        
        if self.test_name == "la":
            macroslist.append ('LA_TESTING')
        if self.test_name in ["gpio_all_o_user","gpio_all_i_user","gpio_all_i_pu_user","gpio_all_i_pd_user","gpio_all_bidir_user"]:
            macroslist.append ('GPIO_TESTING')
        if self.test_name == "user_address_space":
            macroslist.remove('COCOTB_SIM') # using debug register in this test isn't needed
            macroslist.append('ADDR_SPACE_TESTING')
        
        if(self.sim_type=="GL"):
            macroslist.append('GL')
        elif(self.sim_type=="GL_SDF"):
            macroslist.extend(['ENABLE_SDF','GL_SDF','GL',f'SDF_POSTFIX=\\\"{self.corner[-1]}{self.corner[-1]}\\\"',f'CORNER=\\\"{self.corner[0:3]}\\\"'])
            if fnmatch(os.getenv('PDK'),"GF180*"):
                macroslist.remove("FUNCTIONAL") # functional need to be removed so specify blocks are seen in SDF sim
        if caravan:
            print ("Use caravan")
            macroslist.append(f'CARAVAN') 

        if wave_gen:
            macroslist.append(f'WAVE_GEN')

        if sdf_setup:
            macroslist.append(f'MAX_SDF')
        
        if coverage:
            macroslist.append(f'COVERAGE')
        if checkers:
            macroslist.append(f'CHECKERS')

        if not is_vcs:
            macroslist.append(f'IVERILOG')
        else: 
            macroslist.append(f'VCS')

        if fnmatch(os.getenv('PDK'),"sky*"):
            macroslist.append(f'sky')

        macroslist.append(f'CORNER_{self.corner[0:3]}')
        if ARM: 
            macroslist.extend(['ARM','AHB'])

        if "user_ram" in self.test_name: 
            macroslist.append(f'USE_USER_WRAPPER')

        if not is_vcs:
            macros = ' -D'.join(macroslist)
            macros = f'-D{macros}'
            return macros
            print(macros)
            sys.exit()
        else: 
            macros = ' +define+'.join(macroslist)
            macros = f'+define+{macros}'
            return macros
            print(macros)
            sys.exit()
    # iverilog function
    def runTest_iverilog(self):
        print(f"Start running test: {bcolors.OKBLUE}{self.sim_type}-{self.test_name}{bcolors.ENDC}")
        CARAVEL_ROOT = os.getenv('CARAVEL_ROOT')
        CARAVEL_VERILOG_PATH  = os.getenv('CARAVEL_VERILOG_PATH')
        MCW_ROOT = os.getenv('MCW_ROOT')
        VERILOG_PATH = os.getenv('VERILOG_PATH')
        CARAVEL_PATH = os.getenv('CARAVEL_PATH')
        USER_PROJECT_VERILOG  = os.getenv('USER_PROJECT_VERILOG')
        FIRMWARE_PATH = os.getenv('FIRMWARE_PATH')
        RUNTAG = self.args.tag
        ERRORMAX = os.getenv('ERRORMAX')
        PDK_ROOT = os.getenv('PDK_ROOT')
        PDK = os.getenv('PDK')
        TESTFULLNAME = os.getenv('TESTFULLNAME')
        COCOTB_RESULTS_FILE = os.getenv('COCOTB_RESULTS_FILE')
        env_vars = f"-e COCOTB_RESULTS_FILE={COCOTB_RESULTS_FILE} -e {CARAVEL_ROOT} -e CARAVEL_VERILOG_PATH={CARAVEL_VERILOG_PATH} -e MCW_ROOT={MCW_ROOT} -e VERILOG_PATH={VERILOG_PATH} -e CARAVEL_PATH={CARAVEL_PATH} -e USER_PROJECT_VERILOG={USER_PROJECT_VERILOG} -e FIRMWARE_PATH={FIRMWARE_PATH} -e RUNTAG={RUNTAG} -e ERRORMAX={ERRORMAX} -e PDK_ROOT={PDK_ROOT} -e PDK={PDK} -e TESTFULLNAME={TESTFULLNAME} -e COCOTB_PATH={COCOTB_PATH}"
        if SEED != None:
            env_vars += f" -e RANDOM_SEED={SEED} "
        if(self.sim_type=="RTL"): 
            includes = f" -f {VERILOG_PATH}/includes/includes.rtl.caravel"
        elif(self.sim_type=="GL"): 
            includes = f"-f {VERILOG_PATH}/includes/includes.gl.caravel"
        elif(self.sim_type=="GLSDF"): 
            print(f"iverilog can't run SDF for test {self.test_name} Please use anothor simulator like cvc" )
            return
        user_project = f"RTL/debug_regs.v RTL/__user_project_wrapper.v RTL/__user_project_gpio_example.v RTL/__user_project_la_example.v RTL/__user_project_addr_space_project.v"
        if caravan:
            user_project = f"RTL/__user_analog_project_wrapper.v"
        iverilog_command = (f"iverilog -Ttyp {self.caravel_macros()} {includes}  -o {self.sim_path}/sim.vvp"
                            f" {user_project}  RTL/caravel_top.sv -s caravel_top"
                            f" && TESTCASE={self.test_name} MODULE=caravel_tests vvp -M $(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus {self.sim_path}/sim.vvp")
        docker_command = f"docker run -u $(id -u $USER):$(id -g $USER) -it {env_vars} -v {COCOTB_PATH}:{COCOTB_PATH}  -v {os.getenv('CARAVEL_ROOT')}:{os.getenv('CARAVEL_ROOT')} -v {os.getenv('MCW_ROOT')}:{os.getenv('MCW_ROOT')} -v {os.getenv('PDK_ROOT')}:{os.getenv('PDK_ROOT')}   efabless/dv:cocotb sh -c 'cd {self.paths.COCOTB_PATH} && {iverilog_command}' >> {self.full_file}"
        self.full_terminal = open(self.full_file, "a")
        self.full_terminal.write(f"docker command for running iverilog and cocotb:\n% ")
        self.full_terminal.write(os.path.expandvars(docker_command)+"\n")
        self.full_terminal.close()
        
        os.system(docker_command)
        self.passed = search_str(self.test_log.name,"Test passed with (0)criticals (0)errors")
        Path(f'{self.sim_path}/{self.passed}').touch()
        if self.passed == "passed": 
            print(f"{bcolors.OKGREEN }Test: {self.sim_type}-{self.test_name} has passed{bcolors.ENDC}")
            if zip_waves:
                os.chdir(f'{self.paths.COCOTB_PATH}/{self.sim_path}')
                os.system(f'zip -m waves_logs.zip  sim.vvp full.log *.vcd')
                self.cd_cocotb()
        else : 
            print(f"{bcolors.FAIL }Test: {self.sim_type}-{self.test_name} has Failed please check logs under {bcolors.ENDC}{bcolors.OKCYAN }{self.sim_path}{bcolors.ENDC}")


    # vcs function      
    def runTest_vcs(self):
        print(f"Start running test: {bcolors.OKGREEN  } {self.sim_type}-{self.test_name} {bcolors.ENDC}")
        CARAVEL_PATH = os.getenv('CARAVEL_PATH')
        PDK_ROOT = os.getenv('PDK_ROOT')
        PDK = os.getenv('PDK')
        VERILOG_PATH = os.getenv('VERILOG_PATH')
        dirs = f'+incdir+\\\"{PDK_ROOT}/{PDK}\\\" '
        if self.sim_type == "RTL":
            shutil.copyfile(f'{VERILOG_PATH}/includes/rtl_caravel_vcs.v', f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel_mgmt_soc_litex/verilog",new_str=f"\"{VERILOG_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel/verilog",new_str=f"\"{CARAVEL_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")
        else: 
            shutil.copyfile(f'{VERILOG_PATH}/includes/gl_caravel_vcs.v', f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel_mgmt_soc_litex/verilog",new_str=f"\"{VERILOG_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel/verilog",new_str=f"\"{CARAVEL_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")     
            
        # shutil.copyfile(f'{self.test_full_dir}/{self.test_name}.hex',f'{self.sim_path}/{self.test_name}.hex')
        # if os.path.exists(f'{self.test_full_dir}/test_data'):
        #     shutil.copyfile(f'{self.test_full_dir}/test_data',f'{self.sim_path}/test_data')
            # corner example is corner nom-t so `SDF_POSTFIX = tt and `CORNER = nom
            # os.makedirs(f"annotation_logs",exist_ok=True)
            dirs = f"{dirs}  +incdir+\\\"{os.getenv('MCW_ROOT')}/verilog/\\\" "
            # +incdir+\\\"{os.getenv('CARAVEL_ROOT')}/signoff/caravel/primetime-signoff/\\\"
        coverage_command = ""
        if coverage: 
            coverage_command = "-cm line+tgl+cond+fsm+branch+assert"
        os.environ["TESTCASE"] = f"{self.test_name}"
        os.environ["MODULE"] = f"caravel_tests"
        os.environ["SIM"] = self.sim_type
        user_project = f"-v RTL/debug_regs.v  -v RTL/__user_project_wrapper.v -v RTL/__user_project_addr_space_project.v  -v RTL/__user_project_gpio_example.v -v RTL/__user_project_la_example.v "
        if "user_ram" in self.test_name: 
            user_project = user_project.replace('-v RTL/__user_project_wrapper.v', '')        
        if caravan:
            user_project = f"-v RTL/__user_analog_project_wrapper.v"
        os.system(f"vlogan -full64  -sverilog +error+30 RTL/caravel_top.sv {user_project} {dirs}  {self.caravel_macros(True)}   -l {self.sim_path}/analysis.log -o {self.sim_path} ")

        lint = ""
        if LINT: 
            lint = "+lint=all"
        os.system(f"vcs {lint} {coverage_command} -debug_access+all +error+50 -R -diag=sdf:verbose +sdfverbose +neg_tchk -debug_access -full64  -l {self.sim_path}/test.log  caravel_top -Mdir={self.sim_path}/csrc -o {self.sim_path}/simv +vpi -P pli.tab -load $(cocotb-config --lib-name-path vpi vcs)")
        self.passed = search_str(self.test_log.name,"Test passed with (0)criticals (0)errors")
        Path(f'{self.sim_path}/{self.passed}').touch()
        os.system("rm -rf AN.DB ucli.key core") # delete vcs additional files
        if LINT: 
            lint_file = open(f'{self.sim_path}/lint.log', "w")
            lint_line = False
            with open(f'{self.sim_path}/test.log', 'r') as f:
                for line in f.readlines():
                    if 'Lint' in line:
                        lint_file.write(line)
                        lint_line=True
                    elif lint_line:
                        lint_file.write(line)
                        if line.strip() == "": # line emptry
                            lint_line = False
        #delete wave when passed
        if self.passed == "passed" and zip_waves:
            os.chdir(f'{self.paths.COCOTB_PATH}/{self.sim_path}')
            os.system(f'zip -m waves_logs.zip analysis.log test.log *.vpd *.vcd')
            self.cd_cocotb()
        if os.path.exists(f"{self.paths.COCOTB_PATH}/sdfAnnotateInfo"):
            shutil.move(f"{self.paths.COCOTB_PATH}/sdfAnnotateInfo", f"{self.sim_path}/sdfAnnotateInfo")
        shutil.copyfile(f'{self.paths.COCOTB_PATH}/hex_files/{self.test_name}.hex',f'{self.sim_path}/{self.test_name}.hex')

    def find(self,name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        print(f"Test {name} doesn't exist or don't have a C file ")

