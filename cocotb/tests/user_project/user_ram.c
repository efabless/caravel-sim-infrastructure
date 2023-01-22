#include "../common_functions/common.c"
#include "../common_functions/gpios.c"
/*
This test is developed for testing RAM used inside the user area by swift 2 release
*/

void main(){
    enable_debug();
    hk_spi_disable();
    configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);
    set_gpio_l(0);
    unsigned int *dff_start_address =  (unsigned int *) AHB_EXT_BASE_ADDR;
    unsigned int dff_size =  8192/4;
    unsigned int data = 0x55555555;

    for (unsigned int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    
    for (unsigned int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            // set_debug_reg2(i+dff_start_address);
            set_gpio_l(0x1E); 
            return;
        }
    }
    
    data = 0xAAAAAAAA;
    for (unsigned int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            // set_debug_reg2(i+dff_start_address);
            set_gpio_l(0x1E); 
            return;
        }
    }
    
    set_gpio_l(0x1B);
}