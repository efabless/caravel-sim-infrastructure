#include <defs.h>
#include <stub.c>
#ifdef ARM 
#include "swift.h"
#endif
void enable_debug(){
    enable_user_interface();
    set_debug_reg1(0);
    set_debug_reg2(0);
    
}
void enable_user_interface(){
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
}
void hk_spi_disable(){reg_hkspi_disable = 1;}
void hk_spi_enable(){reg_hkspi_disable = 0;}
// debug regs
void set_debug_reg1(unsigned int data){reg_debug_1 = data;}
void set_debug_reg2(unsigned int data){reg_debug_2 = data;}
unsigned int get_debug_reg1(){return reg_debug_1;}
unsigned int get_debug_reg2(){return reg_debug_2;}
void wait_debug_reg1(unsigned int data){while (get_debug_reg1() != data);}
void wait_debug_reg2(unsigned int data){while (get_debug_reg2() != data);}

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
unsigned int get_gpio_num_bit(){
    #ifdef SKY 
    return 13;
    #elif GF
    return 10;
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

// managment gpio 
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
    dummy_delay(25);
}
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
    dummy_delay(25);
}

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
void mgmt_gpio_wr(int data){reg_gpio_out = data;}

int  mgmt_gpio_rd(){return reg_gpio_in;}

void wait_on_gpio_mgmt(unsigned int data){while (reg_gpio_in == data);}

// 
void dummy_delay(int num){for (int i=0;i < num;i++){set_debug_reg1(get_debug_reg1());}}

// timer 

void timer0_oneshot_configure(unsigned int count){
	reg_timer0_config = reg_timer0_config & 0xFFFFFFFE; // disable
	reg_timer0_data = count;
    reg_timer0_config = reg_timer0_config | 1; // enable
}
void timer0_periodic_configure(unsigned int count){
	reg_timer0_config = reg_timer0_config & 0xFFFFFFFE; // disable
	reg_timer0_data = 0;
    reg_timer0_data_periodic  = count;
    reg_timer0_config = reg_timer0_config | 1; // enable
}
void timer0_disable(){
    reg_timer0_config = reg_timer0_config & 0xFFFFFFFE; // disable counter
}

void update_timer0_val(){
    #ifdef ARM // arm update the register automatically 
    return;
    #else
    reg_timer0_update = 1;
    #endif
}

unsigned int get_timer0_val(){
    #ifdef ARM 
    return reg_timer0_data;
    #else
    return reg_timer0_value;
    #endif
    }
void mgmt_uart_enable(){reg_wb_enable = reg_wb_enable | 0x40;}
// uart 
void uart_TX_enable(){
    #ifdef ARM 
    // 0x08 RW    CTRL[3:0]   TxIntEn, RxIntEn, TxEn, RxEn
    //              [6] High speed test mode Enable
    //              [5] RX overrun interrupt enable
    //              [4] TX overrun interrupt enable
    //              [3] RX Interrupt Enable
    //              [2] TX Interrupt Enable
    //              [1] RX Enable
    //              [0] TX Enable
    mgmt_uart_enable();
    reg_uart_ctrl = reg_uart_ctrl | 0x1;
    reg_uart_clkdiv=0x3C0; // set default to 9600
    #else
    reg_uart_enable = 1;
    #endif
}
void uart_RX_enable(){
    #ifdef ARM 
    // 0x08 RW    CTRL[3:0]   TxIntEn, RxIntEn, TxEn, RxEn
    //              [6] High speed test mode Enable
    //              [5] RX overrun interrupt enable
    //              [4] TX overrun interrupt enable
    //              [3] RX Interrupt Enable
    //              [2] TX Interrupt Enable
    //              [1] RX Enable
    //              [0] TX Enable
    mgmt_uart_enable();
    reg_uart_ctrl = reg_uart_ctrl | 0x2;
    reg_uart_clkdiv=0x3C0; // set default to 9600
    #else
    reg_uart_enable = 1;
    #endif
}

char uart_getc(){
    #ifdef ARM 
    while ((reg_uart_stat &2) == 0); // RX is empty
    #else 
    while (uart_rxempty_read() == 1);
    #endif
    return reg_uart_data;
}

void uart_read_pop(){
    #ifndef ARM
    uart_ev_pending_write(UART_EV_RX);
    #endif
    return;
}

// spi 
void spi_go(){reg_spimaster_control = reg_spimaster_control | 0x1;}
void spi_stop(){reg_spimaster_control = reg_spimaster_control & 0x2;}
char spi_busy(){return reg_spimaster_status & 0x2;}
char spi_done(){return reg_spimaster_status & 0x1;}
void spi_write(char c){
    reg_spimaster_wdata = (unsigned long) c;
    #ifndef ARM
    reg_spimaster_control = 0x0801;
    #else
    spi_go();
    spi_stop();
    while(spi_busy());
    #endif
}
char spi_read(){
    spi_write(0x00);
    while (reg_spimaster_status != 1);
    return reg_spimaster_rdata;
}
void mgmt_spi_enable(){reg_wb_enable = reg_wb_enable | 0x20;}

