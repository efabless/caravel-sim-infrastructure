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
#include <common.h>


void main(){
    enable_debug();
    clear_flag();
    enable_hk_spi(0);
    configure_gpio(6,GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5,GPIO_MODE_MGMT_STD_INPUT_NOPULL);
    gpio_config_load();
    uart_RX_enable(1);
    enable_uart_rx_irq(1);

    set_debug_reg2(0xAA); //start sending data through the uart

    // Loop, waiting for the interrupt to change reg_mprj_datah
    char is_pass = 0;
    int timeout = 50; 
    uart_getc();
    for (int i = 0; i < timeout; i++){
        if (get_flag() == 1){
            set_debug_reg1(0x1B); //test pass irq sent
            is_pass = 1;
            break;
        }
    }
    if (!is_pass){
        set_debug_reg1(0x1E); // timeout
    }
    // test interrupt doesn't happened nothing sent at uart
    set_debug_reg2(0xBB);
    enable_uart_rx_irq(0);
    clear_flag();
    // Loop, waiting for the interrupt to change reg_mprj_datah
    is_pass = 0;

    for (int i = 0; i < timeout; i++){
        if (get_flag() == 1){
            set_debug_reg1(0x2E); //test fail interrupt isn't suppose to happened
            is_pass = 1;
            break;
        }
    }
    if (!is_pass){
        set_debug_reg1(0x2B); // test pass
    }
    // test finish 
    set_debug_reg2(0xFF);
}

