`timescale 1 ns / 1 ps
`ifdef VCS
	`include "includes.v" // in case of RTL coverage is needed and it doesn't work correctly without include files by this way
`ifdef sky130
`ifndef ENABLE_SDF
	`include "libs.ref/sky130_fd_io/verilog/sky130_fd_io.v"
	`include "libs.ref/sky130_fd_io/verilog/sky130_ef_io.v"
	`include "libs.ref/sky130_fd_sc_hd/verilog/primitives.v"
	`include "libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v"
	`include "libs.ref/sky130_fd_sc_hvl/verilog/primitives.v"
	`include "libs.ref/sky130_fd_sc_hvl/verilog/sky130_fd_sc_hvl.v"
`else
	`include "cvc-pdk/sky130_ef_io.v"
	`include "cvc-pdk/sky130_fd_io.v"
	`include "cvc-pdk/primitives_hd.v"
	`include "cvc-pdk/sky130_fd_sc_hd.v"
	`include "cvc-pdk/primitives_hvl.v"
	`include "cvc-pdk/sky130_fd_sc_hvl.v"
`endif // ~ ENABLE_SDF
`elsif gf180  // sky180
	`include "libs.ref/gf180mcu_fd_io/verilog/gf180mcu_fd_io.v"
	// `include "libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/GF018hv5v_mcu_sc7_udp.v"
	`include "libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/primitives.v"
	`include "libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/gf180mcu_fd_sc_mcu7t5v0.v"
	// `include "libs.ref/gf180mcu_sc7_hv/verilog/GF018hv5v_mcu_sc7.v"
	`include "libs.ref/gf180mcu_fd_ip_sram/verilog/gf180mcu_fd_ip_sram__sram512x8m8wm1.v"
`endif //sky180
`endif // VCS


module caravel_top ;

// parameter FILENAME = {"hex_files/",`TESTNAME,".hex"};
parameter FILENAME={`SIM_PATH,"/hex_files/",`TESTNAME,".hex"};
`ifdef WAVE_GEN 
initial begin
	`ifdef VCS
		`ifdef ENABLE_SDF
				$vcdplusfile({`SIM_PATH,`TAG,"/",`FTESTNAME,"/",`TESTNAME , `CORNER,"-",`SDF_POSTFIX, ".vpd"});
		`else
				$vcdplusfile({`SIM_PATH,`TAG,"/",`FTESTNAME,"/",`TESTNAME ,".vpd"});
		`endif
		$vcdpluson();
	`else 
		$dumpfile ({`SIM_PATH,`TAG,"/",`SIM,"-",`TESTNAME,"/",`SIM,"-",`TESTNAME,".vcd"});
		$dumpvars (0, caravel_top);
	`endif
end
`endif // WAVE_GEN
	`ifdef VCS
	`ifdef ENABLE_SDF
		`include "sdf_includes.v"
	`endif
	`endif // VCS
	wire vddio_tb;	// Common 3.3V padframe/ESD power
    wire vddio_2_tb;	// Common 3.3V padframe/ESD power
    wire vssio_tb;	// Common padframe/ESD ground
    wire vssio_2_tb;	// Common padframe/ESD ground
    wire vdda_tb;		// Management 3.3V power
    wire vssa_tb;		// Common analog ground
    wire vccd_tb;		// Management/Common 1.8V power
    wire vssd_tb;		// Common digital ground
    wire vdda1_tb;	// User area 1 3.3V power
    wire vdda1_2_tb;	// User area 1 3.3V power
    wire vdda2_tb;	// User area 2 3.3V power
    wire vssa1_tb;	// User area 1 analog ground
    wire vssa1_2_tb;	// User area 1 analog ground
    wire vssa2_tb;	// User area 2 analog ground
    wire vccd1_tb;	// User area 1 1.8V power
    wire vccd2_tb;	// User area 2 1.8V power
    wire vssd1_tb;	// User area 1 digital ground
    wire vssd2_tb;	// User area 2 digital ground

    wire gpio_tb;		// Used for external LDO control
    wire [38-1:0] mprj_io_tb;
    reg clock_tb;    	// CMOS core clock input; not a crystal
    wire resetb_tb;	// Reset input (sense inverted)

    // Note that only two flash data pins are dedicated to the
    // management SoC wrapper.  The management SoC exports the
    // quad SPI mode status to make use of the top two mprj_io
    // pins for io2 and io3.

    wire flash_csb_tb;
    wire flash_clk_tb;
    wire flash_io0_tb;
    wire flash_io1_tb;
`ifdef CPU_TYPE_ARM
swift_caravel uut (
`else //CPU_TYPE_ARM
`ifdef CARAVAN
caravan uut (
`else // caravan
caravel uut (
`endif // caravan
`endif // CPU_TYPE_ARM
		`ifdef sky130
		.vddio	  (vddio_tb),
		.vddio_2  (vddio_2_tb),		
		.vssio	  (vssio_tb),
		.vssio_2  (vssio_2_tb),
		.vdda	  (vdda_tb),
		.vssa	  (vssa_tb),
		.vccd	  (vccd_tb),
		.vssd	  (vssd_tb),
		.vdda1    (vdda1_tb),
		.vdda1_2  (vdda1_2_tb),
		.vdda2    (vdda2_tb),
		.vssa1	  (vssa1_tb),
		.vssa1_2  (vssa1_2_tb),
		.vssa2	  (vssa2_tb),
		.vccd1	  (vccd1_tb),
		.vccd2	  (vccd2_tb),
		.vssd1	  (vssd1_tb),
		.vssd2	  (vssd2_tb),
		`elsif gf180 
		.VDD (vddio_tb),
		.VSS (vssio_tb),
		`endif // sky130
		.clock	  (clock_tb),
		.gpio     (gpio_tb),
		.mprj_io  (mprj_io_tb),
		.flash_csb(flash_csb_tb),
		.flash_clk(flash_clk_tb),
		.flash_io0(flash_io0_tb),
		.flash_io1(flash_io1_tb),
		.resetb	  (resetb_tb)
	);
	
	`ifdef CPU_TYPE_ARM 
	sst26wf080b flash(
		.SCK (flash_clk_tb),
		.SIO ({mprj_io_tb[37], mprj_io_tb[36], flash_io1_tb, flash_io0_tb} ),
		.CEb (flash_csb_tb)
	);
	initial begin
	$display("Reading %s",  FILENAME);
	#1 $readmemh(FILENAME, flash.I0.memory);
	//$display("Memory 5 bytes = 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x",
	//	memory[0], memory[1], memory[2],
	//	memory[3], memory[4]);
	$display("%s loaded into memory", FILENAME);
	$display("Memory 5 bytes = 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x",
		flash.I0.memory[0], flash.I0.memory[1], flash.I0.memory[2],
		flash.I0.memory[3], flash.I0.memory[4]);
	end
 	
	`else
	spiflash #(
		FILENAME
	) spiflash (
		.csb(flash_csb_tb),
		.clk(flash_clk_tb),
		.io0(flash_io0_tb),
		.io1(flash_io1_tb),
		.io2(),			// not used
		.io3()			// not used
	);
	`endif // CPU_TYPE_ARM
	mac macros();


	// make speical variables for the mprj input to assign the input without writing to the output gpios
	// cocotb limitation  #2587: iverilog deal with array as 1 object not multiple of objects so can't write to only 1 element
	wire gpio0;
	wire gpio0_en;	
	wire gpio1;
	wire gpio1_en;	
	wire gpio2;
	wire gpio2_en;	
	wire gpio3;
	wire gpio3_en;	
	wire gpio4;
	wire gpio4_en;
	wire gpio5;
	wire gpio5_en;	
	wire gpio6;
	wire gpio6_en;	
	wire gpio7;
	wire gpio7_en;	
	wire gpio8;
	wire gpio8_en;	
	wire gpio9;
	wire gpio9_en;	
	wire gpio10;
	wire gpio10_en;	
	wire gpio11;
	wire gpio11_en;	
	wire gpio12;
	wire gpio12_en;
	wire gpio13;
	wire gpio13_en;	
	wire gpio14;
	wire gpio14_en;	
	wire gpio15;
	wire gpio15_en;
	wire gpio16;
	wire gpio16_en;	
	wire gpio17;
	wire gpio17_en;	
	wire gpio18;
	wire gpio18_en;	
	wire gpio19;
	wire gpio19_en;
	wire gpio20;
	wire gpio20_en;	
	wire gpio21;
	wire gpio21_en;	
	wire gpio22;
	wire gpio22_en;	
	wire gpio23;
	wire gpio23_en;	
	wire gpio24;
	wire gpio24_en;	
	wire gpio25;
	wire gpio25_en;	
	wire gpio26;
	wire gpio26_en;	
	wire gpio27;
	wire gpio27_en;
	wire gpio28;
	wire gpio28_en;	
	wire gpio29;
	wire gpio29_en;	
	wire gpio30;
	wire gpio30_en;	
	wire gpio31;
	wire gpio31_en;	
	wire gpio32;
	wire gpio32_en;	
	wire gpio33;
	wire gpio33_en;	
	wire gpio34;
	wire gpio34_en;	
	wire gpio35;
	wire gpio35_en;	
	wire gpio36;
	wire gpio36_en;	
	wire gpio37;
	wire gpio37_en;
	

	assign mprj_io_tb[0] = (gpio0_en) ? gpio0 : 1'bz;
	assign mprj_io_tb[1] = (gpio1_en) ? gpio1 : 1'bz;
	assign mprj_io_tb[2] = (gpio2_en) ? gpio2 : 1'bz;
	assign mprj_io_tb[3] = (gpio3_en) ? gpio3 : 1'bz;
	assign mprj_io_tb[4] = (gpio4_en) ? gpio4 : 1'bz;

	assign mprj_io_tb[5] = (gpio5_en) ? gpio5 : 1'bz;
	assign mprj_io_tb[6] = (gpio6_en) ? gpio6 : 1'bz;
	assign mprj_io_tb[7] = (gpio7_en) ? gpio7 : 1'bz;
	assign mprj_io_tb[8] = (gpio8_en) ? gpio8 : 1'bz;
	assign mprj_io_tb[9] = (gpio9_en) ? gpio9 : 1'bz;

	assign mprj_io_tb[10] = (gpio10_en) ? gpio10 : 1'bz;
	assign mprj_io_tb[11] = (gpio11_en) ? gpio11 : 1'bz;
	assign mprj_io_tb[12] = (gpio12_en) ? gpio12 : 1'bz;
	assign mprj_io_tb[13] = (gpio13_en) ? gpio13 : 1'bz;
	assign mprj_io_tb[14] = (gpio14_en) ? gpio14 : 1'bz;

	assign mprj_io_tb[15] = (gpio15_en) ? gpio15 : 1'bz;
	assign mprj_io_tb[16] = (gpio16_en) ? gpio16 : 1'bz;
	assign mprj_io_tb[17] = (gpio17_en) ? gpio17 : 1'bz;
	assign mprj_io_tb[18] = (gpio18_en) ? gpio18 : 1'bz;
	assign mprj_io_tb[19] = (gpio19_en) ? gpio19 : 1'bz;

	assign mprj_io_tb[20] = (gpio20_en) ? gpio20 : 1'bz;
	assign mprj_io_tb[21] = (gpio21_en) ? gpio21 : 1'bz;
	assign mprj_io_tb[22] = (gpio22_en) ? gpio22 : 1'bz;
	assign mprj_io_tb[23] = (gpio23_en) ? gpio23 : 1'bz;
	assign mprj_io_tb[24] = (gpio24_en) ? gpio24 : 1'bz;

	assign mprj_io_tb[25] = (gpio25_en) ? gpio25 : 1'bz;
	assign mprj_io_tb[26] = (gpio26_en) ? gpio26 : 1'bz;
	assign mprj_io_tb[27] = (gpio27_en) ? gpio27 : 1'bz;
	assign mprj_io_tb[28] = (gpio28_en) ? gpio28 : 1'bz;
	assign mprj_io_tb[29] = (gpio29_en) ? gpio29 : 1'bz;

	assign mprj_io_tb[30] = (gpio30_en) ? gpio30 : 1'bz;
	assign mprj_io_tb[31] = (gpio31_en) ? gpio31 : 1'bz;
	assign mprj_io_tb[32] = (gpio32_en) ? gpio32 : 1'bz;
	assign mprj_io_tb[33] = (gpio33_en) ? gpio33 : 1'bz;
	assign mprj_io_tb[34] = (gpio34_en) ? gpio34 : 1'bz;

	assign mprj_io_tb[35] = (gpio35_en) ? gpio35 : 1'bz;
	assign mprj_io_tb[36] = (gpio36_en) ? gpio36 : 1'bz;
	assign mprj_io_tb[37] = (gpio37_en) ? gpio37 : 1'bz;



	// to read from mprj array with iverilog  
	wire gpio0_monitor;
	wire gpio1_monitor;
	wire gpio2_monitor;
	wire gpio3_monitor;
	wire gpio4_monitor;
	wire gpio5_monitor;
	wire gpio6_monitor;
	wire gpio7_monitor;
	wire gpio8_monitor;
	wire gpio9_monitor;
	wire gpio10_monitor;
	wire gpio11_monitor;
	wire gpio12_monitor;
	wire gpio13_monitor;
	wire gpio14_monitor;
	wire gpio15_monitor;
	wire gpio16_monitor;
	wire gpio17_monitor;
	wire gpio18_monitor;
	wire gpio19_monitor;
	wire gpio20_monitor;
	wire gpio21_monitor;
	wire gpio22_monitor;
	wire gpio23_monitor;
	wire gpio24_monitor;
	wire gpio25_monitor;
	wire gpio26_monitor;
	wire gpio27_monitor;
	wire gpio28_monitor;
	wire gpio29_monitor;
	wire gpio30_monitor;
	wire gpio31_monitor;
	wire gpio32_monitor;
	wire gpio33_monitor;
	wire gpio34_monitor;
	wire gpio35_monitor;
	wire gpio36_monitor;
	wire gpio37_monitor;

	assign gpio0_monitor = mprj_io_tb[0];
	assign gpio1_monitor = mprj_io_tb[1];
	assign gpio2_monitor = mprj_io_tb[2];
	assign gpio3_monitor = mprj_io_tb[3];
	assign gpio4_monitor = mprj_io_tb[4];
	assign gpio5_monitor = mprj_io_tb[5];
	assign gpio6_monitor = mprj_io_tb[6];
	assign gpio7_monitor = mprj_io_tb[7];
	assign gpio8_monitor = mprj_io_tb[8];
	assign gpio9_monitor = mprj_io_tb[9];
	assign gpio10_monitor = mprj_io_tb[10];
	assign gpio11_monitor = mprj_io_tb[11];
	assign gpio12_monitor = mprj_io_tb[12];
	assign gpio13_monitor = mprj_io_tb[13];
	assign gpio14_monitor = mprj_io_tb[14];
	assign gpio15_monitor = mprj_io_tb[15];
	assign gpio16_monitor = mprj_io_tb[16];
	assign gpio17_monitor = mprj_io_tb[17];
	assign gpio18_monitor = mprj_io_tb[18];
	assign gpio19_monitor = mprj_io_tb[19];
	assign gpio20_monitor = mprj_io_tb[20];
	assign gpio21_monitor = mprj_io_tb[21];
	assign gpio22_monitor = mprj_io_tb[22];
	assign gpio23_monitor = mprj_io_tb[23];
	assign gpio24_monitor = mprj_io_tb[24];
	assign gpio25_monitor = mprj_io_tb[25];
	assign gpio26_monitor = mprj_io_tb[26];
	assign gpio27_monitor = mprj_io_tb[27];
	assign gpio28_monitor = mprj_io_tb[28];
	assign gpio29_monitor = mprj_io_tb[29];
	assign gpio30_monitor = mprj_io_tb[30];
	assign gpio31_monitor = mprj_io_tb[31];
	assign gpio32_monitor = mprj_io_tb[32];
	assign gpio33_monitor = mprj_io_tb[33];
	assign gpio34_monitor = mprj_io_tb[34];
	assign gpio35_monitor = mprj_io_tb[35];
	assign gpio36_monitor = mprj_io_tb[36];
	assign gpio37_monitor = mprj_io_tb[37];

endmodule

// module that has all needed macros by cocotb
module mac;

reg [7:0] MPRJ_IO_PADS_1  = `ifdef MPRJ_IO_PADS_1 `MPRJ_IO_PADS_1 `else 0 `endif;	/* number of user GPIO pads on user1 side */
reg [7:0] MPRJ_IO_PADS_2  = `ifdef MPRJ_IO_PADS_2 `MPRJ_IO_PADS_2 `else 0 `endif;	/* number of user GPIO pads on user2 side */
reg [7:0] MPRJ_IO_PADS    = `ifdef MPRJ_IO_PADS `MPRJ_IO_PADS `else 0 `endif;
reg [7:0] MPRJ_PWR_PADS_1 =`ifdef MPRJ_PWR_PADS_1 `MPRJ_PWR_PADS_1 `else 0 `endif;	/* vdda1, vccd1 enable/disable control */
reg [7:0] MPRJ_PWR_PADS_2 = `ifdef MPRJ_PWR_PADS_2 `MPRJ_PWR_PADS_2 `else 0 `endif;	/* vdda2, vccd2 enable/disable control */
reg [7:0] MPRJ_PWR_PADS   =`ifdef MPRJ_PWR_PADS `MPRJ_PWR_PADS `else 0 `endif;
// Analog pads are only used by the "caravan" module and associated
// modules such as user_analog_project_wrapper and chip_io_alt.
reg [7:0] ANALOG_PADS_1  = `ifdef ANALOG_PADS_1 `ANALOG_PADS_1 `else 0 `endif;
reg [7:0] ANALOG_PADS_2  = `ifdef ANALOG_PADS_2 `ANALOG_PADS_2 `else 0 `endif;
reg [7:0] ANALOG_PADS    = `ifdef ANALOG_PADS `ANALOG_PADS `else 0 `endif;

// Type and size of soc_mem
reg USE_CUSTOM_DFFRAM    = `ifdef USE_CUSTOM_DFFRAM 1 `else 0 `endif;
// don't change the following without double checking addr widths
reg [7:0] MEM_WORDS      = `ifdef MEM_WORDS `MEM_WORDS `else 0 `endif;
// Number of columns in the custom memory; takes one of three values:
// 1 column : 1 KB, 2 column: 2 KB, 4 column: 4KB
reg [7:0] DFFRAM_WSIZE   = `ifdef DFFRAM_WSIZE `DFFRAM_WSIZE `else 0 `endif;
reg [7:0] DFFRAM_USE_LATCH = `ifdef DFFRAM_USE_LATCH `DFFRAM_USE_LATCH `else 0 `endif;

