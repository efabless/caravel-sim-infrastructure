Overview
========
This project aims to provide a user friendly environment for adding and running cocotb tests for Caravel user projects.


Prerequisites
=============================

* Docker: [Linux](https://hub.docker.com/search?q=&type=edition&offering=community&operating_system=linux&utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) ||  [Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) || [Mac with Intel Chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) || [Mac with M1 Chip](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) 
<!-- start configure the repo include0 -->
* Python 3.6+ with PIP
* ```docker pull efabless/dv:cocotb```
* Clone of caravel 
* Clone of caravel managment repo
* Clone of PDK from volare
* Clone of caravel user project 
<!-- end configure the repo include0 -->


Configure the repo
===================

<!-- start configure the repo include1 -->

Fill the ``design_info.yaml`` file with repos used as following:
<!-- end configure the repo include1 -->

```yaml <!-- start configure the repo include2 -->

  #yaml file contain general design information that would mostly need to be updated in the first run only 
  #eg CARAVEL_ROOT: "/usr/Desktop/caravel_project/caravel/" 
  #like repo https://github.com/efabless/caravel
  CARAVEL_ROOT: "/usr/caravel_project/caravel/"

  #eg MCW_ROOT: "/usr/Desktop/caravel_project/caravel_mgmt_soc_litex/" 
  #like repo https://github.com/efabless/caravel_mgmt_soc_litex 
  # MCW_ROOT: "/home/rady/caravel/swift/swift2"
  MCW_ROOT: "/usr/caravel_project/caravel_mgmt_soc_litex/"

  #eg USER_PROJECT_ROOT: "/usr/Desktop/caravel_project/caravel_user_project/" 
  #like repo https://github.com/efabless/caravel_user_project
  USER_PROJECT_ROOT: "/usr/caravel_project/"

  #eg PDK_ROOT: "/usr/Desktop/caravel_project/pdk/" 
  #exported by volare
  PDK_ROOT: "/usr/pdk"

  #eg PDK: "sky130A"
  PDK: sky130A
  #PDK: gf180mcuC

  #clock in ns
  clk: 25  

  # true when caravan are simulated instead of caravel
  caravan: false

  # optional email address to send the results to 
  emailto: [None,example@efabless.com]
```
<!-- end configure the repo include2 -->
Creating a Test
=================

Refer to [creating a test](docs/build/html/_sources/usage.rst.txt#creating-a-test) for where and how to create a test 

Refer to [cocotb based APIs](docs/build/html/python_api.html) for APIs to monitor or drive the hardware

Refer to [firmware APIs](docs/build/html/C_api.html) for APIs for firmware

# Test Examples

Refer to this [directory](https://github.com/efabless/caravel_user_project/tree/cocotb_dev/verilog/dv/cocotb) for tests example generated for 16bit counter


Creating a Testlist
=================

Refer to [creating a testlist](docs/build/html/_sources/usage.rst.txt#creating-a-testlist) for where and how to create a test 


run a test  
=============================

<!-- start run a test include1 -->
Tests can run individually or as a test group using ``testlist``. Test can also run in RTL, GL or SDF sims with 8 different coreners.

To a test use run script verify_cocotb: 
<!-- end run a test include1 -->



```bash <!-- start run a test include2 -->
usage: verify_cocotb.py [-h] [-regression REGRESSION] [-test TEST [TEST ...]]
                        [-sim SIM [SIM ...]]
                        [-testlist TESTLIST [TESTLIST ...]] [-tag TAG]
                        [-maxerr MAXERR] [-vcs] [-cov] [-checkers_en]
                        [-corner CORNER [CORNER ...]] [-zip_passed]
                        [-emailto EMAILTO [EMAILTO ...]] [-seed SEED]
                        [-no_wave] [-sdf_setup] [-clk CLK] [-lint] [-arm]
                        [-macros MACROS [MACROS ...]] [-sim_path SIM_PATH]

Run caravel cocotb tests

Arguments:
  -h, --help            show this help message and exit
  -test TEST [TEST ...], -t TEST [TEST ...]
                        name of test if no --sim provided RTL will be run
                        <takes list as input>
  -sim SIM [SIM ...]    Simulation type to be run RTL,GL&GL_SDF provided only
                        when run -test <takes list as input>
  -testlist TESTLIST [TESTLIST ...], -tl TESTLIST [TESTLIST ...]
                        path of testlist to be run
  -tag TAG              provide tag of the run default would be regression
                        name and if no regression is provided would be
                        run_<random float>_<timestamp>_
  -maxerr MAXERR        max number of errors for every test before simulation
                        breaks default = 3
  -vcs, -v              use vcs as compiler if not used iverilog would be used
  -corner CORNER [CORNER ...], -c CORNER [CORNER ...]
                        Corner type in case of GL_SDF run has to be provided
  -zip_passed           zip the waves and logs of passed tests. by default if
                        the run has more than 7 tests pass tests results would
                        be zipped automatically
  -emailto EMAILTO [EMAILTO ...], -mail EMAILTO [EMAILTO ...]
                        mails to send results to when results finish
  -seed SEED            run with specific seed
  -no_wave              disable dumping waves
  -clk CLK              define the clock period in ns default defined at
                        design_info.yaml
  -lint                 generate lint log -v must be used
  -macros MACROS [MACROS ...]
                        Add addtional verilog macros for the design
  -sim_path SIM_PATH    directory where simulation result directory "sim"
                        would be created if None it would be created under
                        cocotb folder                    
```
<!-- end run a test include2 -->


Example 
-----------
<!-- start run a test include3 -->
#### Run one test in RTL


```python3 verify_cocotb.py -t <testname> -tag run_one_test```

#### Run 2 tests in GL


```python3 verify_cocotb.py -t <test1> <test2>  -sim GL```

#### Run testlist

``` python3 verify_cocotb.py -tl <path to testlist> -tag all_rtl ```

<!-- end run a test include3 -->

Results 
===============
<!-- start result include1 -->

New directory named ``sim`` would be created under ``<repo root>/cocotb/`` or to the path passed to ``-sim_path`` and it will have all the results. 
<!-- end result include1 -->


```bash <!-- start result include2 -->

| sim #  directory get generate when run a test
│ ├── <tag> # tag of the run  
│ │   ├── <sim type>-<test name> # test result directory contain all logs and wave related to the test
│ │   │   └── <test name>.hex  # hex file used in running this test
│ │   │   └── <test name>.log  # log file generated from cocotb 
│ │   │   └── full.log         # log file has all the command and warning happened if C compilation error happened this file will contain the error msg 
│ │   │   └── <test name>.vcd  # waves can be opened by gtkwave
│ │   │   └── rerun.py         # script to rerun the test
│ │   └── command.log    # command use for this run 
│ │   └── repos_info.log # contain information about the repos used to run these tests 
│ │   └── configs.yaml   # contain information about the repos used to run these tests 
│ │   └── runs.log       # contains status of the run fails and passes tests 
│ ├── hex_files # directory contain all the generated hex files for the runs   
│ 
│ 
``` 
<!-- end result include2 -->

