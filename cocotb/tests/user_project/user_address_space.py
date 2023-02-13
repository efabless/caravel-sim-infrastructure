import random
import cocotb
from cocotb.triggers import FallingEdge,RisingEdge,ClockCycles,Timer,Edge
import cocotb.log
from interfaces.cpu import RiskV
from interfaces.defsParser import Regs
from cocotb.result import TestSuccess
from tests.common_functions.test_functions import *

from interfaces.caravel import GPIO_MODE
from interfaces.common import Macros


reg = Regs()


@cocotb.test()
@repot_test
async def user_address_space(dut):
    caravelEnv,clock = await test_configure(dut,timeout_cycles=11117936)
    cocotb.log.info(f"[TEST] Start user_address_space test")
    ack_hdl   = caravelEnv.caravel_hdl.mprj.addr_space_testing.wbs_ack_o 
    addr_hdl  = caravelEnv.caravel_hdl.mprj.addr_space_testing.addr 
    data_hdl  = caravelEnv.caravel_hdl.mprj.addr_space_testing.data 
    start_addr= Macros["USER_SPACE_ADDR"]
    print(f"user space adddress = {start_addr}")
    user_size = Macros["USER_SPACE_SIZE"]
    addr_arr = (start_addr,start_addr+4,start_addr+8,start_addr +user_size -8,start_addr +user_size -4,start_addr +user_size,start_addr+0x72C,start_addr+0x41198,start_addr+0x7770,start_addr + 0x9F44,start_addr + 0x58,start_addr + 0x3602EC,start_addr + user_size)
    data_arr = (0x97cf0d2d,0xbc748313,0xbfda8146,0x5f5e36b1,0x0c1fe9d9,0x6d12d2b8,0xdcd244d1,0x0da37088,0x7b8e4345,0x00000777,0x00000777,0x00000777,0xFFFFFFFF)
    print([hex(i) for i in addr_arr])
    for addr, data in zip(addr_arr, data_arr):
        await RisingEdge(ack_hdl)
        if addr_hdl.value.integer != addr:
            cocotb.log.error(f"[TEST] seeing unexpected address {hex(addr_hdl.value.integer)} expected {hex(addr)}")
        elif data_hdl.value.integer !=  data:
            cocotb.log.error(f"[TEST] seeing unexpected data {hex(data_hdl.value.integer)} expected {hex(data)} address {hex(addr)}")
        else: 
            cocotb.log.info(f"[TEST] seeing the correct data {hex(data)} from address {hex(addr)}")


