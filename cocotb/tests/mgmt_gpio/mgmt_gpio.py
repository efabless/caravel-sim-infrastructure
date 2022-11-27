import random
import re
import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,ClockCycles
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *
from tests.bitbang.bitbang_functions import *
from interfaces.caravel import GPIO_MODE

reg = Regs()
"""Testbench of GPIO configuration through bit-bang method using the StriVe housekeeping SPI."""
@cocotb.test()
@repot_test
async def mgmt_gpio_out(dut):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=91385)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start mgmt_gpio_out test")  
    phases_fails = 3
    phases_passes = 0 
    reg1 =0 # buffer
    reg2 = 0 #buffer

    while True: 
        if reg2 != cpu.read_debug_reg2():
            reg2 = cpu.read_debug_reg2()
            if reg2 == 0xFF:  # test finish 
                break
        if reg1 != cpu.read_debug_reg1():
            reg1 = cpu.read_debug_reg1()                
            cocotb.log.info(f"[TEST] waiting for {reg1} blinks")
            for i in range(reg1): 
                while (True):
                    if caravelEnv.monitor_mgmt_gpio() == '0': 
                        break
                    if reg1 != cpu.read_debug_reg1(): 
                        cocotb.log.error("[TEST] error failing to catch all blinking ")
                        return
                    await ClockCycles(caravelEnv.clk,10) 

                while (True):
                    if caravelEnv.monitor_mgmt_gpio() == '1': 
                        break
                    if reg1 != cpu.read_debug_reg1(): 
                        cocotb.log.error("[TEST] error failing to catch all blinking ")
                        return
                    await ClockCycles(caravelEnv.clk,10) 
            cocotb.log.info(f"[TEST] passing sending {reg1} blinks ")
            phases_fails -=1
            phases_passes +=1
        await ClockCycles(caravelEnv.clk,10) 

    if phases_fails != 0:
        cocotb.log.error(f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails") 
    else:
        cocotb.log.info(f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails")     


@cocotb.test()
@repot_test
async def mgmt_gpio_in(dut):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=281094)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start mgmt_gpio_in test")  
    phases_fails = 3
    phases_passes = 0 
    pass_list = (0x1B,0x2B,0xFF)
    fail_list = tuple([0xEE])
    reg1 =0 # buffer
    reg2 = 0 #buffer

    while True: 
        if reg2 != cpu.read_debug_reg2():
            reg2 = cpu.read_debug_reg2()
            if reg2 in pass_list: 
                cocotb.log.info  (f"[TEST] reg2 = {reg2}")
                phases_passes +=1
                phases_fails  -=1
                if reg2 == 0xFF:  # test finish 
                    break
                elif reg2 == 0x1B:
                    cocotb.log.info(f"[TEST] pass sending 10 blink ")
                elif reg2 == 0x2B:
                    cocotb.log.info(f"[TEST] pass sending 20 blink ")
            if reg2 in fail_list: 
                cocotb.log.error(f"[TEST] gpio change without sending anything")
        if reg1 != cpu.read_debug_reg1():
            reg1 = cpu.read_debug_reg1()                
            cocotb.log.info(f"[TEST] start sending {reg1} blinks")
            for i in range(reg1): 
                caravelEnv.drive_mgmt_gpio(1)
                await wait_reg2(cpu,caravelEnv,0XAA)
                caravelEnv.drive_mgmt_gpio(0)
                await wait_reg2(cpu,caravelEnv,0XBB)
            cocotb.log.info(f"[TEST] finish sending {reg1} blinks ")
        await ClockCycles(caravelEnv.clk,10) 

    if phases_fails != 0:
        cocotb.log.error(f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails") 
    else:
        cocotb.log.info(f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails")     




@cocotb.test()
@repot_test
async def mgmt_gpio_bidir(dut):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=223191)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start mgmt_gpio_bidir test")  

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

@cocotb.test()
@repot_test
async def mgmt_gpio_pu_pd(dut):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=12477)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start mgmt_gpio_pu_pd test")  

    await wait_reg1(cpu,caravelEnv,0X1B)
    caravelEnv.drive_mgmt_gpio('z')
    await ClockCycles(caravelEnv.clk,1) 
    gpio_in = dut.uut.gpio_in_core
    if gpio_in.value.binstr != '1': 
        cocotb.log.error(f"[TEST] mgmt gpio pull up didn't work correctly reading {gpio_in} instead of 1")

    await wait_reg1(cpu,caravelEnv,0X2B)
    caravelEnv.drive_mgmt_gpio('z')
    await ClockCycles(caravelEnv.clk,1) 
    if gpio_in.value.binstr != '0': 
        cocotb.log.error(f"[TEST] mgmt gpio pull down didn't work correctly reading {gpio_in} instead of 0")

    await wait_reg1(cpu,caravelEnv,0X3B)
    caravelEnv.drive_mgmt_gpio('z')
    await ClockCycles(caravelEnv.clk,1) 
    if gpio_in.value.binstr != 'x': 
        cocotb.log.error(f"[TEST] mgmt gpio no pull didn't work correctly reading {gpio_in} instead of x")



@cocotb.test()
@repot_test
async def mgmt_gpio_disable(dut):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=25554)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    cocotb.log.info(f"[TEST] Start mgmt_gpio_pu_pd test")  
    phases_fails = 2
    phases_passes = 0 
    pass_list = (0x1B,0x2B)
    fail_list = (0x1E,0x2E)
    reg2 = 0 #buffer
    caravelEnv.drive_mgmt_gpio(1)
    
    while True: 
        if reg2 != cpu.read_debug_reg2():
            reg2 = cpu.read_debug_reg2()
            if reg2 == 0xFF:  # test finish 
                    break
            if reg2 in pass_list: 
                cocotb.log.info  (f"[TEST] pass = {hex(reg2)}")
                phases_passes +=1
                phases_fails  -=1
            if reg2 in fail_list: 
                cocotb.log.error(f"[TEST] fail = {hex(reg2)}")
        await ClockCycles(caravelEnv.clk,10) 
    caravelEnv.drive_mgmt_gpio('z')

    if phases_fails != 0:
        cocotb.log.error(f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails") 
    else:
        cocotb.log.info(f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails")     

    await wait_reg1(cpu,caravelEnv,0X1A)
    if caravelEnv.monitor_mgmt_gpio() != '1': 
        cocotb.log.error(f"[TEST] mgmt gpio output enable but output isn't working")
    
    await wait_reg1(cpu,caravelEnv,0X2A)
    if caravelEnv.monitor_mgmt_gpio() == '1': 
        cocotb.log.error(f"[TEST] mgmt gpio disabled but output is working")
        
        