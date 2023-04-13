import os
import shutil
import subprocess
from scripts.verify_cocotb.read_defines import GetDefines
import re
import time


class RunTest:
    def __init__(self, args, paths, test) -> None:
        self.args = args
        self.paths = paths
        self.test = test
        if self.hex_generate() == "hex_generated":  # run test only if hex is generated
            self.runTest()
        self.test.end_of_test()

    def hex_riscv32_command_gen(self):
        GCC_PATH = "/foss/tools/riscv-gnu-toolchain-rv32i/217e7f3debe424d61374d31e33a091a630535937/bin/"
        GCC_PREFIX = "riscv32-unknown-linux-gnu"
        GCC_COMPILE = f"{GCC_PATH}/{GCC_PREFIX}"
        SOURCE_FILES = (
            f"{self.paths.FIRMWARE_PATH}/crt0_vex.S {self.paths.FIRMWARE_PATH}/isr.c"
        )
        LINKER_SCRIPT = f"-Wl,-Bstatic,-T,{self.test.linker_script_file},--strip-debug "
        CPUFLAGS = "-g -march=rv32i -mabi=ilp32 -D__vexriscv__ -ffreestanding -nostdlib"
        includes = f" -I{self.paths.VERILOG_PATH}/dv/firmware -I{self.paths.VERILOG_PATH}/dv/generated  -I{self.paths.VERILOG_PATH}/dv/ -I{self.paths.VERILOG_PATH}/common -I{self.paths.COCOTB_PATH}/interfaces/common_functions/ "
        includes += f" -I{self.paths.USER_PROJECT_ROOT}/verilog/dv/cocotb "
        elf_command = (
            f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
            f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}"
        )
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f'sed -ie "s/@10/@00/g" {self.hex_dir}/{self.test.name}.hex'
        return f" {elf_command} && {lst_command} && {hex_command} && {sed_command}"

    def hex_arm_command_gen(self):
        GCC_COMPILE = "arm-none-eabi"
        SOURCE_FILES = f"{self.paths.FIRMWARE_PATH}/cm0_start.s"
        LINKER_SCRIPT = f"-T {self.test.linker_script_file}"
        CPUFLAGS = "-O2 -Wall -nostdlib -nostartfiles -ffreestanding -mcpu=cortex-m0 -Wno-unused-value"
        includes = f"-I{self.paths.FIRMWARE_PATH} -I{self.paths.COCOTB_PATH}/interfaces/common_functions/"
        elf_command = (
            f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
            f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}"
        )
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f'sed -ie "s/@10/@00/g" {self.hex_dir}/{self.test.name}.hex'
        return f" {elf_command} &&{lst_command}&& {hex_command}&& {sed_command}"

    def hex_generate(self):
        # open docker
        test_path = self.test_path()
        if not os.path.exists(f"{self.paths.SIM_PATH}/hex_files"):
            os.makedirs(
                f"{self.paths.SIM_PATH}/hex_files"
            )  # Create a new hex_files directory because it does not exist
        self.hex_dir = f"{self.paths.SIM_PATH}/hex_files/"
        self.c_file = f"{test_path}/{self.test.name}.c"
        test_dir = f"{self.paths.VERILOG_PATH}/dv/tests-caravel/mem"  # linker script include // TODO: to fix this in the future from the mgmt repo
        if self.args.cpu_type == "ARM":
            command = self.hex_arm_command_gen()
        else:
            command = self.hex_riscv32_command_gen()

        docker_dir = f"-v {self.hex_dir}:{self.hex_dir} -v {self.paths.COCOTB_PATH}:{self.paths.COCOTB_PATH} -v {self.paths.CARAVEL_ROOT}:{self.paths.CARAVEL_ROOT} -v {self.paths.MCW_ROOT}:{self.paths.MCW_ROOT} -v {self.test.test_dir}:{self.test.test_dir} "
        docker_dir = (
            docker_dir
            if not self.args.user_test
            else docker_dir
            + f"-v {self.paths.USER_PROJECT_ROOT}:{self.paths.USER_PROJECT_ROOT}"
        )
        docker_command = f"docker run --init -u $(id -u $USER):$(id -g $USER) -it --sig-proxy=true {docker_dir}   efabless/dv:latest sh -ec 'cd {test_dir} && {command} '"
        command_slipt = command.split("&&")
        self.firmware_log = open(self.test.hex_log, "w")
        self.firmware_log.write("docker for hex command:\n% ")
        self.firmware_log.write(os.path.expandvars(docker_command) + "\n\n")
        self.firmware_log.write("elf file generation command:\n% ")
        self.firmware_log.write(os.path.expandvars(command_slipt[0]) + "\n\n")
        self.firmware_log.write("lst file generation command:\n% ")
        self.firmware_log.write(os.path.expandvars(command_slipt[1]) + "\n\n")
        self.firmware_log.write("hex file generation command:\n% ")
        self.firmware_log.write(os.path.expandvars(command_slipt[2]) + "\n\n")
        self.firmware_log.close()
        # don't run with docker with arm
        cmd = command if self.args.cpu_type == "ARM" else docker_command
        hex_gen_state = run_command_write_to_file(cmd, self.test.hex_log, quiet=False if self.args.verbosity == "debug" else True)
        # docker_process = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # docker_process.wait()
        # stdout, _ = docker_process.communicate()
        # ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        # stdout = ansi_escape.sub('', stdout.decode('utf-8'))
        # self.firmware_log.write(stdout)
        # hex_gen_state = docker_process.returncode
        self.firmware_log = open(self.test.hex_log, "a")
        if hex_gen_state != 0:
            # open(self.test.firmware_log, "w").write(stdout)
            print(
                f"{bcolors.FAIL}Error:{bcolors.ENDC} Fail to compile the C code for more info refer to {bcolors.OKCYAN }{self.test.hex_log}{bcolors.ENDC } "
            )
            self.firmware_log.write("Error: when generating hex")
            self.firmware_log.close()
            return "hex_error"
        self.firmware_log.write("Pass: hex generation")
        self.firmware_log.close()
        return "hex_generated"

    def test_path(self):
        test_name = self.test.name
        test_name += ".c"
        tests_path = os.path.abspath(f"{self.paths.COCOTB_PATH}/tests")
        tests_path_user = os.path.abspath(f"{self.paths.USER_PROJECT_ROOT}/verilog/dv/cocotb")
        if self.args.user_test:
            test_file = self.find(test_name, tests_path_user)
        else:
            test_file = self.find(test_name, tests_path)
        test_path = os.path.dirname(test_file)
        return test_path

    def runTest(self):
        os.environ["COCOTB_RESULTS_FILE"] = f"{self.test.test_dir}/seed.xml"
        if self.args.iverilog:
            self.runTest_iverilog()
        elif self.args.vcs:
            self.runTest_vcs()

    # iverilog function
    def runTest_iverilog(self):
        macros = " -D" + " -D".join(self.test.macros)
        env_vars = f"-e COCOTB_RESULTS_FILE={os.getenv('COCOTB_RESULTS_FILE')} -e CARAVEL_PATH={self.paths.CARAVEL_PATH} -e CARAVEL_VERILOG_PATH={self.paths.CARAVEL_VERILOG_PATH} -e VERILOG_PATH={self.paths.VERILOG_PATH} -e PDK_ROOT={self.paths.PDK_ROOT} -e PDK={self.paths.PDK} -e USER_PROJECT_VERILOG={self.paths.USER_PROJECT_ROOT}/verilog"
        if self.test.sim == "GL_SDF":
            print(
                f"iverilog can't run SDF for test {self.test.name} Please use anothor simulator like cvc"
            )
            return
        self.test.set_user_project()
        defines = GetDefines(self.test.includes_file)
        seed = "" if self.args.seed is None else f"RANDOM_SEED={self.args.seed}"
        iverilog_command = (
            f"iverilog -Ttyp {macros} -f {self.test.includes_list} -o {self.test.test_dir}/sim.vvp"
            f" {self.paths.COCOTB_PATH}/RTL/caravel_top.sv -s caravel_top "
            f" && TESTCASE={self.test.name} MODULE=module_trail {seed} vvp -M $(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus {self.test.test_dir}/sim.vvp +{ ' +'.join(self.test.macros) } {' '.join([f'+{k}={v}' if v != ''else f'+{k}' for k, v in defines.defines.items()])}"
        )
        docker_dir = f"-v {self.paths.COCOTB_PATH}:{self.paths.COCOTB_PATH} -v {self.paths.CARAVEL_ROOT}:{self.paths.CARAVEL_ROOT} -v {self.paths.MCW_ROOT}:{self.paths.MCW_ROOT} -v {self.paths.PDK_ROOT}:{self.paths.PDK_ROOT} "
        if self.args.user_test:
            docker_dir += (
                f"-v {self.paths.USER_PROJECT_ROOT}:{self.paths.USER_PROJECT_ROOT}"
            )
        docker_command = f"docker run --init -u $(id -u $USER):$(id -g $USER) -it --sig-proxy=true {env_vars} {docker_dir} efabless/dv:cocotb sh -ec 'cd {self.test.test_dir} && {iverilog_command}'"
        self.full_terminal = open(self.test.compilation_log, "w")
        self.full_terminal.write("docker command for running iverilog and cocotb:\n% ")
        self.full_terminal.write(os.path.expandvars(docker_command) + "\n\n")
        self.full_terminal.close()
        run_command_write_to_file(
            docker_command,
            self.test.compilation_log,
            quiet=True if self.args.verbosity == "quiet" else False
        )

    # vcs function
    def runTest_vcs(self):
        dirs = f'+incdir+\\"{self.paths.PDK_ROOT}/{self.paths.PDK}\\" '
        if self.test.sim == "RTL":
            shutil.copyfile(
                f"{self.paths.VERILOG_PATH}/includes/rtl_caravel_vcs.v",
                f"{self.test.test_dir}/includes.v",
            )
        else:
            shutil.copyfile(
                f"{self.paths.VERILOG_PATH}/includes/gl_caravel_vcs.v",
                f"{self.test.test_dir}/includes.v",
            )
            if self.test.sim == "GL_SDF":
                dirs += f'+incdir+\\"{self.paths.MCW_ROOT}/verilog/\\" '
                shutil.copyfile(
                    f"{self.paths.COCOTB_PATH}/sdf_includes.v",
                    f"{self.test.test_dir}/sdf_includes.v",
                )
        change_str(
            str='"caravel/verilog',
            new_str=f'"{self.paths.CARAVEL_PATH}',
            file_path=f"{self.test.test_dir}/includes.v",
        )
        change_str(
            str='"caravel_mgmt_soc_litex/verilog',
            new_str=f'"{self.paths.VERILOG_PATH}',
            file_path=f"{self.test.test_dir}/includes.v",
        )
        macros = " +define+" + " +define+".join(self.test.macros)
        coverage_command = '' 
        # coverage_command = "-cm line+tgl+cond+fsm+branch+assert" if self.args.cov else '' 
        os.environ["TESTCASE"] = f"{self.test.name}"
        os.environ["MODULE"] = "module_trail"
        if self.args.seed is not None:
            os.environ["RANDOM_SEED"] = self.args.seed
        self.test.set_user_project()
        defines = GetDefines(self.test.includes_file)
        vlogan_cmd = f"cd {self.test.test_dir}; vlogan -full64 -sverilog +error+30 {self.paths.COCOTB_PATH}/RTL/caravel_top.sv {dirs}  {macros}   -l {self.test.test_dir}/analysis.log -o {self.test.test_dir} "
        run_command_write_to_file(vlogan_cmd, self.test.compilation_log, quiet=False if self.args.verbosity == "debug" else True)
        lint = "+lint=all" if self.args.lint else ""
        vcs_cmd = f"cd {self.test.test_dir};  vcs {lint} {coverage_command} -debug_access+all +error+50 -R -diag=sdf:verbose +sdfverbose +neg_tchk -debug_access -full64  -l {self.test.test_dir}/test.log  caravel_top -Mdir={self.test.test_dir}/csrc -o {self.test.test_dir}/simv +vpi -P pli.tab -load $(cocotb-config --lib-name-path vpi vcs) +{ ' +'.join(self.test.macros)} {' '.join([f'+{k}={v}' if v != ''else f'+{k}' for k, v in defines.defines.items()])}"
        run_command_write_to_file(
            vcs_cmd,
            self.test.compilation_log,
            quiet=True if self.args.verbosity == "quiet" else False
        )

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        print(f"Test {name} doesn't exist or don't have a C file ")


def run_command_write_to_file(cmd, file, quiet=True):
    """run command and write output to file return 0 if no error"""
    try:
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1024
        )
        with open(file, "a") as f:
            while True:
                out = process.stdout.readline().decode("utf-8")
                ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
                stdout = ansi_escape.sub("", out)
                if process.poll() is not None:
                    break
                if out:
                    if not quiet:
                        print(out.replace("\n", "", 1))
                        time.sleep(0.01)
                    f.write(stdout)
    except Exception as e:
        print(f"Docker process stopped by user {e}")
        process.stdin.write(b'\x03') # Send the Ctrl+C signal to the Docker process
        process.terminate()

    return process.returncode


def capture_output(process, file):
    for line in iter(process.stdout.readline, b""):
        file.write(line.decode())
        print(line.decode(), end="")


def capture_error(process, file):
    for line in iter(process.stderr.readline, b""):
        file.write(line.decode())
        print(line.decode(), end="")


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def change_str(str, new_str, file_path):
    # Read in the file
    with open(file_path, "r") as file:
        filedata = file.read()

    filedata = filedata.replace(str, new_str)

    # Write the file out again
    with open(file_path, "w") as file:
        file.write(filedata)
