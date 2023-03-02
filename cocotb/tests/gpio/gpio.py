import random
import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,ClockCycles
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *

from interfaces.caravel import GPIO_MODE
from cocotb.binary import BinaryValue
from tests.gpio.gpio_seq import *
reg = Regs()

@cocotb.test()
@repot_test
async def gpio_all_o(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=1829526)
    await gpio_all_o_seq(dut,caravelEnv)

@cocotb.test()
@repot_test
async def gpio_all_i(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=273525)
    await gpio_all_i_seq(dut,caravelEnv)

@cocotb.test()
@repot_test
async def gpio_all_i_pu(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=64179)
    await gpio_all_i_pu_seq(dut,caravelEnv)
    
@cocotb.test()
@repot_test
async def gpio_all_i_pd(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=64179)
    await gpio_all_i_pd_seq(dut,caravelEnv)
    