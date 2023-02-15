import random
import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,ClockCycles,Timer
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *

from interfaces.caravel import GPIO_MODE
from cocotb.binary import BinaryValue
from interfaces.common import sky
from tests.common_functions.Timeout import Timeout
from tests.housekeeping.housekeeping_spi.spi_access_functions import *
from tests.mgmt_gpio.mgmt_gpio import blink_counter

@cocotb.test()
@repot_test
async def PoR(dut):
    # configurations
    caravelEnv = caravel.Caravel_env(dut)
    Timeout(clk=caravelEnv.clk,cycle_num=18223191,precision=0.2)
    cocotb.scheduler.add(max_num_error(10,caravelEnv.clk))
    clock = Clock(caravelEnv.clk, read_config_file()["clock"], units="ns")  # Create a 25ns period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock
    # drive reset with 1 
    await caravelEnv.disable_csb() # 
    caravelEnv.dut.resetb_tb.value = BinaryValue(value = 1, n_bits =1)
    await caravelEnv.power_up()
    await Timer(530, "ns")
    # await caravelEnv.reset() # 
    await caravelEnv.disable_bins()
    common.fill_macros(caravelEnv.dut.macros) # get macros value
    coverage = Macros['COVERAGE']
    checker = Macros['CHECKERS']

    # start test
    cpu = RiskV(dut)
    cocotb.log.info(f"[TEST] Start mgmt_gpio_bidir test")  

    await wait_reg1(cpu,caravelEnv,0XAA)
    num_blinks = random.randint(1, 20)
    cocotb.log.info (f"[TEST] start send {num_blinks} blinks")
    for i in range(num_blinks):
        if i == num_blinks-1: #last iteration
            cpu.write_debug_reg1_backdoor(0xFF) 
        caravelEnv.drive_mgmt_gpio(1)
        await ClockCycles(caravelEnv.clk,30000) 
        caravelEnv.drive_mgmt_gpio(0)
        if i != num_blinks-1: # not last iteration
            await ClockCycles(caravelEnv.clk,30000) 
        else: 
            # caravelEnv.drive_mgmt_gpio('z')
            await ClockCycles(caravelEnv.clk,1) 

    # caravelEnv.drive_mgmt_gpio('z')
    cocotb.log.info(f"[TEST] finish sending {num_blinks} blinks ")

    cocotb.log.info(f"[TEST] waiting for {num_blinks} blinks ")
    counter = [0] # list to pass by ref
    await cocotb.start(blink_counter(caravelEnv.get_mgmt_gpi_hdl(),counter))  # forked
    await wait_reg2(cpu,caravelEnv,0xFF)
    recieved_blinks = counter[0]
    if recieved_blinks == num_blinks:
        cocotb.log.info(f"[TEST] recieved the correct number of blinks {num_blinks}")
    else: 
        cocotb.log.error(f"[TEST] recieved the incorrect number of blinks recieved = {recieved_blinks} expected = {num_blinks}")
    cocotb.log.info(f"[TEST] counter =  {counter}")
        

    if recieved_blinks == num_blinks:
        cocotb.log.info(f"[TEST] recieved the correct number of blinks {num_blinks}")
    else: 
        cocotb.log.error(f"[TEST] recieved the incorrect number of blinks recieved = {recieved_blinks} expected = {num_blinks}")