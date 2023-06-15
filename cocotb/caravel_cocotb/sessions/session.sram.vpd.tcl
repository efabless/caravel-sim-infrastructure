# Begin_DVE_Session_Save_Info
# DVE full session
# Saved on Tue Nov 22 05:22:59 2022
# Designs open: 1
#   V1: sim/run1/RTL-helloWorld/helloWorld.vpd
# Toplevel windows open: 2
# 	TopLevel.1
# 	TopLevel.2
#   Source.1: caravel_top.uut.soc.core.sram.ram512x32.RAM00
#   Wave.1: 53 signals
#   Group count = 10
#   Group Group1 signal count = 12
#   Group Group2 signal count = 17
#   Group Group3 signal count = 13
#   Group Group4 signal count = 2
#   Group Group5 signal count = 0
#   Group Group6 signal count = 1
#   Group Group7 signal count = 1
#   Group Group8 signal count = 1
#   Group Group9 signal count = 6
#   Group Drivers: V1:caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q[7:0]@240436000 signal count = 10
# End_DVE_Session_Save_Info

# DVE version: T-2022.06_Full64
# DVE build date: May 31 2022 20:53:03


#<Session mode="Full" path="/home/rady/caravel/caravel_gf/caravel/verilog/dv/caravel-dynamic-sims/cocotb/session.helloWorld.vpd.tcl" type="Debug">

gui_set_loading_session_type Post
gui_continuetime_set

# Close design
if { [gui_sim_state -check active] } {
    gui_sim_terminate
}
gui_close_db -all
gui_expr_clear_all

# Close all windows
gui_close_window -type Console
gui_close_window -type Wave
gui_close_window -type Source
gui_close_window -type Schematic
gui_close_window -type Data
gui_close_window -type DriverLoad
gui_close_window -type List
gui_close_window -type Memory
gui_close_window -type HSPane
gui_close_window -type DLPane
gui_close_window -type Assertion
gui_close_window -type CovHier
gui_close_window -type CoverageTable
gui_close_window -type CoverageMap
gui_close_window -type CovDetail
gui_close_window -type Local
gui_close_window -type Stack
gui_close_window -type Watch
gui_close_window -type Group
gui_close_window -type Transaction



# Application preferences
gui_set_pref_value -key app_default_font -value {Helvetica,10,-1,5,50,0,0,0,0,0}
gui_src_preferences -tabstop 8 -maxbits 24 -windownumber 1
#<WindowLayout>

# DVE top-level session


# Create and position top-level window: TopLevel.1

if {![gui_exist_window -window TopLevel.1]} {
    set TopLevel.1 [ gui_create_window -type TopLevel \
       -icon $::env(DVE)/auxx/gui/images/toolbars/dvewin.xpm] 
} else { 
    set TopLevel.1 TopLevel.1
}
gui_show_window -window ${TopLevel.1} -show_state minimized -rect {{0 29} {2559 1336}}

# ToolBar settings
gui_set_toolbar_attributes -toolbar {TimeOperations} -dock_state top
gui_set_toolbar_attributes -toolbar {TimeOperations} -offset 0
gui_show_toolbar -toolbar {TimeOperations}
gui_hide_toolbar -toolbar {&File}
gui_set_toolbar_attributes -toolbar {&Edit} -dock_state top
gui_set_toolbar_attributes -toolbar {&Edit} -offset 0
gui_show_toolbar -toolbar {&Edit}
gui_hide_toolbar -toolbar {CopyPaste}
gui_set_toolbar_attributes -toolbar {&Trace} -dock_state top
gui_set_toolbar_attributes -toolbar {&Trace} -offset 0
gui_show_toolbar -toolbar {&Trace}
gui_hide_toolbar -toolbar {TraceInstance}
gui_hide_toolbar -toolbar {BackTrace}
gui_set_toolbar_attributes -toolbar {&Scope} -dock_state top
gui_set_toolbar_attributes -toolbar {&Scope} -offset 0
gui_show_toolbar -toolbar {&Scope}
gui_set_toolbar_attributes -toolbar {&Window} -dock_state top
gui_set_toolbar_attributes -toolbar {&Window} -offset 0
gui_show_toolbar -toolbar {&Window}
gui_set_toolbar_attributes -toolbar {Signal} -dock_state top
gui_set_toolbar_attributes -toolbar {Signal} -offset 0
gui_show_toolbar -toolbar {Signal}
gui_set_toolbar_attributes -toolbar {Zoom} -dock_state top
gui_set_toolbar_attributes -toolbar {Zoom} -offset 0
gui_show_toolbar -toolbar {Zoom}
gui_set_toolbar_attributes -toolbar {Zoom And Pan History} -dock_state top
gui_set_toolbar_attributes -toolbar {Zoom And Pan History} -offset 0
gui_show_toolbar -toolbar {Zoom And Pan History}
gui_set_toolbar_attributes -toolbar {Grid} -dock_state top
gui_set_toolbar_attributes -toolbar {Grid} -offset 0
gui_show_toolbar -toolbar {Grid}
gui_hide_toolbar -toolbar {Simulator}
gui_hide_toolbar -toolbar {Interactive Rewind}
gui_hide_toolbar -toolbar {Testbench}

