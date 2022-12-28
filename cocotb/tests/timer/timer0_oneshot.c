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


void main(){
    unsigned int value;
    unsigned int old_value;
    enable_debug();
    hk_spi_disable();

    /* Configure timer for a single-shot countdown */
    timer0_oneshot_configure(0xF3000);

    // test path if counter value stop updated after reach 0 and also the value is always decrementing
    update_timer0_val(); // update reg_timer0_value with new counter value
    old_value = get_timer0_val();
    // value us decrementing until it reachs zero
    while (1) {
        update_timer0_val(); // update reg_timer0_value with new counter value
        value = get_timer0_val();
        if (value < old_value && value != 0){
            set_debug_reg1(0x1B); // value decrease
        }
        else if (value == 0){
            set_debug_reg1(0x2B); // value reach 0
            break;
        }else{
            set_debug_reg1(0x1F); // value updated incorrectly
        }
	    old_value = value;
    }
    // check 10 times that value don't change from 0
	dummy_delay(10);
    update_timer0_val(); // update reg_timer0_value with new counter value

    if (get_timer0_val() == 0){
        set_debug_reg1(0x3B); //timer updated correctly
    }else{
        set_debug_reg1(0x2F); //timer updated incorrectly
    }
    set_debug_reg2(0xFF); // finish test
}

