#include "../../common_functions/common.c"
#include "../../common_functions/gpios.c"
// --------------------------------------------------------

void main(){
    enable_debug();
    /* Monitor pins must be set to output */
    configure_gpio(14,GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(15,GPIO_MODE_MGMT_STD_OUTPUT);
    /* Apply configuration */
    gpio_load();
    set_debug_reg1(0xAA);
    dummy_delay(100000000);
    return; 
}