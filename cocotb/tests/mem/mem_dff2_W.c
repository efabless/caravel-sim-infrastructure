#include <defs.h>

void main()
{
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
    reg_debug_1  = 0x0;
    reg_debug_2  = 0x0;

    unsigned int *dff2_start_address =  (unsigned int *) 0x00000400;
    unsigned int dff2_size =  0x200 / 4;

    unsigned int data = 0x55555555;
    for (unsigned int i = 0; i < dff2_size; i++){
      *(dff2_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff2_size; i++){
        if (data != *(dff2_start_address+i)){
            reg_debug_2 = i;
            reg_debug_1 = 0x1E; 
            return;
        }
    }

    data = 0xAAAAAAAA;
    for (unsigned int i = 0; i < dff2_size; i++){
      *(dff2_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff2_size; i++){
        if (data != *(dff2_start_address+i)){
            reg_debug_2 = i;
            reg_debug_1 = 0x1E; 
            return;
        }
    }

    reg_debug_1 = 0x1B;

}