// not really parameterized but just to easily keep track of the number
// of ram_block across different modules
reg [7:0] RAM_BLOCKS = `ifdef RAM_BLOCKS `RAM_BLOCKS `else 0 `endif;

// Clock divisor default value
reg [7:0] CLK_DIV = `ifdef CLK_DIV `CLK_DIV `else 0 `endif;

// GPIO control default mode and enable for most I/Os
// Most I/Os set to be user bidirectional pins on power-up.
reg [7:0] MGMT_INIT = `ifdef MGMT_INIT `MGMT_INIT `else 0 `endif;
reg [7:0] OENB_INIT = `ifdef OENB_INIT `OENB_INIT `else 0 `endif;
reg [7:0] DM_INIT   = `ifdef DM_INIT   `DM_INIT `else 0 `endif;

// GL

reg GL = `ifdef GL 1 `else 0 `endif;

reg CARAVAN = `ifdef CARAVAN 1 `else 0 `endif;

reg CHECKERS = `ifdef CHECKERS 1 `else 0 `endif;
reg COVERAGE = `ifdef COVERAGE 1 `else 0 `endif;
reg ARM      = `ifdef CPU_TYPE_ARM      1 `else 0 `endif;

reg [31:0] LA_SIZE  = `ifdef LA_SIZE `LA_SIZE `else 0 `endif;
reg [31:0]USER_SPACE_ADDR  = `USER_SPACE_ADDR ;
reg [31:0]USER_SPACE_SIZE  = `USER_SPACE_SIZE ;
reg [31:0]IO_CTRL_BITS  = `IO_CTRL_BITS;
endmodule