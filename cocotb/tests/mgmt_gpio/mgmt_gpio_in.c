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

#include "../common_functions/common.c"
#include "../common_functions/gpios.c"
// --------------------------------------------------------

/*
 *	Management SoC GPIO Pin Test
 *		Tests writing to the GPIO pin.
 */

void main(){
    enable_debug();
    hk_spi_disable();
    mgmt_gpio_i_enable();
    set_debug_reg1(10); // wait for 10 blinks
	for (int i = 0; i < 10; i++) {
        wait_on_gpio_mgmt(0);
        set_debug_reg2(0XAA); //  1 is recieved
        wait_on_gpio_mgmt(1);
        set_debug_reg2(0XBB); // 0 is recieved
	}
    set_debug_reg2(0x1B);
    set_debug_reg1(20);
	for (int i = 0; i < 20; i++) {
        wait_on_gpio_mgmt(0);
        set_debug_reg2(0XAA); // 1 is recieved
        wait_on_gpio_mgmt(1);
        set_debug_reg2(0XBB); // 0 is recieved
	}
    set_debug_reg2(0x2B);
    int temp_in = mgmt_gpio_rd();
    set_debug_reg1(0);
    for (int i =0; i<50;i++){ // timeout
        if (temp_in != mgmt_gpio_rd())
            set_debug_reg2(0xEE); //finish test
    }
    set_debug_reg2(0xFF); //finish test
}

