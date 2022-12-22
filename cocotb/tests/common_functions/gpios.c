
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

    reg_mprj_xfer = 1;
    while ((reg_mprj_xfer&0x1) == 1);

}