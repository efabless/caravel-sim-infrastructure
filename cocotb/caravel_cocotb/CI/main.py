from setup_env import SetupEnv
from gen_run_command import GenRunCommand
from checker import Checker
import os
from collections import namedtuple
DirectoryPaths = namedtuple('DirectoryPaths', ['caravel_root', 'mgmt_core_root', 'user_project_root', "pdk_root"])


def main():
    current_path = os.getcwd()
    paths = DirectoryPaths(
        caravel_root=f'{current_path}/caravel',
        mgmt_core_root=f'{current_path}/mgmt_core',
        user_project_root=f'{current_path}/user_project_root',
        pdk_root=f'{current_path}/pdk_root'
    )
    SetupEnv(paths)
    gen_run_obj = GenRunCommand(paths)
    checker_obj = Checker()
    while gen_run_obj.is_all_cases_covered() is False:
        command = gen_run_obj.next_command()
        gen_run_obj.run_command(command)
        try:
            checker_obj.check_command(command[0])
        except ValueError:
            exit(1)


if __name__ == "__main__":
    main()
