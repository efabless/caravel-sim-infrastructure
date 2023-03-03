from curses import baudrate
import random
import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles, Timer, Edge
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *

from interfaces.caravel import GPIO_MODE
from interfaces.common import Macros
from interfaces.UART import UART

reg = Regs()


@cocotb.test()
@repot_test
async def uart_tx(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=407193)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start uart test")
    expected_msg = "Monitor: Test UART (RTL) passed"
    uart = UART(caravelEnv)
    # wait for start of sending
    await wait_reg1(cpu, caravelEnv, 0xAA)
    msg = await uart.get_line()
    if msg == expected_msg:
        cocotb.log.info(f"[TEST] Pass recieve the full expected msg '{msg}'")
    else:
        cocotb.log.error(
            f"[TEST] recieved wrong msg from uart msg recieved:'{msg}' expected '{expected_msg}'"
        )


@cocotb.test()
@repot_test
async def uart_rx(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=154409)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    uart = UART(caravelEnv)
    cocotb.log.info(f"[TEST] Start uart test")
    # IO[0] affects the uart selecting btw system and debug
    caravelEnv.drive_gpio_in((0, 0), 0)
    caravelEnv.drive_gpio_in((5, 5), 1)
    # send first char
    await wait_reg1(cpu, caravelEnv, 0xAA)
    await uart.uart_send_char("B")
    await uart_check_char_recieved(caravelEnv, cpu)
    # send second char
    await wait_reg1(cpu, caravelEnv, 0xBB)
    await uart.uart_send_char("M")
    await uart_check_char_recieved(caravelEnv, cpu)
    # send third char
    await wait_reg1(cpu, caravelEnv, 0xCC)
    await uart.uart_send_char("A")
    await uart_check_char_recieved(caravelEnv, cpu)


async def uart_check_char_recieved(caravelEnv, cpu):
    # check cpu recieved the correct character
    while True:
        if not Macros["GL"]:
            if Macros["ARM"]:
                reg_uart_data = (
                    caravelEnv.caravel_hdl.soc.core.AHB.APB_S3.S3_UART.reg_rx_buf.value.binstr
                )
            else:
                reg_uart_data = caravelEnv.caravel_hdl.soc.core.uart_rxtx_w.value.binstr
        else:
            reg_uart_data = "1001110"

        reg2 = cpu.read_debug_reg2()
        cocotb.log.debug(f"[TEST] reg2 = {hex(reg2)}")
        if reg2 == 0x1B:
            cocotb.log.info(
                f"[TEST] Pass cpu has recieved the correct character {chr(int(reg_uart_data,2))}({reg_uart_data})"
            )
            return
        if reg2 == 0x1E:
            cocotb.log.error(
                f"[TEST] Failed cpu has recieved the wrong character {chr(int(reg_uart_data,2))}({reg_uart_data})"
            )
            return

        await ClockCycles(caravelEnv.clk, 1)


@cocotb.test()
@repot_test
async def uart_loopback(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=199023)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start uart test")
    await cocotb.start(connect_5_6(dut, caravelEnv))  # short gpio 6 and 5
    caravelEnv.drive_gpio_in(
        (0, 0), 0
    )  # IO[0] affects the uart selecting btw system and debug

    # setup watcher loopback results
    await cocotb.start(uart_check_char_recieved_loopback(caravelEnv, cpu))

    await ClockCycles(caravelEnv.clk, 197000)


async def connect_5_6(dut, caravelEnv):
    while True:
        caravelEnv.drive_gpio_in(5, dut.bin6_monitor.value)
        await Edge(dut.bin6_monitor)


async def uart_check_char_recieved_loopback(caravelEnv, cpu):
    # check cpu recieved the correct character
    while True:
        if not Macros["GL"]:
            if Macros["ARM"]:
                reg_uart_data = (
                    caravelEnv.caravel_hdl.soc.core.AHB.APB_S3.S3_UART.reg_rx_buf.value.binstr
                )
            else:
                reg_uart_data = caravelEnv.caravel_hdl.soc.core.uart_rxtx_w.value.binstr
        else:
            reg_uart_data = "1001110"

        reg2 = cpu.read_debug_reg2()
        cocotb.log.debug(f"[TEST] reg2 = {hex(reg2)}")
        if reg2 == 0x1B:
            cocotb.log.info(
                f"[TEST] Pass cpu has sent and recieved the correct character {chr(int(reg_uart_data,2))}"
            )
            await wait_reg2(cpu, caravelEnv, 0)

        if reg2 == 0x1E:
            cocotb.log.error(
                f"[TEST] Failed cpu has sent and recieved the wrong character {chr(int(reg_uart_data,2))}"
            )
            await wait_reg2(cpu, caravelEnv, 0)

        await ClockCycles(caravelEnv.clk, 1)
