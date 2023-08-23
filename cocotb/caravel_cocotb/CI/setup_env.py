import os
import subprocess
import volare
from base_class import BaseClass


class SetupEnv(BaseClass):
    def __init__(self):
        super().__init__()
        self.clone_needed_repos()
        self.pull_cocotb_docker()

    def clone_needed_repos(self):
        self.clone_repo(repo_url="https://github.com/efabless/caravel.git", target_dir="~/repos/caravel", depth=1, branch="duplicate_declaration")
        self.clone_repo(repo_url="https://github.com/M0stafaRady/caravel_cocotb_tests.git", target_dir="~/repos/user_project", depth=1, branch="cocotb-CI")
        self.clone_repo(repo_url="https://github.com/efabless/caravel_mgmt_soc_litex.git", target_dir="~/repos/caravel_mgmt_soc_litex", depth=1, branch="cooctb")
        self.download_sky130_pdk("e3b630d9b7c0e23615367d52c4f78b2d2ede58ac")

    def pull_cocotb_docker(self):
        image_name = 'efabless/dv'
        tag = 'cocotb'
        docker_pull_command = f"docker pull {image_name}:{tag}"
        self.logger.info(f"Pulling cocotb docker image using command: {docker_pull_command}")
        subprocess.run(docker_pull_command, shell=True, check=True)

    def download_sky130_pdk(self, pdk_version):
        self.logger.info(f"download sky130 pdk with pdk version = {pdk_version}")
        volare.enable(pdk_root="~/repos/pdk", pdk="sky130", version=pdk_version)

    def clone_repo(self, repo_url, target_dir, branch=None, commit=None, depth=None):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        clone_command = ["git", "clone"]

        if depth:
            clone_command.extend(["--depth", str(depth)])

        clone_command.extend([repo_url, target_dir])

        if branch:
            clone_command.extend(["--branch", branch])

        self.logger.info(f"Cloning new repo using command: {clone_command}")

        subprocess.run(clone_command, check=True)

        if commit:
            self.checkout_commit(target_dir, commit)

    def checkout_commit(self, repo_dir, commit):
        subprocess.run(["git", "checkout", commit], cwd=repo_dir, check=True)

