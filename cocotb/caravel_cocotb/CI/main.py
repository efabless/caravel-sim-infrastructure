from setup_env import SetupEnv
from gen_run_command import GenRunCommand
from checker import Checker

def main():
    SetupEnv()
    gen_run_obj = GenRunCommand()
    checker_obj = Checker()
    while gen_run_obj.is_all_cases_covered() is False:
        command = gen_run_obj.next_command()
        gen_run_obj.run_command(command)
        checker_obj.check_command(command[0])

if __name__ == "__main__":
    main()
