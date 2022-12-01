initial begin
    `ifndef CARAVAN
    $sdf_annotate({`CARAVEL_ROOT,"/signoff/caravel_core/primetime-signoff/sdf/",`SDF_POSTFIX,"/caravel_core.",`CORNER ,".sdf"}, uut.chip_core,,{`MAIN_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravel_core_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `else
    $sdf_annotate({`CARAVEL_ROOT,"/signoff/caravan/primetime-signoff/sdf/",`SDF_POSTFIX,"/caravan.", `CORNER,".sdf"}, uut,,{`MAIN_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravan_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `endif
end
