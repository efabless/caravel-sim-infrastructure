// SPDX-FileCopyrightText: 2020 Efabless Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// SPDX-License-Identifier: Apache-2.0

`default_nettype none
/*
 *-------------------------------------------------------------
 *
 * user_project_la_example
 *
 * This is a user project for testing the gpio testing only 
 *
 *-------------------------------------------------------------
 */
`ifndef AHB
module user_project_gpio_example (
    // Wishbone Slave ports (WB MI A)
    input wb_clk_i,
    input wb_rst_i,
    input wbs_stb_i,
    input wbs_cyc_i,
    input wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output reg wbs_ack_o,
    output reg[31:0] wbs_dat_o,

    // IOs
    input  [`MPRJ_IO_PADS-1:0] io_in,
    output [`MPRJ_IO_PADS-1:0] io_out,
    output [`MPRJ_IO_PADS-1:0] io_oeb

);
    reg [31:0] io_l;
    reg [5:0] io_h;
    reg [31:0] oeb_l;
    reg [5:0] oeb_h;

     always @(posedge wb_clk_i or posedge wb_rst_i) begin
        if (wb_rst_i) begin
            io_l <=0;
            io_h <=0;
            oeb_l <=0;
            oeb_h <=0;
            wbs_dat_o   <=0;
            wbs_ack_o   <=0;

        end else if (wbs_cyc_i && wbs_stb_i && wbs_we_i && !wbs_ack_o && (wbs_adr_i[31:0]==32'h300FFFF4||wbs_adr_i[31:0]==32'h300FFFF0||wbs_adr_i[31:0]==32'h300FFFEC||wbs_adr_i[31:0]==32'h300FFFE8))begin // write
            // write to io_l
            io_l[7:0]    <= ((wbs_adr_i[31:0]==32'h300FFFF0) && wbs_sel_i[0])?  wbs_dat_i[7:0]   :io_l[7:0];
            io_l[15:8]   <= ((wbs_adr_i[31:0]==32'h300FFFF0) && wbs_sel_i[1])?  wbs_dat_i[15:8]  :io_l[15:8];
            io_l[23:16]  <= ((wbs_adr_i[31:0]==32'h300FFFF0) && wbs_sel_i[2])?  wbs_dat_i[23:16] :io_l[23:16];
            io_l[31:24]  <= ((wbs_adr_i[31:0]==32'h300FFFF0) && wbs_sel_i[3])?  wbs_dat_i[31:24] :io_l[31:24];
            // io_h
            io_h[5:0]  <= ((wbs_adr_i[31:0]==32'h300FFFF4) && wbs_sel_i[0])?  wbs_dat_i[5:0] :io_h[5:0];
            // oeb_l
            oeb_l[7:0]    <= ((wbs_adr_i[31:0]==32'h300FFFEC) && wbs_sel_i[0])?  wbs_dat_i[7:0]   :oeb_l[7:0];
            oeb_l[15:8]   <= ((wbs_adr_i[31:0]==32'h300FFFEC) && wbs_sel_i[1])?  wbs_dat_i[15:8]  :oeb_l[15:8];
            oeb_l[23:16]  <= ((wbs_adr_i[31:0]==32'h300FFFEC) && wbs_sel_i[2])?  wbs_dat_i[23:16] :oeb_l[23:16];
            oeb_l[31:24]  <= ((wbs_adr_i[31:0]==32'h300FFFEC) && wbs_sel_i[3])?  wbs_dat_i[31:24] :oeb_l[31:24];
            // oeb_h
            oeb_h[7:0]    <= ((wbs_adr_i[31:0]==32'h300FFFE8) && wbs_sel_i[0])?  wbs_dat_i[7:0]   :oeb_h[7:0];
            oeb_h[15:8]   <= ((wbs_adr_i[31:0]==32'h300FFFE8) && wbs_sel_i[1])?  wbs_dat_i[15:8]  :oeb_h[15:8];
            oeb_h[23:16]  <= ((wbs_adr_i[31:0]==32'h300FFFE8) && wbs_sel_i[2])?  wbs_dat_i[23:16] :oeb_h[23:16];
            oeb_h[31:24]  <= ((wbs_adr_i[31:0]==32'h300FFFE8) && wbs_sel_i[3])?  wbs_dat_i[31:24] :oeb_h[31:24];

            wbs_ack_o <= 1;
        end else if (wbs_cyc_i && wbs_stb_i && !wbs_we_i && !wbs_ack_o && (wbs_adr_i[31:0]==32'h300FFFF4||wbs_adr_i[31:0]==32'h300FFFF0||wbs_adr_i[31:0]==32'h300FFFEC||wbs_adr_i[31:0]==32'h300FFFE8)) begin // read 
            wbs_dat_o <= (wbs_adr_i[31:0]==32'h300FFFF0)? io_in[31:0] :(wbs_adr_i[31:0]==32'h300FFFF4)? io_in[`MPRJ_IO_PADS-1:32] : (wbs_adr_i[31:0]==32'h300FFFEC) ? io_oeb[31:0]: io_oeb[37:32]; 
            wbs_ack_o <= 1;
        end else begin 
            wbs_ack_o <= 0;
            wbs_dat_o <= 0;
        end
    end
   
    assign io_out = {io_h,io_l};
    assign io_oeb = {oeb_h,oeb_l};

endmodule
`else // not AHB 
module user_project_gpio_example (    
    input   wire            HCLK,
    input   wire            HRESETn,
    input   wire            HSEL,
    input   wire [31:0]     HADDR,
    input   wire [1:0]      HTRANS,
    input   wire [31:0]     HWDATA,
    input   wire            HWRITE,
    input   wire            HREADY,
    output  wire [31:0]     HRDATA,
    // IOs
    input  [`MPRJ_IO_PADS-1:0] io_in,
    output [`MPRJ_IO_PADS-1:0] io_out,
    output [`MPRJ_IO_PADS-1:0] io_oeb
);
    // regs offset
    localparam [23:0]       GPIO_LOW_OFF      = 24'hFFFFF4,
                            GPIO_HIGH_OFF     = 24'hFFFFF0,
                            GPIO_LOW_OEB_OFF  = 24'hFFFFEC,
                            GPIO_HIGH_OEB_OFF = 24'hFFFFE8;
    `AHB_SLAVE_EPILOGUE()
   
    // initial value is outbut disable
    `AHB_DEBUG_REG(gpio_low,32,GPIO_LOW_OFF,0,)
    `AHB_DEBUG_REG(gpio_low_oeb,32,GPIO_LOW_OEB_OFF,FFFFFFFF,)
    `AHB_DEBUG_REG(gpio_high,6,GPIO_HIGH_OFF,0,)
    `AHB_DEBUG_REG(gpio_high_oeb,6,GPIO_HIGH_OEB_OFF,3F,) 

    
    assign HRDATA[31:0] =   `AHB_DEBUG_REG_READ(io_in[32:0], GPIO_LOW_OFF) 
                            `AHB_DEBUG_REG_READ(gpio_low_oeb, GPIO_LOW_OEB_OFF) 
                            `AHB_DEBUG_REG_READ(io_in[37:32], GPIO_HIGH_OFF) 
                            `AHB_DEBUG_REG_READ(gpio_high_oeb, GPIO_HIGH_OEB_OFF) 
                            32'h0;           
    assign io_out = {gpio_high,gpio_low};
    assign io_oeb = {gpio_high_oeb,gpio_low_oeb};

endmodule
`endif
`default_nettype wire
