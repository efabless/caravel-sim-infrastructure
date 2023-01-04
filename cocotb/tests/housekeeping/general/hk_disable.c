#include "../../common_functions/common.c"
#include "../../common_functions/gpios.c"
// --------------------------------------------------------

void main(){
    enable_debug();
    set_debug_reg2(0xBB);
    wait_debug_reg1(0xAA);
    hk_spi_enable();
    reg_hkspi_pll_ena =0;
    set_debug_reg1(0xBB);
    dummy_delay(100000000);
}