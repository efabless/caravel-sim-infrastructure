/**
 \file
*/
#ifndef COMMON_C_HEADER_FILE
#define COMMON_C_HEADER_FILE

#include <defs.h>
#include <stub.c>
#ifdef ARM 
#include "swift.h"
#include <stdbool.h>
#else 
#include <uart.h>
#include <irq_vex.h>

#endif
#include <gpios.h>
#include <timer0.h>
#include <mgmt_gpio.h>
#include <irq.h>
#include <la.h>
#include <uart_api.h>
#include <spi_master.h>

#ifndef DOXYGEN_SHOULD_SKIP_THIS
void enable_debug(){
    enable_user_interface();
    set_debug_reg1(0);
    set_debug_reg2(0);
    
}
#endif /* DOXYGEN_SHOULD_SKIP_THIS */
/**
 * Enable comunication between software and user project 
 * \warning 
 * This necessary when reading or writing are needed between wishbone and user project 
 * if interface isn't enabled no ack would be recieve and the writing or reading command will be stuck
 */
void enable_user_interface(){
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable = reg_wb_enable | 0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
}
/**
 * Enable or disable the housekeeping SPI 
 * This function writes to the housekeeping disenable register inside the housekeeping
 * \note
 * When this register asserted housekeeping SPI can't be used and gpios [3] which is CSB can be used as anyother housekeeping gpio 
 *  
 * @param is_enable when 1 (true) housekeeping is active, 0 (false) housekeeping is disabled
 */
void enable_hk_spi(bool is_enable){reg_hkspi_disable = !is_enable;}
// debug regs
#ifndef DOXYGEN_SHOULD_SKIP_THIS
void set_debug_reg1(unsigned int data){reg_debug_1 = data;}
void set_debug_reg2(unsigned int data){reg_debug_2 = data;}
unsigned int get_debug_reg1(){return reg_debug_1;}
unsigned int get_debug_reg2(){return reg_debug_2;}
void wait_debug_reg1(unsigned int data){while (get_debug_reg1() != data);}
void wait_debug_reg2(unsigned int data){while (get_debug_reg2() != data);}
#endif /* DOXYGEN_SHOULD_SKIP_THIS */

// user project registers
#ifndef DOXYGEN_SHOULD_SKIP_THIS
#ifndef ARM
#define reg_mprj_userl (*(volatile unsigned int*)0x300FFFF0)
#define reg_mprj_userh (*(volatile unsigned int*)0x300FFFF4)
#define reg_oeb_userl  (*(volatile unsigned int*)0x300FFFEC)
#define reg_oeb_userh  (*(volatile unsigned int*)0x300FFFE8)
#else
#define reg_mprj_userl (*(volatile unsigned int*)0x41FFFFF4)
#define reg_mprj_userh (*(volatile unsigned int*)0x41FFFFF0)
#define reg_oeb_userl  (*(volatile unsigned int*)0x41FFFFEC)
#define reg_oeb_userh  (*(volatile unsigned int*)0x41FFFFE8)
#endif

// gpio_user 
void set_gpio_user_l(unsigned int data){reg_mprj_userl = data;}
void set_gpio_user_h(unsigned int data){reg_mprj_userh = data;}
unsigned int get_gpio_user_h(){
    #ifdef ARM 
    return reg_mprj_userh & 0x7; // because with ARM the higest 3 gpios are not used by the design it is used by flashing
    #else 
    return reg_mprj_userh;
    #endif
}
unsigned int get_gpio_user_l(){return reg_mprj_userl;}
void wait_gpio_user_l(unsigned int data){while (reg_mprj_userl != data);}
void wait_gpio_user_h(unsigned int data){
    #ifdef ARM 
    data = data&0x7; // because with ARM the higest 3 gpios are not used by the design it is used by flashing
    #endif
    while (get_gpio_user_h() != data);    
}

void output_enable_all_gpio_user(char is_enable){
    if (is_enable){
        reg_oeb_userl = 0x0;
        #ifdef ARM 
        reg_oeb_userh = 0x38; // 111000 highest gpios has to be disabled 
        #else 
        reg_oeb_userh = 0x0;
        #endif
    }else{
        reg_oeb_userl = 0xFFFFFFFF;
        reg_oeb_userh = 0x3F;
    }

}
#endif /* DOXYGEN_SHOULD_SKIP_THIS */

// 
/**
 * Insert delay 
 * 
 * @param num number of delays steps. step is increment local variable and check it's value
 * 
 * 
 */
void dummy_delay(int num){
    for (int i=0;i < num;i++){
        #ifdef ARM
        reg_wb_enable = reg_wb_enable;
        #endif //ARM
        continue;
    }
}



// debug 
void mgmt_debug_enable(){reg_wb_enable = reg_wb_enable | 0x10;}


// set user address value 

void write_user_word(unsigned int data,int offset){
    (*(volatile unsigned int*) (USER_SPACE_ADDR + offset )) = data;
}

unsigned int write_read_word(int offset){
    return (*(volatile unsigned int*) (USER_SPACE_ADDR + offset ));
}
void write_user_half_word(unsigned short data,unsigned int offset,bool is_lower_half){
    unsigned int half_word_offset = offset *2 + is_lower_half;
    (*(volatile unsigned short*) (USER_SPACE_ADDR + half_word_offset )) = data;
}

unsigned short read_user_half_word(unsigned int offset,bool is_lower_half){
    unsigned int half_word_offset = offset *2 + is_lower_half;
    return (*(volatile unsigned short*) (USER_SPACE_ADDR + half_word_offset ));
}

void write_user_byte(unsigned char data,unsigned int offset,unsigned char byte_num){
    if (byte_num > 3) 
        byte_num =0; 
    unsigned int byte_offset = offset *4 + byte_num;
    (*(volatile unsigned int*) (USER_SPACE_ADDR + byte_offset )) = data;
}

unsigned char read_user_byte( unsigned int offset,unsigned char byte_num){
    if (byte_num > 3) 
        byte_num =0; 
    unsigned int byte_offset = offset *4 + byte_num;
    return (*(volatile unsigned int*) (USER_SPACE_ADDR + byte_offset ));
}


#endif // COMMON_C_HEADER_FILE
