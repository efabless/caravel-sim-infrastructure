# Overview
<!-- start read me file -->
This project aims to provide a user friendly environment for adding and running cocotb tests for Caravel user projects.


# Prerequisites

<!-- start configure the repo include0 -->

* Docker: [Linux](https://hub.docker.com/search?q=&type=edition&offering=community&operating_system=linux&utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) ||  [Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) || [Mac with Intel Chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) || [Mac with M1 Chip](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header) 
* Python 3.6+ with PIP
* ```docker pull efabless/dv:cocotb```
* Clone of Caravel 
* Clone of Caravel management repo
* Clone of PDK from [volare](https://github.com/efabless/volare)
* Clone of Caravel user project 
<!-- end configure the repo include0 -->


# caravel_cocotb

## How to install caravel_cocotb

```bash
 pip install caravel-cocotb
```

or to install from repo
```bash
   git clone git@github.com:efabless/caravel-sim-infrastructure.git
   git checkout <release>
   cd caravel-sim-infrastructure/cocotb
   pip install .
   cd ../..
```

## caravel_cocotb usage
 
caravel_cocotb provides a flow and APIs to run simulation on user_project after integerated with caravel. This is so helpful in detecting any bug in the connection between the user project and Caravel IOs, wishbone interface or logic analyzers. Also since it's easy to add and run tests with this flow it can be used to test the whole user project.
<!-- middle read me file -->

# Creating a Test

<!-- start create a test include1 -->
## Requirements
 
   - install [cocotb_caravel](#how-to-install-caravel_cocotb) 
   - update netlist for RTL and GL files at ```<caravel_user_project>/verilog/includes/``` with the design netlist
   - update the [design_info](#update-design_infoyaml) file at ```<caravel_user_project>/verilog/dv/cocotb/design_info.yaml```

## Adding a test

This section explains the steps needed to create a test.

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
| │   └── design_info.yaml
| 
```
> **Note**: The name of ``C`` file must match the name of ``cocotb`` test function

### Python Template

The template for ``python`` test:

```python

   from caravel_cocotb.caravel_interfaces import test_configure
   from caravel_cocotb.caravel_interfaces import report_test
   from caravel_cocotb.caravel_interfaces import UART
   from caravel_cocotb.caravel_interfaces import SPI
   import cocotb

   @cocotb.test() # decorator to mark the test function as cocotb test
   @report_test # wrapper for configure test reporting files
   async def <test_name>(dut):
      caravelEnv = await test_configure(dut) #configure, start up and reset Caravel

      ######################## add test sequence ###################### 

```
<!-- end create a test include1 -->

Commonly used APIs to monitor or drive the hardware can be found in [`python_api`](docs/build/html/python_api.html)

<!-- start create a test include2 -->

> ! **Warning:** New test python function should be imported into cocotb_tests.py 

```python
  from <new_test>.<new_test> import <new_test>
```
### C Template

The template for Code test:

```C++

   #include <firmware_apis.h> // include required APIs 
   void main(){
      //////////////////////add test here////////////////////// 
      return;
   }
```
<!-- end create a test include2 -->

Commonly used APIs for firmware can be found in [`C_api`](docs/build/html/C_api.html)


<!-- start create a test include3 -->
# Test Examples

Refer to this [directory](https://github.com/efabless/caravel_user_project/tree/main/verilog/dv/cocotb) for tests example generated for 16-bit counter
<!-- end create a test include3 -->


# Creating a Testlist

Refer to [creating a testlist](docs/build/html/_sources/usage.rst.txt#creating-a-testlist) for where and how to create a test 


# run a test  

<!-- start run a test include -->
Tests can run individually or as a test group using ``testlist``. Tests can also run in RTL, GL or SDF sims with 9 different corners.

To run use caravel_cocotb in the location that has the design_info.yaml file or pass the path to the design_info.yaml file as a command -design_info: 



```bash 
usage: caravel_cocotb [-h] [-test TEST [TEST ...]] [-design_info DESIGN_INFO]
                      [-sim SIM [SIM ...]] [-testlist TESTLIST [TESTLIST ...]]
                      [-tag TAG] [-maxerr MAXERR] [-vcs]
                      [-corner CORNER [CORNER ...]] [-zip_passed]
                      [-emailto EMAILTO [EMAILTO ...]] [-seed SEED] [-no_wave]
                      [-sdf_setup] [-clk CLK] [-lint]
                      [-macros MACROS [MACROS ...]] [-sim_path SIM_PATH]
                      [-verbosity VERBOSITY] [-check_commits]
                      [-no_docker] [-compile]

Run cocotb tests

optional arguments:
  -h, --help            show this help message and exit
  -test TEST [TEST ...], -t TEST [TEST ...]
                        name of test or tests.if no --sim provided RTL will be
                        run <takes list as input>
  -design_info DESIGN_INFO, -di DESIGN_INFO
                        path to design_info.yaml file
  -sim SIM [SIM ...]    Simulation type RTL,GL & GL_SDF provided only when run
                        -test<takes list as input>
  -testlist TESTLIST [TESTLIST ...], -tl TESTLIST [TESTLIST ...]
                        path of testlist to be run
  -tag TAG              provide tag of the run default would be regression
                        name and if no regression is provided would be
                        run_<random float>_<timestamp>_
  -maxerr MAXERR        max number of errors for every test before simulation
                        breaks default = 3
  -vcs, -v              use VCS as compiler if not used iverilog would be used
  -corner CORNER [CORNER ...], -c CORNER [CORNER ...]
                        Corner type in case of GL_SDF run has to be provided
  -zip_passed           zip the waves and logs of passed tests. by default if
                        the run has more than 7 tests pass tests results would
                        be zipped automatically
  -emailto EMAILTO [EMAILTO ...], -mail EMAILTO [EMAILTO ...]
                        mails to send results to when results finish
  -seed SEED            run with specific seed
  -no_wave              disable dumping waves
  -sdf_setup            targeting setup violations by taking the SDF maximum
                        values
  -clk CLK              define the clock period in ns default defined at
                        design_info.yaml
  -lint                 generate lint log VCS must be used
  -macros MACROS [MACROS ...]
                        Add additional verilog macros for the design
  -sim_path SIM_PATH    directory where simulation result directory "sim"
                        would be created if None it would be created under
                        cocotb folder
  -verbosity VERBOSITY  verbosity of the console output it can have one of 3
                        value debug, normal or quiet the default value is
                        normal
  -check_commits        use to check if repos are up to date
  -no_docker            run iverilog without docker
  -compile              force recompilation
  -no_gen_defaults      dont run gen_gpio_defaults script
  --version             show program's version number and exit
```
<!-- end run a test include -->


## Example 

<!-- start run a test include3 -->
#### Run one test in RTL

```caravel_cocotb -t <testname> -tag run_one_test```

#### Run 2 tests in GL

```caravel_cocotb -t <test1> <test2>  -sim GL```

#### Run testlist

``` caravel_cocotb -tl <path to testlist> -tag all_rtl ```

<!-- end run a test include3 -->

# Creating a Testlist

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

# Results 
<!-- start result include -->

New directory named ``sim`` would be created under ``<repo root>/cocotb/`` or to the path passed to ``-sim_path`` and it will have all the results. 


```bash 

| sim #  directory get generate when run a test
│ ├── <tag> # tag of the run  
│ │   ├── compilation # directory contain all logs and build files related to the RTL compilation
│ │   │   └── compilation.log  # log file has all the commands used to run iverilog and any compilation error or warning
│ │   ├── <sim type>-<test name> # test result directory contain all logs and wave related to the test
│ │   │   └── firmware.hex  # hex file used in running this test
│ │   │   └── <test name>.log  # log file generated from cocotb 
│ │   │   └── firmware.log     # log file has all the commands used to compile the C code and any compilation error or warning
│ │   │   └── waves.vcd  # waves can be opened by gtkwave
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

# Update design_info.yaml 
<!-- start Update design_info include -->

> **Note**: This step is required only if make setup isn't used after cloning <caravel_user_project> 

> After any change `make setup-cocotb` can be used.

``design_info.yaml`` are used to reference all the needed repos and paths needed to run the tests:

fill  it like the following
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

  # true when caravan are simulated instead of Caravel
  caravan: false

  # optional email address to send the results to 
  emailto: [None]
```

<!-- end Update design_info include -->

# HDL include files format 
<!-- start Update include files format include -->
Include files from ``<caravel_user_project>/verilog/include`` like  ``includes.rtl.caravel_user_project``, ``includes.gl.caravel_user_project`` and ``includes.sdf.caravel_user_project`` are used to reference all the needed repos and paths needed to run the tests:

The legacy format to reference files is:
- support verilog file include
   ```bash
   -v $(USER_PROJECT_VERILOG)/rtl/user_project_wrapper.v
   ```

Coctb flow supports this format in addition to other formats:
- support systemVerilg file include
   ```bash
   -sv  $(USER_PROJECT_VERILOG)/rtl/counter.sv
   ```
- support wild card use
   ```bash
   -sv $(USER_PROJECT_VERILOG)/rtl/peripherals/*.sv
   ```
- support add search path for `.vh` and `.svh` files
   ```bash
   -I $(USER_PROJECT_VERILOG)/rtl/peripherals
   ```

<!-- end Update include files format include -->

# Unexisted python modules 
<!-- start unexisted python modules include -->
If the testbench use python modules that are not installed in the docker image, there are 2 options: 

1. use `-no_docker` option to run without docker if you have all the required tools installed.
2. Add requirments file to `<caravel_user_project>/verilog/dv/cocotb/requirements.txt` 
   ```txt
   rich==12.0.1
   ```
<!-- end unexisted python modules include -->