# End ToolBar settings

# Docked window settings
set HSPane.1 [gui_create_window -type HSPane -parent ${TopLevel.1} -dock_state left -dock_on_new_line true -dock_extent 437]
catch { set Hier.1 [gui_share_window -id ${HSPane.1} -type Hier] }
gui_set_window_pref_key -window ${HSPane.1} -key dock_width -value_type integer -value 437
gui_set_window_pref_key -window ${HSPane.1} -key dock_height -value_type integer -value -1
gui_set_window_pref_key -window ${HSPane.1} -key dock_offset -value_type integer -value 0
gui_update_layout -id ${HSPane.1} {{left 0} {top 0} {width 436} {height 924} {dock_state left} {dock_on_new_line true} {child_hier_colhier 344} {child_hier_coltype 107} {child_hier_colpd 0} {child_hier_col1 0} {child_hier_col2 1} {child_hier_col3 -1}}
set DLPane.1 [gui_create_window -type DLPane -parent ${TopLevel.1} -dock_state left -dock_on_new_line true -dock_extent 379]
catch { set Data.1 [gui_share_window -id ${DLPane.1} -type Data] }
gui_set_window_pref_key -window ${DLPane.1} -key dock_width -value_type integer -value 379
gui_set_window_pref_key -window ${DLPane.1} -key dock_height -value_type integer -value 923
gui_set_window_pref_key -window ${DLPane.1} -key dock_offset -value_type integer -value 0
gui_update_layout -id ${DLPane.1} {{left 0} {top 0} {width 378} {height 924} {dock_state left} {dock_on_new_line true} {child_data_colvariable 515} {child_data_colvalue 96} {child_data_coltype 64} {child_data_col1 0} {child_data_col2 1} {child_data_col3 2}}
set Console.1 [gui_create_window -type Console -parent ${TopLevel.1} -dock_state bottom -dock_on_new_line true -dock_extent 303]
gui_set_window_pref_key -window ${Console.1} -key dock_width -value_type integer -value -1
gui_set_window_pref_key -window ${Console.1} -key dock_height -value_type integer -value 303
gui_set_window_pref_key -window ${Console.1} -key dock_offset -value_type integer -value 0
gui_update_layout -id ${Console.1} {{left 0} {top 0} {width 295} {height 302} {dock_state bottom} {dock_on_new_line true}}
set DriverLoad.1 [gui_create_window -type DriverLoad -parent ${TopLevel.1} -dock_state bottom -dock_on_new_line false -dock_extent 180]
gui_set_window_pref_key -window ${DriverLoad.1} -key dock_width -value_type integer -value 150
gui_set_window_pref_key -window ${DriverLoad.1} -key dock_height -value_type integer -value 180
gui_set_window_pref_key -window ${DriverLoad.1} -key dock_offset -value_type integer -value 0
gui_update_layout -id ${DriverLoad.1} {{left 0} {top 0} {width 2263} {height 302} {dock_state bottom} {dock_on_new_line false}}
#### Start - Readjusting docked view's offset / size
set dockAreaList { top left right bottom }
foreach dockArea $dockAreaList {
  set viewList [gui_ekki_get_window_ids -active_parent -dock_area $dockArea]
  foreach view $viewList {
      if {[lsearch -exact [gui_get_window_pref_keys -window $view] dock_width] != -1} {
        set dockWidth [gui_get_window_pref_value -window $view -key dock_width]
        set dockHeight [gui_get_window_pref_value -window $view -key dock_height]
        set offset [gui_get_window_pref_value -window $view -key dock_offset]
        if { [string equal "top" $dockArea] || [string equal "bottom" $dockArea]} {
          gui_set_window_attributes -window $view -dock_offset $offset -width $dockWidth
        } else {
          gui_set_window_attributes -window $view -dock_offset $offset -height $dockHeight
        }
      }
  }
}
#### End - Readjusting docked view's offset / size
gui_sync_global -id ${TopLevel.1} -option true

