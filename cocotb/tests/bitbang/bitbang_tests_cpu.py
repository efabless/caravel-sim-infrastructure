import random
import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *
from interfaces.caravel import GPIO_MODE
from interfaces.common import Macros
from tests.gpio.gpio_seq import *
from tests.common_functions.bitbang import bb_configure_all_gpios
from tests.housekeeping.housekeeping_spi.spi_access_functions import *

reg = Regs()


@cocotb.test()
@repot_test
async def bitbang_cpu_all_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1111437008)
    await gpio_all_o_seq(dut, caravelEnv)


@cocotb.test()
@repot_test
async def bitbang_cpu_all_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2835898)
    await gpio_all_i_seq(dut, caravelEnv)


"""Testbench of GPIO configuration through bit-bang method using the housekeeping SPI configure all gpio as output."""


@cocotb.test()
@repot_test
async def bitbang_spi_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1802769)
    await gpio_all_o_seq(dut, caravelEnv, bitbang_spi_o_configure)


"""Testbench of GPIO configuration through bit-bang method using the housekeeping SPI configure all gpio as input."""


@cocotb.test()
@repot_test
async def bitbang_spi_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=295585)
    await gpio_all_i_seq(dut, caravelEnv, bitbang_spi_i_configure)


async def bitbang_spi_i_configure(caravelEnv, cpu):
    await bb_configure_all_gpios(
        GPIO_MODE.GPIO_MODE_MGMT_STD_INPUT_NOPULL.value, caravelEnv
    )

    # disable Housekeeping SPI
    await write_reg_spi(caravelEnv, 0x6F, 0x1)
    await ClockCycles(caravelEnv.clk, 1)
    cpu.write_debug_reg2_backdoor(0xDD)


async def bitbang_spi_o_configure(caravelEnv, cpu):
    await bb_configure_all_gpios(GPIO_MODE.GPIO_MODE_MGMT_STD_OUTPUT.value, caravelEnv)
    cpu.write_debug_reg2_backdoor(0xDD)
