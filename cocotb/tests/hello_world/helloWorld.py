import cocotb
from tests.common_functions.test_functions import *


@cocotb.test()
@repot_test
async def helloWorld(dut):
    caravelEnv = await test_configure(dut)
    cocotb.log.info("[Test] Hello world")
    await ClockCycles(caravelEnv.clk, 100000)