# MDI window settings
set Source.1 [gui_create_window -type {Source}  -parent ${TopLevel.1}]
gui_show_window -window ${Source.1} -show_state maximized
gui_update_layout -id ${Source.1} {{show_state maximized} {dock_state undocked} {dock_on_new_line false}}

# End MDI window settings


# Create and position top-level window: TopLevel.2

if {![gui_exist_window -window TopLevel.2]} {
    set TopLevel.2 [ gui_create_window -type TopLevel \
       -icon $::env(DVE)/auxx/gui/images/toolbars/dvewin.xpm] 
} else { 
    set TopLevel.2 TopLevel.2
}
gui_show_window -window ${TopLevel.2} -show_state maximized -rect {{0 29} {2559 1336}}

# ToolBar settings
gui_set_toolbar_attributes -toolbar {TimeOperations} -dock_state top
gui_set_toolbar_attributes -toolbar {TimeOperations} -offset 0
gui_show_toolbar -toolbar {TimeOperations}
gui_hide_toolbar -toolbar {&File}
gui_set_toolbar_attributes -toolbar {&Edit} -dock_state top
gui_set_toolbar_attributes -toolbar {&Edit} -offset 0
gui_show_toolbar -toolbar {&Edit}
gui_hide_toolbar -toolbar {CopyPaste}
gui_set_toolbar_attributes -toolbar {&Trace} -dock_state top
gui_set_toolbar_attributes -toolbar {&Trace} -offset 0
gui_show_toolbar -toolbar {&Trace}
gui_hide_toolbar -toolbar {TraceInstance}
gui_hide_toolbar -toolbar {BackTrace}
gui_set_toolbar_attributes -toolbar {&Scope} -dock_state top
gui_set_toolbar_attributes -toolbar {&Scope} -offset 0
gui_show_toolbar -toolbar {&Scope}
gui_set_toolbar_attributes -toolbar {&Window} -dock_state top
gui_set_toolbar_attributes -toolbar {&Window} -offset 0
gui_show_toolbar -toolbar {&Window}
gui_set_toolbar_attributes -toolbar {Signal} -dock_state top
gui_set_toolbar_attributes -toolbar {Signal} -offset 0
gui_show_toolbar -toolbar {Signal}
gui_set_toolbar_attributes -toolbar {Zoom} -dock_state top
gui_set_toolbar_attributes -toolbar {Zoom} -offset 0
gui_show_toolbar -toolbar {Zoom}
gui_set_toolbar_attributes -toolbar {Zoom And Pan History} -dock_state top
gui_set_toolbar_attributes -toolbar {Zoom And Pan History} -offset 0
gui_show_toolbar -toolbar {Zoom And Pan History}
gui_set_toolbar_attributes -toolbar {Grid} -dock_state top
gui_set_toolbar_attributes -toolbar {Grid} -offset 0
gui_show_toolbar -toolbar {Grid}
gui_hide_toolbar -toolbar {Simulator}
gui_hide_toolbar -toolbar {Interactive Rewind}
gui_hide_toolbar -toolbar {Testbench}

# End ToolBar settings

# Docked window settings
gui_sync_global -id ${TopLevel.2} -option true

# MDI window settings
set Wave.1 [gui_create_window -type {Wave}  -parent ${TopLevel.2}]
gui_show_window -window ${Wave.1} -show_state maximized
gui_update_layout -id ${Wave.1} {{show_state maximized} {dock_state undocked} {dock_on_new_line false} {child_wave_left 743} {child_wave_right 1811} {child_wave_colname 446} {child_wave_colvalue 293} {child_wave_col1 0} {child_wave_col2 1}}

