#include "../common_functions/common.c"
#include "../common_functions/gpios.c"

void main(){
        unsigned int i,i_temp, j, active_gpio_num,num_high_gpio;
        enable_debug();
        hk_spi_disable();
        configure_all_gpios(GPIO_MODE_USER_STD_OUTPUT);        
        set_debug_reg1(0xAA); // finish configuration 
        output_enable_all_gpio_user(1);
        set_gpio_user_l(0x0);
        set_gpio_user_h(0x0);
        active_gpio_num = get_active_gpios_num();
        num_high_gpio = (active_gpio_num - 32);
        i = 0x1 << num_high_gpio;
        i_temp = i;
        for (j = 0; j < num_high_gpio; j++) {
                set_gpio_user_h(i);
                set_debug_reg2(active_gpio_num-j);
                wait_debug_reg1(0xD1); // wait until wait until test read 1
                set_gpio_user_h(0x0);
                set_debug_reg2(0);
                wait_debug_reg1(0xD0);// wait until test read 0
                i >>=1;
                i |= i_temp;
        }
        i = 0x80000000;
        for (j = 0; j < 32; j++) {
                set_gpio_user_h(0x3f);
                set_gpio_user_l(i);
                set_debug_reg2(32-j);
                wait_debug_reg1(0xD1); // wait until test read 1
                set_gpio_user_h(0x00);
                set_gpio_user_l(0x0);
                set_debug_reg2(0);
                wait_debug_reg1(0xD0);// wait until test read 0
                i >>=1;
                i |= 0x80000000;
        }
        set_debug_reg1(0XFF); // configuration done wait environment to send 0xFFA88C5A to reg_mprj_datal
}

