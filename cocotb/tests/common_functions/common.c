#include <defs.h>
#include <stub.c>

void enable_debug(){
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
    set_debug_reg1(0);
    set_debug_reg2(0);
    reg_debug_1  = 0x0;
    reg_debug_2  = 0x0;
    
}
void hk_spi_disable(){reg_hkspi_disable = 1;}
// debug regs
void set_debug_reg1(unsigned int data){reg_debug_1 = data;}
void set_debug_reg2(unsigned int data){reg_debug_2 = data;}
unsigned int get_debug_reg1(){return reg_debug_1;}
unsigned int get_debug_reg2(){return reg_debug_2;}
void wait_debug_reg1(unsigned int data){while (reg_debug_1 != data);}
void wait_debug_reg2(unsigned int data){while (reg_debug_2 != data);}

// gpios_mgmt
void set_gpio_l(unsigned int data){reg_mprj_datal = data;}
void set_gpio_h(unsigned int data){reg_mprj_datah = data;}
unsigned int get_gpio_h(){
    #ifdef ARM 
    return reg_mprj_datah & 0x7; // because with ARM the higest 3 gpios are not used by the design it is used by flashing
    #else 
    return reg_mprj_datah;
    #endif
}
unsigned int get_gpio_l(){return reg_mprj_datal;}
void wait_gpio_l(unsigned int data){while (reg_mprj_datal != data);}
void wait_gpio_h(unsigned int data){
    #ifdef ARM 
    data = data&0x7; // because with ARM the higest 3 gpios are not used by the design it is used by flashing
    #endif
    while (get_gpio_h() != data);    
}
// 
unsigned int get_active_gpios_num(){
    #ifdef ARM 
    return 34;
    #else
    return 37;
    #endif
}
// user project registers
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