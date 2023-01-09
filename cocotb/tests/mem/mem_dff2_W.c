#include "../common_functions/common.c"
#include "../common_functions/gpios.c"
void main(){
    enable_debug();
    unsigned int *dff2_start_address =  (unsigned int *) DFF2_START_ADDR;
    unsigned int dff2_size =  DFF2_SIZE / 4;
    unsigned int data = 0x55555555;
    for (unsigned int i = 0; i < dff2_size; i++){
      *(dff2_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff2_size; i++){
        if (data != *(dff2_start_address+i)){
            set_debug_reg2(i);
            set_debug_reg1(0x1E); 
            return;
        }
    }

    data = 0xAAAAAAAA;
    for (unsigned int i = 0; i < dff2_size; i++){
      *(dff2_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff2_size; i++){
        if (data != *(dff2_start_address+i)){
            set_debug_reg2(i);
            set_debug_reg1(0x1E); 
            return;
        }
    }

    set_debug_reg1(0x1B);

}