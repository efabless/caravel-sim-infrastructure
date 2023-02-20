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

// --------------------------------------------------------

#include <common.h>


// --------------------------------------------------------

void wait_for_char(char *c){
    
    if (uart_getc() == *c){
        set_debug_reg2(0x1B); // recieved the correct character
    }else{
        set_debug_reg2(0x1E); // timeout didn't recieve the character
    }
    uart_read_pop();
    set_debug_reg2(0);
}

void main(){
    enable_debug();
    hk_spi_disable();
    configure_gpio(6,GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5,GPIO_MODE_MGMT_STD_INPUT_NOPULL);

    // Now, apply the configuration
    gpio_config_load();

    uart_RX_enable();
    uart_TX_enable();

    print("M");
    wait_for_char("M");
    
    print("B");
    wait_for_char("B");

    print("A");
    wait_for_char("A");

    print("5");
    wait_for_char("5");

    print("o");
    wait_for_char("o");

}
