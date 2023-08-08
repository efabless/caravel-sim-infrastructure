import yaml
import os
import random


class TestDefaults:
    def __init__(self) -> None:
        self.cocotb_path = os.getcwd()
        self.gpio_num = 38
        self.gpio_config_covered = [set() for _ in range(self.gpio_num)]
        self.get_design_info()
        self.update_random_user_defines()
        pass

    def test_defaults(self):
        assert True

    def get_design_info(self):
        yaml_file = open(f"design_info.yaml", "r")
        self.design_info = yaml.safe_load(yaml_file)
        yaml_file.close()

    def update_random_user_defines(self):
        """
        Update user-defined modes in a Verilog file with random values.

        Reads valid modes from a YAML file, writes them to a Verilog file along
        with random values for user-defined modes.

        Args:
            self: An instance of SomeClass.

        Returns:
            None
        """
        # Open user-defined Verilog file for writing
        with open(f'{self.design_info["USER_PROJECT_ROOT"]}/verilog/rtl/user_defines.v', 'w') as user_define_file:
            self.gpio_configs = [""] * self.gpio_num

            # Read valid modes from YAML file
            with open(f'{self.cocotb_path}/scripts/test_defaults/gpio_modes.yml') as modes_file:
                valid_modes = yaml.safe_load(modes_file)

            # Write header to Verilog file
            header = """`ifndef __USER_DEFINES_H \n`define __USER_DEFINES_H\n\n\n"""
            user_define_file.write(header)

            # Write valid modes and their values to Verilog file
            for mode, value in valid_modes.items():
                line = f"`define {mode} 13'h{value:04x}\n"  # format: `define <mode> <value>
                user_define_file.write(line)

            # Write random values for user-defined modes to Verilog file
            user_define_file.write("\n\n\n")
            valid_modes_set = set(valid_modes.keys())
            # print(valid_modes_set)
            for i in range(self.gpio_num):
                # get difference between 2 sets valid_modes_set and self.gpio_config_covered 
                modes_difference = valid_modes_set - self.gpio_config_covered[i]
                if len(modes_difference) == 0:
                    modes_difference = valid_modes_set
                if i ==0:
                    print(modes_difference) 
                random_mode = random.choice(list(modes_difference))
                self.gpio_configs[i] = random_mode
                self.gpio_config_covered[i].add(random_mode)
                line = f"`define USER_CONFIG_GPIO_{i}_INIT  {random_mode}\n"  # format: `define USER_CONFIG_GPIO_<i>_INIT  <random mode>
                user_define_file.write(line)

            # Write footer to Verilog file
            footer = "\n\n\n`endif // __USER_DEFINES_H"
            user_define_file.write(footer)

    def update_random_user_defines(self):
        """
        Update user-defined modes in a Verilog file with random values.

        Reads valid modes from a YAML file, writes them to a Verilog file along
        with random values for user-defined modes.

        Args:
            self: An instance of SomeClass.

        Returns:
            None
        """
        self.gpio_configs = [""] * self.gpio_num

        valid_modes, unvalid_modes = self.read_valid_modes()
        for i in range(len(valid_modes)):

            self.write_user_defines_to_file(valid_modes, unvalid_modes)

            self.write_random_values_to_file(valid_modes)

            self.run_gen_gpio_defaults()

            self.run_GL_test(i)

    def read_valid_modes(self):
        with open(f'{self.cocotb_path}/scripts/test_defaults/gpio_modes.yml') as modes_file:
            valid_modes = yaml.safe_load(modes_file)
            # unvalid modes that can't be testsed
            unvalid_modes = {}
            unvalid_modes["GPIO_MODE_MGMT_STD_BIDIRECTIONAL"] = valid_modes.pop("GPIO_MODE_MGMT_STD_BIDIRECTIONAL")
            unvalid_modes["GPIO_MODE_MGMT_STD_ANALOG"] = valid_modes.pop("GPIO_MODE_MGMT_STD_ANALOG")
            unvalid_modes["GPIO_MODE_USER_STD_ANALOG"] = valid_modes.pop("GPIO_MODE_USER_STD_ANALOG")  
        return valid_modes, unvalid_modes

    def write_user_defines_to_file(self, valid_modes, unvalid_modes):
        with open(f'{self.design_info["USER_PROJECT_ROOT"]}/verilog/rtl/user_defines.v', 'w') as user_define_file:
            user_define_file.write("""`ifndef __USER_DEFINES_H \n`define __USER_DEFINES_H\n\n\n""")

            for mode, value in valid_modes.items():
                line = f"`define {mode} 13'h{value:04x}\n"  # format: `define <mode> <value>
                user_define_file.write(line)

            for mode, value in unvalid_modes.items():
                line = f"`define {mode} 13'h{value:04x}\n"  # format: `define <mode> <value>
                user_define_file.write(line)


    def write_random_values_to_file(self, valid_modes):
        with open(f'{self.design_info["USER_PROJECT_ROOT"]}/verilog/rtl/user_defines.v', 'a') as user_define_file:
            with open(f'{self.design_info["USER_PROJECT_ROOT"]}/verilog/rtl/user_define_temp.txt', 'w') as user_define_txt_file:
                user_define_file.write("\n\n\n")
                for i in range(self.gpio_num):
                    modes_difference = self.get_modes_difference(valid_modes, i)
                    random_mode = random.choice(list(modes_difference))
                    # check for the fixed configured GPIO
                    if i in [0, 1, 2, 3, 4]:
                        if i in [0,1]:
                            random_mode = "GPIO_MODE_MGMT_STD_INPUT_NOPULL"
                        elif i in [2,4]:
                            random_mode = "GPIO_MODE_MGMT_STD_INPUT_NOPULL"
                        elif i == 3:
                            random_mode = "GPIO_MODE_MGMT_STD_INPUT_PULLUP"

                    self.gpio_configs[i] = random_mode
                    self.gpio_config_covered[i].add(random_mode)

                    line = f"`define USER_CONFIG_GPIO_{i}_INIT  `{random_mode}\n"  # format: `define USER_CONFIG_GPIO_<i>_INIT  <random mode>
                    user_define_file.write(line)
                    user_define_txt_file.write(f"{random_mode}\n")
                user_define_file.write("\n\n\n`endif // __USER_DEFINES_H")

    def get_modes_difference(self, valid_modes, i):
        valid_modes_set = set(valid_modes.keys())
        modes_difference = valid_modes_set - self.gpio_config_covered[i]
        if len(modes_difference) == 0:
            modes_difference = valid_modes_set
        return modes_difference
    

    def run_gen_gpio_defaults(self):
        script_path = f'{self.design_info["CARAVEL_ROOT"]}/scripts/gen_gpio_defaults.py'
        os.system(f'cd {self.design_info["CARAVEL_ROOT"]}; python3 {script_path} {self.design_info["USER_PROJECT_ROOT"]}')

    def run_RTL_test(self, i):
        os.system(f'python3 verify_cocotb.py -t check_defaults -tag default_run{i} -v -verbosity quiet -no_wave')

    def run_GL_test(self, i):
        os.system(f'python3 verify_cocotb.py -t check_defaults -tag default_run{i} -v -verbosity quiet -sim GL -no_wave')


x = TestDefaults()