# End MDI window settings

gui_set_env TOPLEVELS::TARGET_FRAME(Source) ${TopLevel.1}
gui_set_env TOPLEVELS::TARGET_FRAME(Schematic) ${TopLevel.1}
gui_set_env TOPLEVELS::TARGET_FRAME(PathSchematic) ${TopLevel.1}
gui_set_env TOPLEVELS::TARGET_FRAME(Wave) none
gui_set_env TOPLEVELS::TARGET_FRAME(List) none
gui_set_env TOPLEVELS::TARGET_FRAME(Memory) ${TopLevel.1}
gui_set_env TOPLEVELS::TARGET_FRAME(DriverLoad) none
gui_update_statusbar_target_frame ${TopLevel.1}
gui_update_statusbar_target_frame ${TopLevel.2}

#</WindowLayout>

#<Database>

# DVE Open design session: 

if { ![gui_is_db_opened -db {sim/run1/RTL-helloWorld/helloWorld.vpd}] } {
	gui_open_db -design V1 -file sim/run1/RTL-helloWorld/helloWorld.vpd -to 846631000 -nosource
}
gui_set_precision 1ps
gui_set_time_units 1ns
#</Database>

# DVE Global setting session: 


# Global: Bus

# Global: Expressions

# Global: Signal Time Shift

# Global: Signal Compare

# Global: Signal Groups
gui_load_child_values {caravel_top.uut.soc.core.sram}
gui_load_child_values {caravel_top.uut.soc.core.sram.ram512x32}


set _session_group_70 Group1
gui_sg_create "$_session_group_70"
set Group1 "$_session_group_70"

gui_sg_addsignal -group "$_session_group_70" { caravel_top.uut.mprj.debug.debug_reg_1 caravel_top.uut.soc.core.sram.clk0 caravel_top.uut.soc.core.sram.csb0 caravel_top.uut.soc.core.sram.web0 caravel_top.uut.soc.core.sram.wmask0 caravel_top.uut.soc.core.sram.addr0 caravel_top.uut.soc.core.sram.din0 caravel_top.uut.soc.core.sram.dout0 caravel_top.uut.soc.core.slave_sel caravel_top.uut.soc.core.slave_sel_r caravel_top.uut.soc.core.VexRiscv.dBusWishbone_ADR caravel_top.uut.soc.core.VexRiscv.dBusWishbone_DAT_MOSI }

set _session_group_71 Group2
gui_sg_create "$_session_group_71"
set Group2 "$_session_group_71"

gui_sg_addsignal -group "$_session_group_71" { caravel_top.uut.soc.core.sram.ram512x32.CLK caravel_top.uut.soc.core.sram.ram512x32.CEN caravel_top.uut.soc.core.sram.ram512x32.GWEN caravel_top.uut.soc.core.sram.ram512x32.WEN caravel_top.uut.soc.core.sram.ram512x32.A caravel_top.uut.soc.core.sram.ram512x32.D caravel_top.uut.soc.core.sram.ram512x32.Q caravel_top.uut.soc.core.sram.ram512x32.VDD caravel_top.uut.soc.core.sram.ram512x32.VSS caravel_top.uut.soc.core.sram.ram512x32.Q0 caravel_top.uut.soc.core.sram.ram512x32.Q1 caravel_top.uut.soc.core.sram.ram512x32.sel_0 caravel_top.uut.soc.core.sram.ram512x32.gwen_0 caravel_top.uut.soc.core.sram.ram512x32.wen_0 caravel_top.uut.soc.core.sram.ram512x32.wen_1 caravel_top.uut.soc.core.sram.ram512x32.wen_2 caravel_top.uut.soc.core.sram.ram512x32.wen_3 }

set _session_group_72 Group3
gui_sg_create "$_session_group_72"
set Group3 "$_session_group_72"

