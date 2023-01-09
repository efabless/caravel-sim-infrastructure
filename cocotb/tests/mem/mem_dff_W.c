#include "../common_functions/common.c"
#include "../common_functions/gpios.c"
void main(){
    enable_debug();
    unsigned int *dff_start_address =  (unsigned int *) DFF1_START_ADDR;
    unsigned int dff_size =  DFF1_SIZE/4;
    unsigned int data = 0x55555555;

    for (unsigned int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            set_debug_reg2(i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    data = 0xAAAAAAAA;
    for (unsigned int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            set_debug_reg2(i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    set_debug_reg1(0x1B);
}