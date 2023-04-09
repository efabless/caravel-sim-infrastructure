#!/usr/bin/python3

from datetime import datetime
import os
import sys
from pathlib import Path
import tarfile
import shutil
import xml.etree.ElementTree as ET
from scripts.verify_cocotb.RunTest import change_str
from scripts.verify_cocotb.RunTest import bcolors


class Test:
    max_name_size = 1
    unknown_count = 0
    passed_count = 0
    failed_count = 0

    def __init__(self, name, sim, corner, args, paths):
        self.name = name
        self.sim = sim
        self.corner = corner
        self.args = args
        self.paths = paths
        self.hex_dir = f"{self.paths.SIM_PATH}/hex_files/"
        self.init_test()

    def init_test(self):
        self.start_time = "-"
        self.duration = "-"
        self.status = "pending"
        self.endtime = "-"
        self.passed = "-"
        self.seed = "-"
        self.full_name = f"{self.sim}-{self.name}"
        if self.sim == "GL_SDF":
            self.full_name = f"{self.sim}-{self.name}-{self.corner}"
        if len(self.full_name) > Test.max_name_size - 4:
            Test.max_name_size = len(self.full_name) + 4
        Test.unknown_count += 1

    def set_test_macros(self):
        testmacros = [
            f'SIM=\\"{self.sim}\\"',
            f'TESTNAME=\\"{self.name}\\"',
            f'FTESTNAME=\\"{self.full_name}\\"',
            f'SIM_DIR=\\"{self.paths.SIM_PATH}/{self.args.tag}\\"'
        ]
        if self.sim == "GL":
            testmacros.append("GL")
        elif self.sim == "GL_SDF":
            testmacros.extend(
                [
                    "ENABLE_SDF",
                    "GL_SDF",
                    "GL",
                    f'SDF_POSTFIX=\\"{self.corner[-1]}{self.corner[-1]}\\"',
                    f'CORNER=\\"{self.corner[0:3]}\\"',
                ]
            )
        testmacros.append(f"CORNER_{self.corner[0:3]}")

        # special tests
        if self.name == "la":
            testmacros.append("LA_TESTING")

        user_gpio_tests = (
            "gpio_all_o_user",
            "gpio_all_i_user",
            "gpio_all_i_pu_user",
            "gpio_all_i_pd_user",
            "gpio_all_bidir_user",
        )
        if self.name in user_gpio_tests:
            testmacros.append("GPIO_TESTING")

        if self.name == "user_address_space":
            testmacros.append("ADDR_SPACE_TESTING")

        if "user_ram" in self.name:
            testmacros.append("USE_USER_WRAPPER")

        self.macros = self.args.macros + testmacros

        if self.name == "user_address_space":
            self.macros.remove(
                "COCOTB_SIM"
            )  # using debug register in this test isn't needed

    def set_user_project(self):
        if not self.args.user_test:
            user_project = f" {self.paths.COCOTB_PATH}/RTL/debug_regs.v {self.paths.COCOTB_PATH}/RTL/__user_project_wrapper.v {self.paths.COCOTB_PATH}/RTL/__user_project_gpio_example.v {self.paths.COCOTB_PATH}/RTL/__user_project_la_example.v {self.paths.COCOTB_PATH}/RTL/__user_project_addr_space_project.v"
            if self.args.caravan:
                user_project = (
                    f" {self.paths.COCOTB_PATH}/RTL/__user_analog_project_wrapper.v"
                )
            if self.args.vcs:
                user_project = user_project.replace("{", "-v {")
        else:
            if self.sim == "RTL":
                user_include = f"{self.paths.USER_PROJECT_ROOT}/verilog/includes/includes.rtl.caravel_user_project"
            else:
                user_include = f"{self.paths.USER_PROJECT_ROOT}/verilog/includes/includes.gl.caravel_user_project"

            user_project = f" -f {user_include}"
            self.write_includes_file(user_include)
            if self.args.vcs:
                user_project = ""
                lines = open(user_include, "r").readlines()
                for line in lines:
                    if line.startswith("-v"):
                        user_project += line.replace(
                            "$(USER_PROJECT_VERILOG)",
                            f"{self.paths.USER_PROJECT_ROOT}/verilog",
                        ) + " "
        return user_project.replace("\n", "")

    def start_of_test(self):
        print(f"Start running test: {bcolors.OKBLUE  } {self.full_name} {bcolors.ENDC}")
        self.start_time_t = datetime.now()
        self.create_logs()
        self.create_module_trail()
        shutil.copyfile(f"{self.paths.COCOTB_PATH}/pli.tab", f"{self.test_dir}/pli.tab")
        self.set_test_macros()
        self.set_linker_script()
        self.start_time = self.start_time_t.strftime("%H:%M:%S(%a)")
        self.status = "running"

    def end_of_test(self):
        self.status = "done"
        self.endtime = datetime.now().strftime("%H:%M:%S(%a)")
        self.duration = "%.10s" % (datetime.now() - self.start_time_t)
        self.seed = self.get_seed()
        Test.unknown_count -= 1
        is_pass = self.check_test_pass()
        self.passed = is_pass[0]
        Path(f"{self.test_dir}/{self.passed}").touch()
        if is_pass[1]:
            Test.passed_count += 1
            print(
                f"{bcolors.OKGREEN }Test: {self.sim}-{self.name} has passed{bcolors.ENDC}"
            )
        else:
            Test.failed_count += 1
            if not os.path.isfile(self.compilation_log):
                pass
            elif os.path.isfile(self.test_log):
                print(
                    f"{bcolors.FAIL }Fail{bcolors.ENDC}: Test {self.sim}-{self.name} has Failed for more info refer to {bcolors.OKCYAN }{self.test_log}{bcolors.ENDC}"
                )
            else:
                print(
                    f"{bcolors.FAIL }Error{bcolors.ENDC}: Fail to compile the verilog code for more info refer to {bcolors.OKCYAN }{self.compilation_log}{bcolors.ENDC}"
                )

        if self.args.lint:
            self.create_lint_log()
        if is_pass[1] and self.args.zip_passed:
            self.tar_large_files()

        if os.path.isfile(f"{self.hex_dir}/{self.name}.hex"):
            shutil.copyfile(
                f"{self.hex_dir}/{self.name}.hex", f"{self.test_dir}/{self.name}.hex"
            )
        self.set_rerun_script()

    # create and open full terminal log to be able to use it before run the test
    def create_logs(self):
        self.test_dir = f"{self.paths.SIM_PATH}/{self.args.tag}/{self.full_name}"
        # remove if already exists
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)
        self.test_log = f"{self.test_dir}/{self.name}.log"
        self.firmware_log = f"{self.test_dir}/firmware_error.log"
        # self.test_log=open(test_log, "w")
        self.compilation_log = f"{self.test_dir}/compilation.log"
        self.hex_log = f"{self.test_dir}/firmware.log"
        # self.full_terminal = open(self.compilation_log, "w")

    def create_lint_log(self):
        lint_file = open(f"{self.test_dir}/lint.log", "w")
        lint_line = False
        with open(f"{self.test_dir}/test.log", "r") as f:
            for line in f.readlines():
                if "Lint" in line:
                    lint_file.write(line)
                    lint_line = True
                elif lint_line:
                    lint_file.write(line)
                    if line.strip() == "":  # line emptry
                        lint_line = False

    def tar_large_files(self):
        file_obj = tarfile.open(f"{self.test_dir}/waves_logs.tar", "w")
        # Add other files to tar file
        if self.args.vcs:
            file_obj.add(f"{self.test_dir}/analysis.log")
            os.remove(f"{self.test_dir}/analysis.log")
            file_obj.add(f"{self.test_dir}/test.log")
            os.remove(f"{self.test_dir}/test.log")
        file_obj.add(f"{self.test_dir}/compilation.log")
        os.remove(f"{self.test_dir}/compilation.log")
        file_obj.add(f"{self.test_dir}/firmware.log")
        os.remove(f"{self.test_dir}/firmware.log")

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
        # if file doesn't exist
        if not os.path.isfile(self.test_log):
            return ("failed", False)
        with open(self.test_log, "r") as file:
            # read all content of a file
            content = file.read()
            # check if string present in a file
            if pass_pattern in content:
                return ("passed", True)
            else:
                return ("failed", False)

    def get_seed(self):
        seed = "unknown"
        seed_file = f"{self.test_dir}/seed.xml"
        if not os.path.exists(seed_file):
            return seed
        seed_tree = ET.parse(seed_file)
        root = seed_tree.getroot()
        for property in root.iter("property"):
            if property.attrib["name"] == "random_seed":
                seed = property.attrib["value"]
                return seed
        return seed

    def set_rerun_script(self):
        to_remove = ["-no_wave"]
        remove_argument(to_remove, "-t")
        remove_argument(to_remove, "-tl")
        remove_argument(to_remove, "-r")
        remove_argument(to_remove, "-tag")
        remove_argument(to_remove, "-seed")
        remove_argument(to_remove, "-sim")
        remove_argument(to_remove, "-corner")
        command = " ".join([arg for arg in sys.argv if arg not in to_remove])
        command += f" -test {self.name} -tag {self.args.tag}/{self.full_name}/rerun   -sim {self.sim} -corner {self.corner} "
        if self.get_seed().isdigit():
            command += f" -seed {self.get_seed()} "
        shutil.copyfile(
            f"{self.paths.COCOTB_PATH}/scripts/rerun_script_tamplate.py",
            f"{self.test_dir}/rerun.py",
        )
        change_str(
            str="replace by test command",
            new_str=f"{command}",
            file_path=f"{self.test_dir}/rerun.py",
        )
        change_str(
            str="replace by cocotb path",
            new_str=f"{self.paths.COCOTB_PATH}",
            file_path=f"{self.test_dir}/rerun.py",
        )
        change_str(
            str="replace by mgmt Root",
            new_str=f"{self.paths.MCW_ROOT}",
            file_path=f"{self.test_dir}/rerun.py",
        )
        change_str(
            str="replace by caravel Root",
            new_str=f"{self.paths.CARAVEL_ROOT}",
            file_path=f"{self.test_dir}/rerun.py",
        )
        change_str(
            str="replace by orignal rerun script",
            new_str=f"{self.test_dir}/rerun.py",
            file_path=f"{self.test_dir}/rerun.py",
        )
        change_str(
            str="replace by new rerun script",
            new_str=f"{self.test_dir}/rerun/{self.full_name}/rerun.py",
            file_path=f"{self.test_dir}/rerun.py",
        )

    def create_module_trail(self):
        f = open(f"{self.test_dir}/module_trail.py", "w")
        f.write("from os import path\n")
        f.write("import sys\n")
        if self.args.user_test:
            f.write(
                f"sys.path.append(path.abspath('{self.paths.USER_PROJECT_ROOT}/verilog/dv/cocotb'))\nfrom cocotb_tests import *\n"
            )
        else:
            f.write(
                f"sys.path.append(path.abspath('{self.paths.COCOTB_PATH}'))\nfrom caravel_tests import *\n"
            )

    def set_linker_script(self):
        linker_script_orginal = (
            f"{self.paths.FIRMWARE_PATH}/sections.lds"
            if self.args.cpu_type == "VexRISC"
            else f"{self.paths.FIRMWARE_PATH}/link.ld"
        )
        self.linker_script_file = f"{self.test_dir}/linker_script.lds"
        shutil.copyfile(f"{linker_script_orginal}", self.linker_script_file)
        if self.args.cpu_type == "ARM":
            return
        if "mem_dff2_" in self.name:
            change_str(
                str="> dff2 ", new_str="> dff ", file_path=self.linker_script_file
            )
            change_str(
                str="ORIGIN(dff2)",
                new_str="ORIGIN(dff)",
                file_path=self.linker_script_file,
            )
            change_str(
                str="LENGTH(dff2)",
                new_str="LENGTH(dff)",
                file_path=self.linker_script_file,
            )
        elif "mem_dff_" in self.name:
            change_str(
                str="> dff ", new_str="> dff2 ", file_path=self.linker_script_file
            )
            change_str(
                str="> dff\n", new_str="> dff2\n", file_path=self.linker_script_file
            )
            change_str(
                str="ORIGIN(dff)",
                new_str="ORIGIN(dff2)",
                file_path=self.linker_script_file,
            )
            change_str(
                str="LENGTH(dff)",
                new_str="LENGTH(dff2)",
                file_path=self.linker_script_file,
            )

    # takes command file and write file for includes
    def write_includes_file(self, file):
        paths = self.convert_list_to_include(file)
        # write to include file in the top of the file
        self.includes_file = f"{self.test_dir}/includes.v"
        if self.args.vcs:
            includes = open(self.includes_file, 'r').read()
        else:
            if self.sim == "RTL":
                includes = self.convert_list_to_include(f"{self.paths.VERILOG_PATH}/includes/includes.rtl.caravel")
            elif self.sim == "GL":
                includes = self.convert_list_to_include(f"{self.paths.VERILOG_PATH}/includes/includes.gl.caravel")
        includes = paths + includes
        open(self.includes_file, "w").write(includes)
        move_defines_to_start(self.includes_file, 'defines.v"')
      
        if self.args.iverilog:
            # when running with iverilog add includes list also
            paths = open(file, "r").read()
            self.includes_list = f"{self.test_dir}/includes"
            if self.sim == "RTL":
                includes = open(f"{self.paths.VERILOG_PATH}/includes/includes.rtl.caravel", 'r').read()
            elif self.sim == "GL":
                includes = open(f"{self.paths.VERILOG_PATH}/includes/includes.gl.caravel", 'r').read()
            includes = paths + includes
            open(self.includes_list, "w").write(includes)
            move_defines_to_start(self.includes_list, 'defines.v')
        

    def convert_list_to_include(self, file):
        paths = ""
        with open(file, "r") as f:
            for line in f:
                # Remove leading and trailing whitespace
                line = line.strip()
                # Check if line is not empty or a comment
                if line and not line.startswith("#"):
                    # Replace $(VERILOG_PATH) with actual path
                    line = line.replace("$(VERILOG_PATH)", self.paths.VERILOG_PATH)
                    line = line.replace("$(CARAVEL_PATH)", self.paths.CARAVEL_PATH)
                    line = line.replace(
                        "$(USER_PROJECT_VERILOG)",
                        f"{self.paths.USER_PROJECT_ROOT}/verilog",
                    )
                    line = line.replace("$(PDK_ROOT)", f"{self.paths.PDK_ROOT}")
                    line = line.replace("$(PDK)", f"{self.paths.PDK}")
                    # Extract file path from command
                    if line.startswith("-v"):
                        file_path = line.split(" ")[1]
                        paths += f'`include "{file_path}"\n'
        return paths

def remove_argument(to_remove, patt):
    test_name = False
    for arg in sys.argv:
        if arg == patt:
            test_name = True
            to_remove.append(patt)
        elif test_name:
            if arg[0] == "-":
                test_name = False
            else:
                to_remove.append(arg)


def move_defines_to_start(filename, pattern):
    # Read the contents of the file into a list of lines
    # print(f"file name = {filename}")
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Extract the lines that end with "defines.v"
    defines_lines = [f"{line.strip()}\n" for line in lines if line.strip().endswith(pattern)]
    # print(f"defines_lines {defines_lines}")
    # Remove the extracted lines from the original list
    lines = [f"{line.strip()}\n" for line in lines if line not in defines_lines]

    # Insert the extracted lines at the start of the list
    lines = defines_lines + lines

    # Write the modified list of lines back to the file
    with open(filename, 'w') as f:
        f.writelines(lines)