gui_sg_addsignal -group "$_session_group_72" { caravel_top.uut.soc.core.sram.ram512x32.RAM00.clk_dly caravel_top.uut.soc.core.sram.ram512x32.RAM00.write_flag caravel_top.uut.soc.core.sram.ram512x32.RAM00.no_st_viol caravel_top.uut.soc.core.sram.ram512x32.RAM00.read_flag caravel_top.uut.soc.core.sram.ram512x32.RAM00.write_flag_dly caravel_top.uut.soc.core.sram.ram512x32.RAM00.cen_fell caravel_top.uut.soc.core.sram.ram512x32.RAM00.CEN caravel_top.uut.soc.core.sram.ram512x32.RAM00.GWEN caravel_top.uut.soc.core.sram.ram512x32.RAM00.WEN caravel_top.uut.soc.core.sram.ram512x32.RAM00.cd5 caravel_top.uut.soc.core.sram.ram512x32.RAM00.A caravel_top.uut.soc.core.sram.ram512x32.RAM00.marked_a caravel_top.uut.soc.core.sram.ram512x32.RAM00.qo_reg }

set _session_group_73 Group4
gui_sg_create "$_session_group_73"
set Group4 "$_session_group_73"

gui_sg_addsignal -group "$_session_group_73" { caravel_top.uut.soc.core.shared_dat_w caravel_top.uut.soc.core.shared_dat_r }

set _session_group_74 Group5
gui_sg_create "$_session_group_74"
set Group5 "$_session_group_74"


set _session_group_75 Group6
gui_sg_create "$_session_group_75"
set Group6 "$_session_group_75"

gui_sg_addsignal -group "$_session_group_75" { caravel_top.uut.soc.core.mgmtsoc_dbus_dbus_dat_r }

set _session_group_76 Group7
gui_sg_create "$_session_group_76"
set Group7 "$_session_group_76"

gui_sg_addsignal -group "$_session_group_76" { caravel_top.uut.soc.core.VexRiscv.writeBack_MEMORY_READ_DATA }

set _session_group_77 Group8
gui_sg_create "$_session_group_77"
set Group8 "$_session_group_77"

gui_sg_addsignal -group "$_session_group_77" { caravel_top.uut.soc.core.VexRiscv.writeBack_MEMORY_ADDRESS_LOW }

set _session_group_78 Group9
gui_sg_create "$_session_group_78"
set Group9 "$_session_group_78"

gui_sg_addsignal -group "$_session_group_78" { caravel_top.uut.soc.core.VexRiscv.writeBack_DBusSimplePlugin_rspShifted caravel_top.uut.soc.core.VexRiscv._zz_writeBack_DBusSimplePlugin_rspFormated caravel_top.uut.soc.core.VexRiscv.writeBack_DBusSimplePlugin_rspFormated caravel_top.uut.soc.core.VexRiscv.dBusWishbone_ACK caravel_top.uut.soc.core.sram.ram512x32.RAM00.qo_reg caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q }

set _session_group_79 {Drivers: V1:caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q[7:0]@240436000}
gui_sg_create "$_session_group_79"
set {Drivers: V1:caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q[7:0]@240436000} "$_session_group_79"

gui_sg_addsignal -group "$_session_group_79" { caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q caravel_top.uut.soc.core.sram.ram512x32.RAM00.qo_reg caravel_top.uut.soc.core.sram.ram512x32.RAM00.cdx caravel_top.uut.soc.core.sram.ram512x32.RAM00.no_st_viol caravel_top.uut.soc.core.sram.ram512x32.RAM00.marked_a caravel_top.uut.soc.core.sram.ram512x32.RAM00.A caravel_top.uut.soc.core.sram.ram512x32.RAM00.read_flag caravel_top.uut.soc.core.sram.ram512x32.RAM00.write_flag caravel_top.uut.soc.core.sram.ram512x32.RAM00.ntf_twh caravel_top.uut.soc.core.sram.ram512x32.RAM00.write_flag_dly }

# Global: Highlighting

# Global: Stack
gui_change_stack_mode -mode list

# Post database loading setting...

# Restore C1 time
gui_set_time -C1_only 272701.1



# Save global setting...

# Wave/List view global setting
gui_list_create_group_when_add -list -enable
gui_cov_show_value -switch false

