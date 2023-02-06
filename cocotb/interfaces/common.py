from cocotb.handle import SimHandleBase
from cocotb.binary import BinaryValue
from enum import Enum
import cocotb
from importlib import import_module
import os
"""return the value and the size of the signal"""
def signal_value_size(path:SimHandleBase):
    value = path.value
    size  = value.n_bits
    return value, size
    
    
"""
Create a binaryValue object with all Z that helps when drive to drive only the bits needed
return value with all z and the size
"""
def signal_valueZ_size(path:SimHandleBase):
    value = path.value
    size  = value.n_bits
    value = BinaryValue(value = int(size) * 'z',n_bits=size)
    return value, size

def int_to_bin_list(number:bin,number_of_bits)-> list:
    data = bin(number)
    data = data[2:].zfill(number_of_bits)[::-1]
    bits = [int(bit) for bit in data]
    return bits

def drive_hdl(path,bits,data):
        hdl , n_bits = signal_value_size(path)
        is_list_of_lists  = all(isinstance(x, list) for x in bits)
        is_list_of_tuples  = all(isinstance(x, tuple) for x in bits)
        if is_list_of_lists | is_list_of_tuples: 
            for i,bits2 in enumerate(bits):
                hdl[n_bits-1-bits2[0]:n_bits-1-bits2[1]] = data[i]
        else:
            hdl[n_bits-1-bits[0]:n_bits-1-bits[1]] = data
        path.value = hdl
        cocotb.log.debug(f' [common] drive { path._path }  with {hdl}')   

"""Enum for GPIO modes valus used to configured the pins"""
tag = os.getenv('RUNTAG')
# config_file = f"sim.{tag.replace('/','.')}.configs" // TODO: fix this 
sky = 1
if 1:
    class GPIO_MODE(Enum):
        GPIO_MODE_MGMT_STD_INPUT_NOPULL    = 0x0403
        GPIO_MODE_MGMT_STD_INPUT_PULLDOWN  = 0x0c01
        GPIO_MODE_MGMT_STD_INPUT_PULLUP	   = 0x0801
        GPIO_MODE_MGMT_STD_OUTPUT	       = 0x1809
        GPIO_MODE_MGMT_STD_BIDIRECTIONAL   = 0x1801
        GPIO_MODE_MGMT_STD_ANALOG   	   = 0x000b
        GPIO_MODE_USER_STD_INPUT_NOPULL	   = 0x0402
        GPIO_MODE_USER_STD_INPUT_PULLDOWN  = 0x0c00
        GPIO_MODE_USER_STD_INPUT_PULLUP	   = 0x0800
        GPIO_MODE_USER_STD_OUTPUT	       = 0x1808
        GPIO_MODE_USER_STD_BIDIRECTIONAL   = 0x1800
        GPIO_MODE_USER_STD_OUT_MONITORED   = 0x1802
        GPIO_MODE_USER_STD_ANALOG   	   = 0x000a

else: 
    class GPIO_MODE(Enum):
        GPIO_MODE_MGMT_STD_INPUT_NOPULL    = 0x007
        GPIO_MODE_MGMT_STD_INPUT_PULLDOWN  = 0x047
        GPIO_MODE_MGMT_STD_INPUT_PULLUP	   = 0x087
        GPIO_MODE_MGMT_STD_OUTPUT	       = 0x00b
        GPIO_MODE_MGMT_STD_BIDIRECTIONAL   = 0x009
        GPIO_MODE_USER_STD_INPUT_NOPULL	   = 0x006
        GPIO_MODE_USER_STD_INPUT_PULLDOWN  = 0x046
        GPIO_MODE_USER_STD_INPUT_PULLUP	   = 0x086
        GPIO_MODE_USER_STD_OUTPUT	       = 0x00a
        GPIO_MODE_USER_STD_BIDIRECTIONAL   = 0x00C
class MASK_GPIO_CTRL(Enum):
    MASK_GPIO_CTRL_MGMT_EN   = 0
    MASK_GPIO_CTRL_OUT_DIS   = 1
    MASK_GPIO_CTRL_OVERRIDE  = 2
    MASK_GPIO_CTRL_INP_DIS   = 3
    MASK_GPIO_CTRL_MOD_SEL   = 4
    MASK_GPIO_CTRL_ANLG_EN   = 5
    MASK_GPIO_CTRL_ANLG_SEL  = 6
    MASK_GPIO_CTRL_ANLG_POL  = 7
    MASK_GPIO_CTRL_SLOW      = 8
    MASK_GPIO_CTRL_TRIP      = 9
    MASK_GPIO_CTRL_DGTL_MODE = 10

class SPI_COMMAND(Enum):
    NO_OP          = 0x0
    WRITE_STREAM   = 0x80
    READ_STREAM    = 0x40
    READ_WRITE     = 0xC0
    USER_PASS_THRU = 0xC6
    MGMT_PATH_THRU = 0xC4

def get_gpio_num_bit():
    if sky:
        return 13
    else:
        return 10



Macros= {}

def fill_macros(macros_hdl):
    Macros['MPRJ_IO_PADS_1']  = macros_hdl.MPRJ_IO_PADS_1.value.integer
    Macros['MPRJ_IO_PADS_2']  = macros_hdl.MPRJ_IO_PADS_2.value.integer
    Macros['MPRJ_IO_PADS']    = macros_hdl.MPRJ_IO_PADS.value.integer
    Macros['GL']              = macros_hdl.GL.value.integer
    Macros['CARAVAN']         = macros_hdl.CARAVAN.value.integer
    Macros['CHECKERS']        = macros_hdl.CHECKERS.value.integer
    Macros['COVERAGE']        = macros_hdl.COVERAGE.value.integer
    Macros['ARM']             = macros_hdl.ARM.value.integer
    Macros['LA_SIZE']         = macros_hdl.LA_SIZE.value.integer
    Macros['USER_SPACE_ADDR'] = macros_hdl.USER_SPACE_ADDR.value.integer
    Macros['USER_SPACE_SIZE'] = macros_hdl.USER_SPACE_SIZE.value.integer



