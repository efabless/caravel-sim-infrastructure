#include <defs.h>
#include <stub.c>
// --------------------------------------------------------

void main(){
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
    reg_debug_1  = 0x0;
    reg_debug_2  = 0x0;

    /* Monitor pins must be set to output */
    reg_mprj_io_15 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_14 = GPIO_MODE_MGMT_STD_OUTPUT;
    /* Apply configuration */
    reg_mprj_xfer = 1;
    while ((reg_mprj_xfer&0x1) == 1);
    reg_debug_1 =0xAA;
    //print("adding a very very long delay because cpu produces X's when code finish and this break the simulation");
    for(int i=0; i<100000000; i++);

    return; 
}