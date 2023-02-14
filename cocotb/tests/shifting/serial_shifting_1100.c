#include "../common_functions/common.c"
#include "../common_functions/gpios.c"

void main(){
    enable_debug();
    hk_spi_disable();
    int counter = 0;
    for (int i =0;i<19;i++){
        if(counter == 0)
           configure_gpio(i,0x666);
        else if (counter == 1)
           configure_gpio(i,0xccc); 
        else if (counter == 2)
           configure_gpio(i,0x1999); 
        else if (counter == 3)
           configure_gpio(i,0x1333); 
        counter++; 
        counter %= 4;
    }
    counter =0;
    for (int i =37;i>=19;i--){
        if(counter == 0)
           configure_gpio(i,0x666);
        else if (counter == 1)
           configure_gpio(i,0xccc); 
        else if (counter == 2)
           configure_gpio(i,0x1999); 
        else if (counter == 3)
           configure_gpio(i,0x1333); 
        counter++; 
        counter %= 4;
    }
    gpio_config_load();
    dummy_delay(10);
    set_debug_reg1(0XFF); // finish configuration 
    dummy_delay(10000); 
}
