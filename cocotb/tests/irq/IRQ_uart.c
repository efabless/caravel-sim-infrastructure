/*
 * SPDX-FileCopyrightText: 2020 Efabless Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */
#include <defs.h>

#include <csr.h>
#include <soc.h>
#include <irq_vex.h>
#include <uart.h>
#include <stub.c>




extern uint16_t flag;

void main(){
    flag = 0;
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
    reg_debug_1  = 0x0;
    reg_debug_2  = 0x0;

    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_5 = 0x1803;
	 
    if(1){
        reg_mprj_xfer = 1;
        while ((reg_mprj_xfer&0x1) == 1);
    }
    reg_uart_enable = 1;
    reg_uart_irq_en =1;
    irq_setmask(0);
	irq_setie(1);


	irq_setmask(irq_getmask() | (1 << UART_INTERRUPT));

    reg_debug_2 = 0xAA; //start sending data through the uart
    print("M");

    // Loop, waiting for the interrupt to change reg_mprj_datah
    bool is_pass = false;
    int timeout = 100; 

    for (int i = 0; i < timeout; i++){
        if (flag == 1){
            reg_debug_1 = 0x1B; //test pass irq sent
            is_pass = true;
            break;
        }
    }
    if (!is_pass){
        reg_debug_1 = 0x1E; // timeout
    }
    // test interrupt doesn't happened nothing sent at uart
    reg_debug_2 = 0xBB;
    flag = 0;
    // Loop, waiting for the interrupt to change reg_mprj_datah
    is_pass = false;

    for (int i = 0; i < timeout; i++){
        if (flag == 1){
            reg_debug_1 = 0x2E; //test fail interrupt isn't suppose to happened
            is_pass = true;
            break;
        }
    }
    if (!is_pass){
        reg_debug_1 = 0x2B; // test pass
    }
    // test finish 
    reg_debug_2 = 0xFF;

}

