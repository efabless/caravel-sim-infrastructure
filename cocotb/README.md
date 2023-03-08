Overview
========
This project aims to provide a user friendly environment for adding and running cocotb tests for Caravel user projects.


Prerequisites
=============================
<!-- start configure the repo include0 -->

* Docker: [Linux](https://hub.docker.com/search?q=&type=edition&offering=community&operating_system=linux&utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) ||  [Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) || [Mac with Intel Chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) || [Mac with M1 Chip](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) 
* Python 3.6+ with PIP
* ```docker pull efabless/dv:cocotb```
* Clone of caravel 
* Clone of caravel managment repo
* Clone of PDK from volare
* Clone of caravel user project 
<!-- end configure the repo include0 -->


Configure the repo
===================

<!-- start configure the repo include-->

Fill the ``design_info.yaml`` file with repos used as following:

```yaml
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
> **Note**: This step is only when first clone the repo.

<!-- end configure the repo include -->
Creating a Test
=================

<!-- start create a test include1 -->

This section explains the the steps needed to create a test.

A typical test for *Caravel* consists of 2 parts: ``Python/cocotb`` code and ``C`` code. 

* ``Python/cocotb`` code is for communicating with *Caravel* hardware interface inputs, outputs, clock, reset, and power ports/bins. ``cocotb`` here replaces the ``verilog`` code.

* ``C`` code provides firmware code that would be loaded into the *Caravel* CPU.

Tests files has to located under ``<caravel_user_project>/verilog/dv/cocotb/`` 

```bash
| dv
| ├── cocotb
| │   ├── <new_test>
| │   │   └── <new_test.py>
| │   │   └── <new_test.c>
| │   └── cocotb_tests.py
| 
```
> **Note**: The name of ``C`` file must match the name of ``cocotb`` test function

Python Template
--------------------------

The template for ``python`` test:

```python

   from cocotb_includes import * # import python APIs 
   import cocotb

   @cocotb.test() # cocotb test marker
   @repot_test # wrapper for configure test reporting files
   async def <test_name>(dut):
      caravelEnv = await test_configure(dut) #configure, start up and reset caravel

      ######################## add test sequence ###################### 

```
<!-- end create a test include1 -->

Commonly used APIs to monitor or drive the hardware can be found in [`python_api`](docs/build/html/python_api.html)

<!-- start create a test include2 -->

> ! **Warning:** New test python function should be imported into cocotb_tests.py 

```python
  from <new_test>.<new_test> import <new_test>
```
C Template
----------------------

The template for Code test:

```C++

   #include <common.h> // include required APIs 
   void main(){
      //////////////////////add test here////////////////////// 
      return;
   }
```
<!-- end create a test include2 -->

Commonly used APIs for firmware can be found in [`C_api`](docs/build/html/C_api.html)


<!-- start create a test include3 -->
# Test Examples

Refer to this [directory](https://github.com/efabless/caravel_user_project/tree/cocotb_dev/verilog/dv/cocotb) for tests example generated for 16bit counter
<!-- end create a test include3 -->


Creating a Testlist
=================

Refer to [creating a testlist](docs/build/html/_sources/usage.rst.txt#creating-a-testlist) for where and how to create a test 


run a test  
=============================

<!-- start run a test include -->
Tests can run individually or as a test group using ``testlist``. Test can also run in RTL, GL or SDF sims with 8 different coreners.

To a test use run script verify_cocotb: 



```bash 
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
<!-- end run a test include -->


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

Creating a Testlist
==============================
<!-- start testlist include -->

Testlist is a file that contains a collection of test names to run together. 

The syntax is simple as ``YAML`` is used to write the testlist  

``` yaml

   # Testlist Can has only 2 elements Tests or includes 

   # Test element has list of dictionaries of tests to include 
   Tests: 
      - {name: <test1>, sim: RTL} 
      - {name: <test1>, sim: GL} 
      - {name: <test2>, sim: RTL} 

   # include has paths  for other testlist to include in this test list 
   # paths are relative to the location of this yaml file
   includes: 
      - <test4>/<testlist>.yaml
      - <testlist>.yaml
      - ../<test5>/<testlist>.yaml
```
<!-- end testlist include -->

Results 
===============
<!-- start result include -->

New directory named ``sim`` would be created under ``<repo root>/cocotb/`` or to the path passed to ``-sim_path`` and it will have all the results. 


```bash 

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
<!-- end result include -->

