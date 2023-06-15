initial begin
    `ifndef CARAVAN
    `ifdef ARM
    $sdf_annotate({`SDF_PATH,"/",`SDF_POSTFIX,"/swift_caravel.",`CORNER ,".sdf"}, uut,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravel_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `else
    $sdf_annotate({`SDF_PATH,"/",`SDF_POSTFIX,"/caravel.",`CORNER ,".sdf"}, uut,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravel_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `endif //ARM
    `else // CARAVAN
    $sdf_annotate({`SDF_PATH,"/",`SDF_POSTFIX,"/caravan.", `CORNER,".sdf"}, uut,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravan_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `endif

    // `ifdef USER_SDF_ENABLE
    // $sdf_annotate({`USER_PROJECT_ROOT,"/signoff/user_project_wrapper/primetime/sdf/",`SDF_POSTFIX,"/user_project_wrapper.", `CORNER,".sdf"}, uut.chip_core.mprj,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/user_prog_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    // `endif // USER_SDF_ENABLE
end
