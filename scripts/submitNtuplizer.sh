#!/bin/bash
DATE=`date +%Y-%m-%d`
if [ "$1" == "" ]; then
    NAME="$DATE"_DevTools_80X_v1
else
    NAME="$1"
fi
#submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_Data.txt --applyLumiMask "Collisions16" "$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=0 crab=1
#submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_MC.txt "$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1 crab=1
submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/MM_test.txt "$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1 crab=1
#submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_MC_nonvalid.txt --allowNonValid "$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1 crab=1
#submit_job.py crabSubmit --sampleList DevTools/Ntuplizer/data/datasetList_phys03.txt --inputDBS phys03 "$NAME" DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1 crab=1
