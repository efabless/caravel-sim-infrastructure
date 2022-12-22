#include <defs.h>
#include <stub.c>
#include "bitbang_functions.c"

void main(){
        unsigned int i, j, k;
        #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
        bool sky = reg_debug_1;
        reg_debug_1  = 0x0;
        reg_debug_2  = 0x0;
        reg_hkspi_disable = 1;
        // bitbang
        // Configure all as output except reg_mprj_io_3
        clock_in_right_o_left_o_standard(sky); // 18	and 19	
        clock_in_right_o_left_o_standard(sky); // 17	and 20	
        clock_in_right_o_left_o_standard(sky); // 16	and 21	
        clock_in_right_o_left_o_standard(sky); // 15	and 22	
        clock_in_right_o_left_o_standard(sky); // 14	and 23	
        clock_in_right_o_left_o_standard(sky); // 13	and 24	
        clock_in_right_o_left_o_standard(sky); // 12	and 25	
        clock_in_right_o_left_o_standard(sky); // 11	and 26	
        clock_in_right_o_left_o_standard(sky); // 10	and 27	
        clock_in_right_o_left_o_standard(sky); // 9	and 28	
        clock_in_right_o_left_o_standard(sky); // 8	and 29	
        clock_in_right_o_left_o_standard(sky); // 7	and 30	
        clock_in_right_o_left_o_standard(sky); // 6	and 31	
        clock_in_right_o_left_o_standard(sky); // 5	and 32	
        clock_in_right_o_left_o_standard(sky); // 4	and 33	
        clock_in_right_o_left_o_standard(sky); // 3	and 34	
        clock_in_right_o_left_o_standard(sky); // 2	and 35	
        clock_in_right_o_left_o_standard(sky); // 1	and 36	
        clock_in_right_o_left_o_standard(sky); // 0 and 37	
        load();
        reg_debug_1 = 0xFF; // finish configuration 
        reg_mprj_datal = 0x0;
        reg_mprj_datah = 0x0;
        i = 0x20;
        for (j = 0; j < 5; j++) {
                reg_mprj_datah = i;
                reg_debug_2 = 37-j;
                reg_mprj_datah = 0x00000000;
                reg_debug_2 = 0;
                i >>=1;
                i |= 0x20;
        }
        i = 0x80000000;
        for (j = 0; j < 32; j++) {
                reg_mprj_datah = 0x3f;
                reg_mprj_datal = i;
                reg_debug_2 = 32-j;
                reg_mprj_datah = 0x00;
                reg_mprj_datal = 0x00000000;
                reg_debug_2 = 0;
                i >>=1;
                i |= 0x80000000;
        }

}