void spi_en(){
    #ifndef ARM
    reg_spi_enable = 1;
    #else
    mgmt_spi_enable();
    #endif
}
void CS_en(){
    #ifndef ARM
    reg_spimaster_cs = 0x10001; // select chip 0
    #else
    reg_spimaster_control = reg_spimaster_control | 0x2; //bit 1
    #endif
}
void CS_dis(){
     #ifndef ARM
    reg_spimaster_cs = 0;
    #else
    reg_spimaster_control = reg_spimaster_control & 0x1; //bit 1
    spi_stop();
    #endif
}

// LA 
void set_la_ien(char number , unsigned int data){
    switch(number){
        #if LA_SIZE >= 64
        case 0 : reg_la0_iena = data; break;
        case 1 : reg_la1_iena = data; break;
        #endif 
        #if LA_SIZE >= 128
        case 2 : reg_la2_iena = data; break;
        case 3 : reg_la3_iena = data; break;
        #endif
        default: break;
    }
}
void set_la_oenb(char number , unsigned int data){
    switch(number){
        #if LA_SIZE >= 64
        case 0 : reg_la0_oenb = data; break;
        case 1 : reg_la1_oenb = data; break;
        #endif 
        #if LA_SIZE >= 128
        case 2 : reg_la2_oenb = data; break;
        case 3 : reg_la3_oenb = data; break;
        #endif
        default: break;
    }
}
void set_la_reg(char number , unsigned int data){
    switch(number){
        #if LA_SIZE >= 64
        case 0 : reg_la0_data = data; break;
        case 1 : reg_la1_data = data; break;
        #endif 
        #if LA_SIZE >= 128
        case 2 : reg_la2_data = data; break;
        case 3 : reg_la3_data = data; break;
        #endif
        default: break;
    }
}
unsigned int get_la_reg(char number){
    switch(number){
        #if LA_SIZE >= 64
        case 0 : return reg_la0_data_in;
        case 1 : return reg_la1_data_in;
        #endif 
        #if LA_SIZE >= 128
        case 2 : return reg_la2_data_in;
        case 3 : return reg_la3_data_in;
        #endif
        default: break;
    }
}

// IRQ 
#ifndef ARM
extern unsigned int flag;
#else 
unsigned int flag;
void HK_IRQ0_Handler(void){flag = 1;}
void HK_IRQ1_Handler(void){flag = 1;}
void HK_IRQ2_Handler(void){flag = 1;}
void TMR0_Handler(void){flag = 1;clear_TMR0_Handler();}
void UART0_Handler(void){flag = 1;clear_UART0_Handler();}
void clear_TMR0_Handler(){
reg_timer0_irq =1;
}
void clear_UART0_Handler(){
reg_uart_isc =0x3;
}
#endif
char get_flag(){
    #ifndef ARM
    return flag;
    #else 
    dummy_delay(1);
    return flag;
    #endif
}

void clear_flag(){
    #ifndef ARM
    flag=0;
    #else 
    flag=0;
    
    #endif
}
void enable_external1_irq(){
    #ifndef ARM
    irq_setmask(0);
	irq_setie(1);
	irq_setmask(irq_getmask() | (1 << USER_IRQ_4_INTERRUPT));
    reg_user4_irq_en =1;
    #else
    NVIC_EnableIRQ(HK_IRQ1);
    __enable_irq();
    #endif
}
void enable_timer0_irq(){
    #ifndef ARM
    irq_setmask(0);
	irq_setie(1);
	irq_setmask(irq_getmask() | (1 << TIMER0_INTERRUPT));
    reg_timer0_irq_en = 1;
    #else
    NVIC_EnableIRQ(TMR0_IRQn);
	reg_timer0_config = reg_timer0_config | 0x8; // enable irq
    __enable_irq();
    #endif
}
void enable_uart_tx_irq(){
    #ifndef ARM
    reg_uart_enable = 1;
    reg_uart_irq_en =1;
    irq_setmask(0);
	irq_setie(1);
	irq_setmask(irq_getmask() | (1 << UART_INTERRUPT));
    #else
    NVIC_EnableIRQ(UART0_IRQn);
    reg_uart_ctrl = reg_uart_ctrl | 0x5; // enable irq TX 
    __enable_irq();
    #endif
}

void enable_spi_irq(){
    #ifndef ARM
    irq_setmask(0);
	irq_setie(1);
	irq_setmask(irq_getmask() | (1 << USER_IRQ_0_INTERRUPT));
    #else
    NVIC_EnableIRQ(HK_IRQ0);
    __enable_irq();
    #endif
}
// debug 
void mgmt_debug_enable(){reg_wb_enable = reg_wb_enable | 0x10;}