# Close all empty TopLevel windows
foreach __top [gui_ekki_get_window_ids -type TopLevel] {
    if { [llength [gui_ekki_get_window_ids -parent $__top]] == 0} {
        gui_close_window -window $__top
    }
}
gui_set_loading_session_type noSession
# DVE View/pane content session: 


# Hier 'Hier.1'
gui_show_window -window ${Hier.1}
gui_list_set_filter -id ${Hier.1} -list { {Package 1} {All 0} {Process 1} {VirtPowSwitch 0} {UnnamedProcess 1} {UDP 0} {Function 1} {Block 1} {SrsnAndSpaCell 0} {OVA Unit 1} {LeafScCell 1} {LeafVlgCell 1} {Interface 1} {LeafVhdCell 1} {$unit 1} {NamedBlock 1} {Task 1} {VlgPackage 1} {ClassDef 1} {VirtIsoCell 0} }
gui_list_set_filter -id ${Hier.1} -text {*}
gui_hier_list_init -id ${Hier.1}
gui_change_design -id ${Hier.1} -design V1
catch {gui_list_expand -id ${Hier.1} caravel_top}
catch {gui_list_expand -id ${Hier.1} caravel_top.uut}
catch {gui_list_select -id ${Hier.1} {caravel_top.uut}}
gui_view_scroll -id ${Hier.1} -vertical -set 0
gui_view_scroll -id ${Hier.1} -horizontal -set 0

# Data 'Data.1'
gui_list_set_filter -id ${Data.1} -list { {Buffer 1} {Input 1} {Others 1} {Linkage 1} {Output 1} {LowPower 1} {Parameter 1} {All 1} {Aggregate 1} {LibBaseMember 1} {Event 1} {Assertion 1} {Constant 1} {Interface 1} {BaseMembers 1} {Signal 1} {$unit 1} {Inout 1} {Variable 1} }
gui_list_set_filter -id ${Data.1} -text {dBusWishbone_ACK}
gui_list_show_data -id ${Data.1} {caravel_top.uut}
gui_view_scroll -id ${Data.1} -vertical -set 0
gui_view_scroll -id ${Data.1} -horizontal -set 0
gui_view_scroll -id ${Hier.1} -vertical -set 0
gui_view_scroll -id ${Hier.1} -horizontal -set 0

# Source 'Source.1'
gui_src_value_annotate -id ${Source.1} -switch false
gui_set_env TOGGLE::VALUEANNOTATE 0
gui_open_source -id ${Source.1}  -replace -active caravel_top.uut.soc.core.sram.ram512x32.RAM00 /home/rady/caravel/files4vcs/pdk/gf180mcuC/libs.ref/gf180mcu_fd_ip_sram/verilog/gf180mcu_fd_ip_sram__sram512x8m8wm1.v
gui_src_value_annotate -id ${Source.1} -switch true
gui_set_env TOGGLE::VALUEANNOTATE 1
gui_view_scroll -id ${Source.1} -vertical -set 1248
gui_src_set_reusable -id ${Source.1}

# View 'Wave.1'
gui_wv_sync -id ${Wave.1} -switch false
set groupExD [gui_get_pref_value -category Wave -key exclusiveSG]
gui_set_pref_value -category Wave -key exclusiveSG -value {false}
set origWaveHeight [gui_get_pref_value -category Wave -key waveRowHeight]
gui_list_set_height -id Wave -height 25
set origGroupCreationState [gui_list_create_group_when_add -wave]
gui_list_create_group_when_add -wave -disable
gui_marker_set_ref -id ${Wave.1}  C1
gui_wv_zoom_timerange -id ${Wave.1} 0 846631
gui_list_add_group -id ${Wave.1} -after {New Group} {Group1}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group2}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group3}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group4}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group5}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group6}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group7}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group8}
gui_list_add_group -id ${Wave.1} -after {New Group} {Group9}
gui_list_collapse -id ${Wave.1} Group2
gui_list_collapse -id ${Wave.1} Group4
gui_list_collapse -id ${Wave.1} Group6
gui_list_collapse -id ${Wave.1} Group7
gui_list_collapse -id ${Wave.1} Group8
gui_list_expand -id ${Wave.1} caravel_top.uut.soc.core.slave_sel
gui_list_select -id ${Wave.1} {caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q }
gui_seek_criteria -id ${Wave.1} {Value...}



