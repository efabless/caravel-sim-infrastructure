#include "../common_functions/common.c"
#include "../common_functions/gpios.c"

void main(){
    enable_debug();
    hk_spi_disable();
    output_enable_all_gpio_user(1);
    configure_all_gpios(GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    set_debug_reg1(0xAA); // finish configuration 
    //print("adding a very very long delay because cpu produces X's when code finish and this break the simulation");
    for(int i=0; i<100000000; i++);

    while (1);
}
