/**
 \file
*/
#ifndef MGMT_GPIO_C_HEADER_FILE
#define MGMT_GPIO_C_HEADER_FILE

// managment gpio 
/**
 * Configure managment GPIO as input  
 * 
 */
void mgmt_gpio_i_enable(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
    #ifndef REG_GPIO_INVERTED 
    reg_gpio_ien = 1;
    reg_gpio_oe = 0;
    #else
    reg_gpio_ien = 0; // because in gf the gpio enable regs are inverted
    reg_gpio_oe = 1;
    #endif
    dummy_delay(1);
}
/**
 * Configure managment GPIO as outpur  
 * 
 */
void mgmt_gpio_o_enable(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
    #ifndef REG_GPIO_INVERTED 
    reg_gpio_ien = 0;
    reg_gpio_oe = 1;
    #else
    reg_gpio_ien = 1; // because in gf the gpio enable regs are inverted
    reg_gpio_oe = 0;
    #endif
    dummy_delay(1);
}
/**
 * Configure managment GPIO as bi-direction  
 * 
 */
void mgmt_gpio_io_enable(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
    #ifndef REG_GPIO_INVERTED 
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    #else
    reg_gpio_ien = 0; // because in gf the gpio enable regs are inverted
    reg_gpio_oe = 0;
    #endif
}
/**
 * Configure managment GPIO as floating 
 * It's not connected as input or output   
 * 
 */
void mgmt_gpio_io_disable(){
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0; // for full swing
    #ifndef REG_GPIO_INVERTED 
    reg_gpio_ien = 0;
    reg_gpio_oe = 0;
    #else
    reg_gpio_ien = 1; // because in gf the gpio enable regs are inverted
    reg_gpio_oe = 1;
    #endif
}
/**
 * Write data in managment GPIO
 * 
 * @param data data to write at managment GPIO possbile values are 0 and 1
 * 
 * \note
 * This function works when managment GPIO  configured as output
 * 
 */
void mgmt_gpio_wr(bool data){reg_gpio_out = data;}
/**
 * Read data in managment GPIO
 * 
 * \note
 * This function works correctly when managment GPIO  configured as input 
 * If managment doesn't connect to anything the software would read "0"
 * 
 */
int  mgmt_gpio_rd(){return reg_gpio_in;}
/**
 * Wait over managment GPIO to equal data
 * 
 * \note
 * This function works correctly when managment GPIO  configured as input 
 *  
 * @param data data to wait over 
 * 
 */
void wait_gpio_mgmt(bool data){while (reg_gpio_in == data);}


#endif // MGMT_GPIO_C_HEADER_FILE
