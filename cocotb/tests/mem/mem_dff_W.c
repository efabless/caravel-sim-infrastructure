#include "../common_functions/common.c"
#include "../common_functions/gpios.c"
void main(){
    enable_debug();
    unsigned int *dff_start_address =  (unsigned int *) DFF1_START_ADDR;
    unsigned int dff_size =  DFF1_SIZE/4;
    unsigned int data = 0x55555555;
    unsigned int mask = 0xFFFFFFFF;
    unsigned int shifting =0;
    unsigned int data_used = 0;

    for (unsigned int i = 0; i < dff_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
      *(dff_start_address+i) = data_used; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
        if (data_used != *(dff_start_address+i)){
            set_debug_reg2(dff2_start_address+ i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    data = 0xAAAAAAAA;
    for (unsigned int i = 0; i < dff_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
      *(dff_start_address+i) = data_used; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
        if (data_used != *(dff_start_address+i)){
            set_debug_reg2(dff2_start_address+ i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    set_debug_reg1(0x1B);
}