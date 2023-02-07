import os 
import shutil
import sys
from fnmatch import fnmatch

class RunTest:
    def __init__(self,args,paths,test) -> None:
        self.args  = args
        self.paths = paths
        self.test  = test
        self.test.start_of_test()
        self.hex_generate()
        self.runTest()
        self.test.end_of_test()

    def hex_riscv32_command_gen(self): 
        GCC_PATH = "/foss/tools/riscv-gnu-toolchain-rv32i/217e7f3debe424d61374d31e33a091a630535937/bin/"
        GCC_PREFIX = "riscv32-unknown-linux-gnu"
        GCC_COMPILE = f"{GCC_PATH}/{GCC_PREFIX}"
        SOURCE_FILES = f"{self.paths.FIRMWARE_PATH}/crt0_vex.S {self.paths.FIRMWARE_PATH}/isr.c"
        LINKER_SCRIPT = f"-Wl,-Bstatic,-T,{self.paths.FIRMWARE_PATH}/sections.lds,--strip-debug "
        CPUFLAGS = f"-g -march=rv32i -mabi=ilp32 -D__vexriscv__ -ffreestanding -nostdlib"
        includes = f"-I{self.paths.VERILOG_PATH}/dv/firmware -I{self.paths.VERILOG_PATH}/dv/generated  -I{self.paths.VERILOG_PATH}/dv/ -I{self.paths.VERILOG_PATH}/common -I{self.paths.COCOTB_PATH}/tests/common_functions/"
        elf_command = (f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
                 f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}")
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f'sed -ie "s/@10/@00/g" {self.hex_dir}/{self.test.name}.hex'
        return f" {elf_command} && {lst_command} && {hex_command} && {sed_command}"

    def hex_arm_command_gen(self): 
        GCC_COMPILE = f"arm-none-eabi"
        SOURCE_FILES = f"{self.paths.FIRMWARE_PATH}/cm0_start.s"
        LINKER_SCRIPT = f"-T {self.paths.FIRMWARE_PATH}/link.ld"
        CPUFLAGS = f"-O2 -Wall -nostdlib -nostartfiles -ffreestanding -mcpu=cortex-m0 -Wno-unused-value"
        includes = f"-I{self.paths.FIRMWARE_PATH} -I{self.paths.COCOTB_PATH}/tests/common_functions/"
        elf_command = (f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
                 f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}")
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f'sed -ie "s/@10/@00/g" {self.hex_dir}/{self.test.name}.hex'
        return f" {elf_command} &>> {self.test.full_log}&&{lst_command}&& {hex_command}&& {sed_command}"

    def hex_generate(self):
        #open docker 
        test_path =self.test_path()
        if not os.path.exists(f"{self.paths.COCOTB_PATH}/hex_files"):
            os.makedirs(f"{self.paths.COCOTB_PATH}/hex_files") # Create a new hex_files directory because it does not exist 
        self.hex_dir = f"{self.paths.COCOTB_PATH}/hex_files/"
        self.c_file = f"{test_path}/{self.test.name}.c"
        test_dir = f"{self.paths.VERILOG_PATH}/dv/tests-caravel/mem" # linker script include // TODO: to fix this in the future from the mgmt repo
        if self.args.arm : 
            command = self.hex_arm_command_gen()
        else: 
            command = self.hex_riscv32_command_gen()

        docker_command = f"docker run -u $(id -u $USER):$(id -g $USER) -it -v {self.paths.COCOTB_PATH}:{self.paths.COCOTB_PATH} -v {self.paths.CARAVEL_ROOT}:{self.paths.CARAVEL_ROOT} -v {self.paths.MCW_ROOT}:{self.paths.MCW_ROOT} efabless/dv:latest sh -c 'cd {test_dir} && {command} ' >> {self.test.full_log}"
        
        command_slipt = command.split('&&')
        self.test.full_terminal.write("docker for hex command:\n% ")
        self.test.full_terminal.write(os.path.expandvars(docker_command)+"\n\n")
        self.test.full_terminal.write("elf file generation command:\n% ")
        self.test.full_terminal.write(os.path.expandvars(command_slipt[0])+"\n\n")
        self.test.full_terminal.write("lst file generation command:\n% ")
        self.test.full_terminal.write(os.path.expandvars(command_slipt[1])+"\n\n")
        self.test.full_terminal.write("hex file generation command:\n% ")
        self.test.full_terminal.write(os.path.expandvars(command_slipt[2])+"\n\n")
        self.test.full_terminal.close()
        if not self.args.arm : # TODO add arm processor to docker
            hex_gen_state = os.system(docker_command)
        else:
            hex_gen_state = os.system(f" {command} ")
        if hex_gen_state != 0 :
            raise RuntimeError (f"Error when generating hex")
        

    def test_path(self):
        test_name = self.test.name
        test_name += ".c"
        tests_path = os.path.abspath(f"{self.paths.COCOTB_PATH}/tests")
        tests_path_user = os.path.abspath(f"{self.paths.USR_PRJ_ROOT}")
        if self.args.user_test:
            test_file =  self.find(test_name,tests_path_user)
        else:
            test_file =  self.find(test_name,tests_path)
        test_path = os.path.dirname(test_file)
        return (test_path)


    def runTest(self):
        os.environ["COCOTB_RESULTS_FILE"] = f"{self.test.test_dir}/seed.xml"
        if (self.args.iverilog): self.runTest_iverilog()
        elif(self.args.vcs): self.runTest_vcs()

    # iverilog function
    def runTest_iverilog(self):
        macros = ' -D' + ' -D'.join(self.test.macros)
        env_vars = f"-e COCOTB_RESULTS_FILE={os.getenv('COCOTB_RESULTS_FILE')} -e CARAVEL_VERILOG_PATH={self.paths.CARAVEL_VERILOG_PATH} -e VERILOG_PATH={self.paths.VERILOG_PATH} -e PDK_ROOT={self.paths.PDK_ROOT} -e PDK={self.paths.PDK}"

        if(self.test.sim=="RTL"): 
            includes = f" -f {self.paths.VERILOG_PATH}/includes/includes.rtl.caravel"
        elif(self.test.sim=="GL"): 
            includes = f"-f {self.paths.VERILOG_PATH}/includes/includes.gl.caravel"
        elif(self.test.sim=="GL_SDF"): 
            print(f"iverilog can't run SDF for test {self.test.name} Please use anothor simulator like cvc" )
            return
        user_project = f"{self.paths.COCOTB_PATH}/RTL/debug_regs.v {self.paths.COCOTB_PATH}/RTL/__user_project_wrapper.v {self.paths.COCOTB_PATH}/RTL/__user_project_gpio_example.v {self.paths.COCOTB_PATH}/RTL/__user_project_la_example.v {self.paths.COCOTB_PATH}/RTL/__user_project_addr_space_project.v"
        if self.args.caravan:
            user_project = f"{self.paths.COCOTB_PATH}/RTL/__user_analog_project_wrapper.v"
        seed = f"" 
        if self.args.seed is not None: 
            seed = f"RANDOM_SEED={self.args.seed}" 

        iverilog_command = (f"iverilog -Ttyp {macros} {includes}  -o {self.test.test_dir}/sim.vvp"
                            f" {user_project}  {self.paths.COCOTB_PATH}/RTL/caravel_top.sv -s caravel_top "
                            f" && TESTCASE={self.test.name} MODULE=module_trail {seed} vvp -M $(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus {self.test.test_dir}/sim.vvp +{ ' +'.join(self.test.macros)}")
        docker_command = f"docker run -u $(id -u $USER):$(id -g $USER) -it {env_vars} -v {self.paths.COCOTB_PATH}:{self.paths.COCOTB_PATH} -v {self.paths.CARAVEL_ROOT}:{self.paths.CARAVEL_ROOT} -v {self.paths.MCW_ROOT}:{self.paths.MCW_ROOT} -v {self.paths.PDK_ROOT}:{self.paths.PDK_ROOT}  efabless/dv:cocotb sh -c 'cd {self.test.test_dir} && {iverilog_command}' >> {self.test.full_log}"
        self.test.full_terminal = open(self.test.full_log, "a")
        self.test.full_terminal.write(f"docker command for running iverilog and cocotb:\n% ")
        self.test.full_terminal.write(os.path.expandvars(docker_command)+"\n\n")
        self.test.full_terminal.close()
        os.system(docker_command)


    # vcs function      
    def runTest_vcs(self):
        dirs = f'+incdir+\\\"{self.paths.PDK_ROOT}/{self.paths.PDK}\\\" '
        if self.test.sim == "RTL":
            shutil.copyfile(f'{self.paths.VERILOG_PATH}/includes/rtl_caravel_vcs.v', f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel_mgmt_soc_litex/verilog",new_str=f"\"{self.paths.VERILOG_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel/verilog",new_str=f"\"{self.paths.CARAVEL_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")
            shutil.copyfile(f"{self.paths.COCOTB_PATH}/includes.v", f"{self.test.test_dir}/includes.v")

        else: 
            shutil.copyfile(f'{self.paths.VERILOG_PATH}/includes/gl_caravel_vcs.v', f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel_mgmt_soc_litex/verilog",new_str=f"\"{self.paths.VERILOG_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")
            change_str(str="\"caravel/verilog",new_str=f"\"{self.paths.CARAVEL_PATH}",file_path=f"{self.paths.COCOTB_PATH}/includes.v")   
        macros = ' +define+' + ' +define+'.join(self.test.macros)
        coverage_command = ""
        if self.args.cov: 
            coverage_command = "-cm line+tgl+cond+fsm+branch+assert"
        os.environ["TESTCASE"] = f"{self.test.name}"
        os.environ["MODULE"] = f"module_trail"
        if self.args.seed is not None:
            os.environ["RANDOM_SEED"] = self.args.seed
        user_project = f"-v {self.paths.COCOTB_PATH}/RTL/debug_regs.v  -v {self.paths.COCOTB_PATH}/RTL/__user_project_wrapper.v -v {self.paths.COCOTB_PATH}/RTL/__user_project_addr_space_project.v  -v {self.paths.COCOTB_PATH}/RTL/__user_project_gpio_example.v -v {self.paths.COCOTB_PATH}/RTL/__user_project_la_example.v "
        if "user_ram" in self.test.name: 
            user_project = user_project.replace('-v RTL/__user_project_wrapper.v', '')        
        if self.args.caravan:
            user_project = f"-v RTL/__user_analog_project_wrapper.v"
        os.system(f"cd {self.test.test_dir}; vlogan -full64  -sverilog +error+30 {self.paths.COCOTB_PATH}/RTL/caravel_top.sv {user_project} {dirs}  {macros}   -l {self.test.test_dir}/analysis.log -o {self.test.test_dir} >> {self.test.full_log}")

        lint = ""
        if self.args.lint: 
            lint = "+lint=all"

        os.system(f"cd {self.test.test_dir};  vcs {lint} {coverage_command} -debug_access+all +error+50 -R -diag=sdf:verbose +sdfverbose +neg_tchk -debug_access -full64  -l {self.test.test_dir}/test.log  caravel_top -Mdir={self.test.test_dir}/csrc -o {self.test.test_dir}/simv +vpi -P pli.tab -load $(cocotb-config --lib-name-path vpi vcs) +{ ' +'.join(self.test.macros)} >> {self.test.full_log}")
        

    def find(self,name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        print(f"Test {name} doesn't exist or don't have a C file ")


    

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