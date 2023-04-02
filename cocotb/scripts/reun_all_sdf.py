import subprocess
from datetime import datetime
import time

test_list = "/home/rady/caravel/tests/Caravel_cocotb_tests/verilog/dv/cocotb/regression/all_sdf_sky130.yaml"
low = "high"
corners = ["nom-t", "min-t", "max-t", "nom-f", "min-f", "max-f", "nom-s", "min-s", "max-s"]
sim_path = "/home/rady/caravel/sims/caravel/second_sdf"
commands = []
for corner in corners:
    commands.append(f"python3 verify_cocotb.py -tl {test_list} -sim GL_SDF -vcs  -no_wave -tag run_sdf_{corner}_25ns_{low}_{datetime.now().strftime('%d_%b_%H_%M_%S_%f')[:-4]} -sdf_setup -corner {corner} -sim_path {sim_path}")


# create a list to store the subprocess objects
procs = []

# run each command asynchronously
for cmd in commands:
    proc = subprocess.Popen(cmd, shell=True)
    procs.append(proc)
    time.sleep(3)


# wait for all processes to finish
for proc in procs:
    proc.wait()
