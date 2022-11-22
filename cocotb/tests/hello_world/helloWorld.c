#include <defs.h>

int main(){
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    unsigned int j = 0x77;
    reg_debug_1  = 0x66;
    reg_debug_1  = j;
    // reg_debug_1  = 1;
    // reg_debug_1  = j;
    // reg_debug_1  = 1;
    // reg_debug_1  = j;
    // (*(volatile uint32_t*)0x0 ) = 0x11; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x8 ) = (*(volatile uint32_t*)0x4 ); 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x88888888; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x2 ) = 0x14; 

    return 0;
}