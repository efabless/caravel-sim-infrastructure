import os
import subprocess
import volare
from base_class import BaseClass


class SetupEnv(BaseClass):
    def __init__(self, paths):
        super().__init__()
        self.paths = paths
        self.clone_needed_repos()
        self.pull_cocotb_docker()

    def clone_needed_repos(self):
        self.clone_repo(repo_url="https://github.com/efabless/caravel.git", target_dir=self.paths.caravel_root, depth=1, branch="duplicate_declaration")
        self.clone_repo(repo_url="https://github.com/M0stafaRady/caravel_cocotb_tests.git", target_dir=self.paths.user_project_root, depth=1, branch="cocotb-CI")
        self.clone_repo(repo_url="https://github.com/efabless/caravel_mgmt_soc_litex.git", target_dir=self.paths.mgmt_core_root, depth=1, branch="cooctb")
        self.download_sky130_pdk("e3b630d9b7c0e23615367d52c4f78b2d2ede58ac")

    def pull_cocotb_docker(self):
        image_name = 'efabless/dv'
        tag = 'cocotb'
        docker_pull_command = f"docker pull {image_name}:{tag}"
        self.logger.info(f"Pulling cocotb docker image using command: {docker_pull_command}")
        subprocess.run(docker_pull_command, shell=True, check=True)

    def download_sky130_pdk(self, pdk_version):
        self.logger.info(f"download sky130 pdk with pdk version = {pdk_version}")
        try:
            volare.enable(pdk_root=self.paths.pdk_root, pdk="sky130", version=pdk_version)
        except Exception as e:
            raise RuntimeError(f"Error occurred while downloading pdk: {e}")

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

        try:
            subprocess.run(clone_command, check=True)
            if commit:
                self.checkout_commit(target_dir, commit)
        except Exception as e:
            raise RuntimeError(f"Error occurred while cloning repo: {e}")

    def checkout_commit(self, repo_dir, commit):
        subprocess.run(["git", "checkout", commit], cwd=repo_dir, check=True)

