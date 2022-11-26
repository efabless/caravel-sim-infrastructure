#include <defs.h>
#include <stub.c>
#include "bitbang_functions.c"

void main(){
    unsigned int i, j, k;
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    bool sky = reg_debug_1;
    reg_debug_1  = 0x0;
    reg_debug_2  = 0x0;
    reg_hkspi_disable = 1;


    // bitbang
   //Configure all as input except reg_mprj_io_3
    clock_in_right_i_left_i_standard(sky); // 18	and 19	
    clock_in_right_i_left_i_standard(sky); // 17	and 20	
    clock_in_right_i_left_i_standard(sky); // 16	and 21	
    clock_in_right_i_left_i_standard(sky); // 15	and 22	
    clock_in_right_i_left_i_standard(sky); // 14	and 23	
    clock_in_right_i_left_i_standard(sky); // 13	and 24	
    clock_in_right_i_left_i_standard(sky); // 12	and 25	
    clock_in_right_i_left_i_standard(sky); // 11	and 26	
    clock_in_right_i_left_i_standard(sky); // 10	and 27	
    clock_in_right_i_left_i_standard(sky); // 9	and 28	
    clock_in_right_i_left_i_standard(sky); // 8	and 29	
    clock_in_right_i_left_i_standard(sky); // 7	and 30	
    clock_in_right_i_left_i_standard(sky); // 6	and 31	
    clock_in_right_i_left_i_standard(sky); // 5	and 32	
    clock_in_right_i_left_i_standard(sky); // 4	and 33	
    clock_in_right_i_left_i_standard(sky); // 3	and 34	
    clock_in_right_i_left_i_standard(sky); // 2	and 35	
    clock_in_right_i_left_i_standard(sky); // 1	and 36	
    clock_in_right_i_left_i_standard(sky); // 0	and 37	
    load();		                        // load
    reg_debug_1 = 0XAA; // configuration done wait environment to send 0x8F66FD7B to reg_mprj_datal
    while (reg_mprj_datal != 0x8F66FD7B);
    reg_debug_1 = 0XBB; // configuration done wait environment to send 0xFFA88C5A to reg_mprj_datal
    while (reg_mprj_datal != 0xFFA88C5A);
    reg_debug_1 = 0XCC; // configuration done wait environment to send 0xC9536346 to reg_mprj_datal
    while (reg_mprj_datal != 0xC9536346);
    reg_debug_1 = 0XD1;
    while (reg_mprj_datah != 0x3F);
    reg_debug_1 = 0XD2;
    while (reg_mprj_datah != 0x0);
    reg_debug_1 = 0XD3;
    while (reg_mprj_datah != 0x15);
    reg_debug_1 = 0XD4;
    while (reg_mprj_datah != 0x2A);

    reg_debug_2 = 0xFF;

}

