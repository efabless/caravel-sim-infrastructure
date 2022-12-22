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

async def gpio_all_i_seq(dut,timeout):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=timeout)
    from tests.common_functions.test_functions import active_gpios_num
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    caravelEnv.drive_gpio_in((active_gpios_num,0),0)
    await wait_reg1(cpu,caravelEnv,0xAA)
    cocotb.log.info(f"[TEST] configuration finished")
    data_in = 0xFFFFFFFF
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31,0),data_in)
    await wait_reg1(cpu,caravelEnv,0xBB)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datal has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0xAAAAAAAA
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31,0),data_in)
    await wait_reg1(cpu,caravelEnv,0xCC)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datal has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0x55555555
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31,0),data_in)
    await wait_reg1(cpu,caravelEnv,0xDD)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datal has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0x0
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31,0),data_in)
    await wait_reg1(cpu,caravelEnv,0xD1)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datal has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0x3f
    data_in = int(bin(data_in)[31-active_gpios_num:],2)
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num,32),data_in)
    await wait_reg1(cpu,caravelEnv,0xD2)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datah has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0x0
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num,32),data_in)
    await wait_reg1(cpu,caravelEnv,0xD3)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datah has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0x15
    data_in = int(bin(data_in)[31-active_gpios_num:],2)

    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num,32),data_in)
    await wait_reg1(cpu,caravelEnv,0xD4)
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datah has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    data_in = 0x2A
    data_in = int(bin(data_in)[31-active_gpios_num:],2)
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num,32),data_in) 
    await wait_reg1(cpu,caravelEnv,0XD5) 
    if cpu.read_debug_reg2() == data_in:
        cocotb.log.info(f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]")
    else: 
        cocotb.log.error(f"[TEST] Error: reg_mprj_datah has recieved wrong data {cpu.read_debug_reg2()} instead of {data_in}")
    caravelEnv.release_gpio((active_gpios_num,0))
    await wait_reg2(cpu,caravelEnv,0XFF) 
    if caravelEnv.monitor_gpio((active_gpios_num,0)).binstr != ''.join(['z'*(active_gpios_num+1)]):
        cocotb.log.error(f"[TEST] ERROR: firmware can write to the gpios while they are configured as input_nopull gpio= {caravelEnv.monitor_gpio((active_gpios_num,0))}")
    else:
        cocotb.log.info(f"[TEST] [TEST] PASS: firmware cannot write to the gpios while they are configured as input_nopull gpio= {caravelEnv.monitor_gpio((active_gpios_num,0))}")
    cocotb.log.info(f"[TEST] finish")

async def gpio_all_o_seq(dut,timeout):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=timeout)
    from tests.common_functions.test_functions import active_gpios_num
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    
    await wait_reg1(cpu,caravelEnv,0xAA)
    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] finish configuring as user output")
    i= 0x1 << (active_gpios_num-32)
    i_temp = i
    for j in range(active_gpios_num-32):
        await wait_reg2(cpu,caravelEnv,active_gpios_num-j)
        cocotb.log.info(f'[Test] gpio out = {caravelEnv.monitor_gpio((active_gpios_num,0))} j = {j}')
        if caravelEnv.monitor_gpio((active_gpios_num,0)).integer != i<<32:
            cocotb.log.error(f'[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((active_gpios_num,0))} instead of {bin(i<<32)}')
        cpu.write_debug_reg1_backdoor(0xD1) # finsh reading 1
        await wait_reg2(cpu,caravelEnv,0)
        if caravelEnv.monitor_gpio((active_gpios_num,0)).integer != 0:
            cocotb.log.error(f'[TEST] Wrong gpio output {caravelEnv.monitor_gpio((active_gpios_num,0))} instead of {bin(0x00000)}')
        cpu.write_debug_reg1_backdoor(0xD0) # finsh reading 0
        i = i >> 1
        i |= i_temp

    i= 0x80000000
    for j in range(32):
        await wait_reg2(cpu,caravelEnv,32-j)
        cocotb.log.info(f'[Test] gpio out = {caravelEnv.monitor_gpio((active_gpios_num,0))} j = {j}')
        high_gpio_val = 0x3f
        if  Macros['ARM']:
            high_gpio_val = 0x7 # with ARM the last 3 gpios are not configurable
        if caravelEnv.monitor_gpio((active_gpios_num,32)).integer != high_gpio_val:
            cocotb.log.error(f'[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((active_gpios_num,32))} instead of {bin(high_gpio_val)} ')
        if caravelEnv.monitor_gpio((31,0)).integer != i :
            cocotb.log.error(f'[TEST] Wrong gpio low bits output {caravelEnv.monitor_gpio((31,0))} instead of {bin(i)}')
        cpu.write_debug_reg1_backdoor(0xD1) # finsh reading 1
        await wait_reg2(cpu,caravelEnv,0)
        if caravelEnv.monitor_gpio((active_gpios_num,0)).integer != 0:
            cocotb.log.error(f'Wrong gpio output {caravelEnv.monitor_gpio((active_gpios_num,0))} instead of {bin(0x00000)}')
        cpu.write_debug_reg1_backdoor(0xD0) # finsh reading 0
        i = i >> 1
        i |= 0x80000000

    await wait_reg1(cpu,caravelEnv,0XFF)
    await ClockCycles(caravelEnv.clk, 10)

