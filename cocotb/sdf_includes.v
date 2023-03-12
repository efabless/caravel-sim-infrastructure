initial begin
    `ifndef CARAVAN
    `ifdef ARM
    $sdf_annotate({`CARAVEL_ROOT,"/signoff/swift_caravel/primetime/sdf/",`SDF_POSTFIX,"/swift_caravel.",`CORNER ,".sdf"}, uut,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravel_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `else
    $sdf_annotate({`CARAVEL_ROOT,"/signoff/caravel/primetime/sdf/",`SDF_POSTFIX,"/caravel.",`CORNER ,".sdf"}, uut,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravel_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `endif //ARM
    `else
    $sdf_annotate({`CARAVEL_ROOT,"/signoff/caravan/primetime/sdf/",`SDF_POSTFIX,"/caravan.", `CORNER,".sdf"}, uut,,{`COCOTB_PATH,"/sim/",`TAG,"/",`FTESTNAME,"/caravan_sdf.log"},`ifdef MAX_SDF "MAXIMUM" `else "MINIMUM" `endif ); 
    `endif
end