gui_set_env TOGGLE::DEFAULT_WAVE_WINDOW ${Wave.1}
gui_set_pref_value -category Wave -key exclusiveSG -value $groupExD
gui_list_set_height -id Wave -height $origWaveHeight
if {$origGroupCreationState} {
	gui_list_create_group_when_add -wave -enable
}
if { $groupExD } {
 gui_msg_report -code DVWW028
}
gui_list_set_filter -id ${Wave.1} -list { {Buffer 1} {Input 1} {Others 1} {Linkage 1} {Output 1} {Parameter 1} {All 1} {Aggregate 1} {LibBaseMember 1} {Event 1} {Assertion 1} {Constant 1} {Interface 1} {BaseMembers 1} {Signal 1} {$unit 1} {Inout 1} {Variable 1} }
gui_list_set_filter -id ${Wave.1} -text {*}
gui_list_set_insertion_bar  -id ${Wave.1} -group Group9  -position in

gui_marker_move -id ${Wave.1} {C1} 272701.1
gui_view_scroll -id ${Wave.1} -vertical -set 0
gui_show_grid -id ${Wave.1} -enable false

# DriverLoad 'DriverLoad.1'
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.slave_sel[2]} -time 308821 -starttime 308821
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv._zz_dBus_cmd_payload_data[31:0]} -time 305161 -starttime 305191
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.execute_RS2[31:0]} -time 305161 -starttime 305191
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.decode_to_execute_RS2[31:0]} -time 305161 -starttime 305191
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.decode_RS2[31:0]} -time 305131 -starttime 305191
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.decode_RegFilePlugin_rs2Data[31:0]} -time 305131 -starttime 305191
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv._zz_RegFilePlugin_regFile_port1[31:0]} -time 305131 -starttime 305191
gui_get_drivers -session -id ${DriverLoad.1} -signal caravel_top.uut.soc.core.sram.ram512x32.RAM00.write_flag -time 0 -starttime 250613.199
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.mprj.debug.debug_reg_1[31:0]} -time 272881 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.mprj.debug.wbs_dat_i[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.mgmt_buffers.mprj_dat_o_core[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.mprj_dat_w[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.shared_dat_w[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.comb_array_muxed1[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.mgmtsoc_dbus_dbus_dat_w[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.dBus_cmd_halfPipe_payload_data[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.dBus_cmd_rData_data[31:0]} -time 272851 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.dBus_cmd_payload_data[31:0]} -time 272821 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.execute_RS2[31:0]} -time 272821 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.decode_to_execute_RS2[31:0]} -time 272821 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.decode_RS2[31:0]} -time 272791 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.decode_RegFilePlugin_rs2Data[31:0]} -time 272791 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv._zz_RegFilePlugin_regFile_port1[31:0]} -time 272791 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.RegFilePlugin_regFile[0:31][31:0]} -time 272881 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.VexRiscv.lastStageRegFileWrite_payload_data[31:0]} -time 272881 -starttime 272881
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.dout0[31:0]} -time 272746 -starttime 272746
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.ram512x32.Q[31:0]} -time 272746 -starttime 272746
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.ram512x32.Q0[31:0]} -time 272746 -starttime 272746
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q[7:0]} -time 272746 -starttime 272746
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.ram512x32.RAM00.Q[7:0]} -time 240436 -starttime 272701.1
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.ram512x32.RAM00.qo_reg[7:0]} -time 272701.1 -starttime 272716
gui_get_drivers -session -id ${DriverLoad.1} -signal {caravel_top.uut.soc.core.sram.ram512x32.RAM00.qo_reg[7:0]} -time 272701.1 -starttime 272701.1
# Restore toplevel window zorder
# The toplevel window could be closed if it has no view/pane
if {[gui_exist_window -window ${TopLevel.1}]} {
	gui_set_active_window -window ${TopLevel.1}
	gui_set_active_window -window ${Source.1}
	gui_set_active_window -window ${HSPane.1}
}
if {[gui_exist_window -window ${TopLevel.2}]} {
	gui_set_active_window -window ${TopLevel.2}
	gui_set_active_window -window ${Wave.1}
}
#</Session>

