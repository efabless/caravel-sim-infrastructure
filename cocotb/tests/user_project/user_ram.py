import random
import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *

from interfaces.caravel import GPIO_MODE

reg = Regs()


@cocotb.test()
@repot_test
async def user_ram(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1167331)
    cocotb.log.info(f"[TEST] Start user RAM word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    await wait_configure(caravelEnv)
    while True:
        if caravelEnv.monitor_gpio((31, 0)).integer == 0xFF:  # test finish
            break
        if reg1 != caravelEnv.monitor_gpio((31, 0)).integer:
            reg1 = caravelEnv.monitor_gpio((31, 0)).integer
            if reg1 in pass_list:  # pass phase
                cocotb.log.info(f"[TEST] pass writing and reading all dff2 memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(f"[TEST] failed access address")
                break
        await ClockCycles(caravelEnv.clk, 1000)


async def wait_configure(caravelEnv):
    serial_load = caravelEnv.caravel_hdl.housekeeping.serial_load
    while True:
        if serial_load.value:
            cocotb.log.info(f"serial load is asserted serial_load = {serial_load}")
            break
        await ClockCycles(caravelEnv.clk, 1)
    await ClockCycles(caravelEnv.clk, 10)
    await caravelEnv.release_csb()
    await ClockCycles(caravelEnv.clk, 10)