async def gpio_all_i_pd_seq(dut,timeout):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=timeout)
    from tests.common_functions.test_functions import active_gpios_num
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    uut = dut.uut
    await wait_reg1(cpu,caravelEnv,0xAA)
    await caravelEnv.release_csb()
    # monitor the output of padframe module it suppose to be all ones  when no input is applied
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "0":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and float")
    await ClockCycles(caravelEnv.clk,100) 
    # drive gpios with zero 
    data_in =  0x0
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "0":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with 0")
    await ClockCycles(caravelEnv.clk,100) 
    # drive gpios with ones 
    data_in =  0x3FFFFFFFFF
    data_in = int(bin(data_in)[-active_gpios_num-1:],2)
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "1":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pulldown and drived with 1")
    await ClockCycles(caravelEnv.clk,100) 
    # drive odd half gpios with zeros and float other half
    data_in =  0x0
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(0,38,2):
        caravelEnv.release_gpio(i) # release even gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i]!="0":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with odd half with 0")
       
    await ClockCycles(caravelEnv.clk,100) 
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(1,38,2):
        caravelEnv.release_gpio(i) # release odd gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i]!="0":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with even half with 0")
    await ClockCycles(caravelEnv.clk,100) 
    # drive odd half gpios with ones and float other half
    data_in =  0x3FFFFFFFFF
    data_in = int(bin(data_in)[-active_gpios_num-1:],2)
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(0,38,2):
        caravelEnv.release_gpio(i) # release even gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if i%2 ==0: #even
            if gpio[i]!="0":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pulldown and drived with odd half with 1")
        else:
            if gpio[i] != "1":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with odd half with 1")
    
    await ClockCycles(caravelEnv.clk,100) 
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(1,38,2):
        caravelEnv.release_gpio(i) # release odd gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if i%2 ==1: #odd
            if gpio[i]!="0":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pulldown and drived with odd half with 1")
        else:
            if gpio[i] != "1":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with odd half with 1")

    await ClockCycles(caravelEnv.clk,100) 

    # drive with ones then release all gpio
    data_in =  0x3FFFFFFFFF
    data_in = int(bin(data_in)[-active_gpios_num-1:],2)
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    await ClockCycles(caravelEnv.clk,100) 
    caravelEnv.release_gpio((active_gpios_num,0))
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "0":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and all released")
    await ClockCycles(caravelEnv.clk,100) 

async def gpio_all_i_pu_seq(dut,timeout):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=timeout)
    from tests.common_functions.test_functions import active_gpios_num
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    cpu.cpu_release_reset()
    uut = dut.uut
    await wait_reg1(cpu,caravelEnv,0xAA)
    await caravelEnv.release_csb()
    # monitor the output of padframe module it suppose to be all ones  when no input is applied
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "1":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {i} instead of 1 while configured as input pullup and float")
    await ClockCycles(caravelEnv.clk,100) 
    # drive gpios with zero 
    data_in =  0x0
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "0":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pullup and drived with 0")
    await ClockCycles(caravelEnv.clk,100) 
    # drive gpios with ones 
    data_in =  0x3FFFFFFFFF
    data_in = int(bin(data_in)[-active_gpios_num-1:],2)
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "1":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with 1")
    await ClockCycles(caravelEnv.clk,100) 
    # drive odd half gpios with zeros and float other half
    data_in =  0x0
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(0,active_gpios_num+1,2):
        caravelEnv.release_gpio(i) # release even gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if i%2 ==1: #odd
            if gpio[i]!="0":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with odd half with 0")
        else:
            if gpio[i] != "1":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pullup and drived with odd half with 0")
    await ClockCycles(caravelEnv.clk,100) 
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(1,active_gpios_num+1,2):
        caravelEnv.release_gpio(i) # release odd gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if i%2 ==1: #odd
            if gpio[i] != "1":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pullup and drived with even half with 0")
        else:
            if gpio[i]!="0":
                cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with even half with 0")
    await ClockCycles(caravelEnv.clk,100) 
    # drive odd half gpios with ones and float other half
    data_in =  0x3FFFFFFFFF
    data_in = int(bin(data_in)[-active_gpios_num-1:],2)
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(0,active_gpios_num+1,2):
        caravelEnv.release_gpio(i) # release even gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i]!="1":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with odd half with 1")
    
    await ClockCycles(caravelEnv.clk,100) 
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    for i in range(1,active_gpios_num+1,2):
        caravelEnv.release_gpio(i) # release odd gpios
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "1":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with even half with 1")
       
    await ClockCycles(caravelEnv.clk,100) 

    # drive with zeros then release all gpio
    data_in =  0x0
    caravelEnv.drive_gpio_in((active_gpios_num,0),data_in)
    await ClockCycles(caravelEnv.clk,100) 
    caravelEnv.release_gpio((active_gpios_num,0))
    await ClockCycles(caravelEnv.clk,100) 
    gpio = dut.uut.padframe.mprj_io_in.value.binstr[::-1]
    cocotb.log.info(f"mprj value seen = {gpio}")
    for i in range(active_gpios_num+1):
        if gpio[i] != "1":
            cocotb.log.error(f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and all released")
    await ClockCycles(caravelEnv.clk,100) 