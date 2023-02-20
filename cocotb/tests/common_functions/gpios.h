
#ifndef GPIO_C_HEADER_FILE
#define GPIO_C_HEADER_FILE


void configure_all_gpios(unsigned int config){
    #ifndef ARM
    reg_mprj_io_37 = config;
    reg_mprj_io_36 = config;
    reg_mprj_io_35 = config;
    #endif
    reg_mprj_io_34 = config;
    reg_mprj_io_33 = config;
    reg_mprj_io_32 = config;
    reg_mprj_io_31 = config;
    reg_mprj_io_30 = config;
    reg_mprj_io_29 = config;
    reg_mprj_io_28 = config;
    reg_mprj_io_27 = config;
    reg_mprj_io_26 = config;
    reg_mprj_io_25 = config;
    reg_mprj_io_24 = config;
    reg_mprj_io_23 = config;
    reg_mprj_io_22 = config;
    reg_mprj_io_21 = config;
    reg_mprj_io_20 = config;
    reg_mprj_io_19 = config;
    reg_mprj_io_18 = config;
    reg_mprj_io_17 = config;
    reg_mprj_io_16 = config;
    reg_mprj_io_15 = config;
    reg_mprj_io_14 = config;
    reg_mprj_io_13 = config;
    reg_mprj_io_12 = config;
    reg_mprj_io_11 = config;
    reg_mprj_io_10 = config;
    reg_mprj_io_9  = config;
    reg_mprj_io_8  = config;
    reg_mprj_io_7  = config;
    reg_mprj_io_6  = config;
    reg_mprj_io_5  = config;
    reg_mprj_io_4  = config;
    reg_mprj_io_3  = config;
    reg_mprj_io_2  = config;
    reg_mprj_io_1  = config;
    reg_mprj_io_0  = config;
    gpio_config_load();
}
void gpio_config_load(){
    reg_mprj_xfer = 1;
    while ((reg_mprj_xfer&0x1) == 1);

}
void configure_gpio(int gpio_num, unsigned int config){
    switch(gpio_num){
        case 0 :
            reg_mprj_io_0   = config; break;
        case 1 :
            reg_mprj_io_1   = config; break;
        case 2 :
            reg_mprj_io_2   = config; break;
        case 3 :
            reg_mprj_io_3   = config; break;
        case 4 :
            reg_mprj_io_4   = config; break;
        case 5 :
            reg_mprj_io_5   = config; break;
        case 6 :
            reg_mprj_io_6   = config; break;
        case 7 :
            reg_mprj_io_7   = config; break;
        case 8 :
            reg_mprj_io_8   = config; break;
        case 9 :
            reg_mprj_io_9   = config; break;
        case 10:
            reg_mprj_io_10  = config; break;
        case 11:
            reg_mprj_io_11  = config; break;
        case 12:
            reg_mprj_io_12  = config; break;
        case 13:
            reg_mprj_io_13  = config; break;
        case 14:
            reg_mprj_io_14  = config; break;
        case 15:
            reg_mprj_io_15  = config; break;
        case 16:
            reg_mprj_io_16  = config; break;
        case 17:
            reg_mprj_io_17  = config; break;
        case 18:
            reg_mprj_io_18  = config; break;
        case 19:
            reg_mprj_io_19  = config; break;
        case 20:
            reg_mprj_io_20  = config; break;
        case 21:
            reg_mprj_io_21  = config; break;
        case 22:
            reg_mprj_io_22  = config; break;
        case 23:
            reg_mprj_io_23  = config; break;
        case 24:
            reg_mprj_io_24  = config; break;
        case 25:
            reg_mprj_io_25  = config; break;
        case 26:
            reg_mprj_io_26  = config; break;
        case 27:
            reg_mprj_io_27  = config; break;
        case 28:
            reg_mprj_io_28  = config; break;
        case 29:
            reg_mprj_io_29  = config; break;
        case 30:
            reg_mprj_io_30  = config; break;
        case 31:
            reg_mprj_io_31  = config; break;
        case 32:
            reg_mprj_io_32  = config; break;
        case 33:
            reg_mprj_io_33  = config; break;
        case 34:
            reg_mprj_io_34  = config; break;
        case 35:
            reg_mprj_io_35  = config; break;
        case 36:
            reg_mprj_io_36  = config; break;
        case 37:
            reg_mprj_io_37  = config; break;
        default:
            break;
    }
}

#endif // GPIO_C_HEADER_FILE
