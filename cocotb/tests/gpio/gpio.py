import random
import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,ClockCycles
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *
from tests.bitbang.bitbang_functions import *
from interfaces.caravel import GPIO_MODE
from cocotb.binary import BinaryValue
from tests.gpio.gpio_seq import *
reg = Regs()

@cocotb.test()
@repot_test
async def gpio_all_o(dut):
    await gpio_all_o_seq(dut,538624)

@cocotb.test()
@repot_test
async def gpio_all_i(dut):
    await gpio_all_i_seq(dut,56837)

@cocotb.test()
@repot_test
async def gpio_all_i_pu(dut):
    await gpio_all_i_pu_seq(dut,54138)
    
@cocotb.test()
@repot_test
async def gpio_all_i_pd(dut):
    await gpio_all_i_pd_seq(dut,54138)
    