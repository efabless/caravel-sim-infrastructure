import random
import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,ClockCycles,Timer
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *
from tests.bitbang.bitbang_functions import *
from interfaces.caravel import GPIO_MODE
from cocotb.binary import BinaryValue
from interfaces.common import sky
from tests.common_functions.Timeout import Timeout
from tests.housekeeping.housekeeping_spi.spi_access_functions import *

reg = Regs()
config_file = f"sim.{os.getenv('RUNTAG')}.configs"
clk = import_module(config_file).clock

@cocotb.test()
@repot_test
async def PoR(dut):
    # configurations
    caravelEnv = caravel.Caravel_env(dut)
    Timeout(clk=caravelEnv.clk,cycle_num=185972,precision=0.2)
    cocotb.scheduler.add(max_num_error(10,caravelEnv.clk))
    clock = Clock(caravelEnv.clk, clk, units="ns")  # Create a 25ns period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock
    # drive reset with 1 
    await caravelEnv.power_up()
    await caravelEnv.disable_csb() # 
    caravelEnv.dut.resetb_tb.value = BinaryValue(value = 1, n_bits =1)
    await Timer(530, "ns")
    # await caravelEnv.reset() # 
    await caravelEnv.disable_bins()
    common.fill_macros(caravelEnv.dut.macros) # get macros value
    coverage = Macros['COVERAGE']
    checker = Macros['CHECKERS']

    # start test
    cpu = RiskV(dut)
    cocotb.log.info(f"[TEST] Start mgmt_gpio_bidir but depending on PoR test")  
    await wait_reg1(cpu,caravelEnv,0XAA)
    num_blinks = random.randint(1, 20)
    cocotb.log.info (f"[TEST] start send {num_blinks} blinks")
    for i in range(num_blinks):
        if i == num_blinks-1: #last iteration
            # await cpu.drive_data2address(reg.get_addr('reg_debug_1'),0xFF)
            cpu.write_debug_reg1_backdoor(0xFF) 
        caravelEnv.drive_mgmt_gpio(1)
        await ClockCycles(caravelEnv.clk,3000) 
        caravelEnv.drive_mgmt_gpio(0)
        await ClockCycles(caravelEnv.clk,3000) 
    cocotb.log.info(f"[TEST] finish sending {num_blinks} blinks ")

    cocotb.log.info(f"[TEST] waiting for {num_blinks} blinks ")
    recieved_blinks = 0
    while True:
        if cpu.read_debug_reg2() == 0xFF:  #test finish
            break
        while (True):
            if caravelEnv.monitor_mgmt_gpio() == '0': 
                break
            if cpu.read_debug_reg2() == 0xFF:  #test finish
                break
            await ClockCycles(caravelEnv.clk,10) 
        while (True):
            if caravelEnv.monitor_mgmt_gpio() == '1': 
                recieved_blinks +=1
                break
            if cpu.read_debug_reg2() == 0xFF:  #test finish
                break
            await ClockCycles(caravelEnv.clk,10) 
        await ClockCycles(caravelEnv.clk,1) 
        

    if recieved_blinks == num_blinks:
        cocotb.log.info(f"[TEST] recieved the correct number of blinks {num_blinks}")
    else: 
        cocotb.log.error(f"[TEST] recieved the incorrect number of blinks recieved = {recieved_blinks} expected = {num_blinks}")
