#!/usr/bin/env bash

# CMSSW packages
pushd $CMSSW_BASE/src

# IDs
git cms-merge-topic ikrav:egm_id_80X_v1

# EGMSmearer
## broken recipe
#git remote add -f -t ecal_smear_fix_80X emanueledimarco https://github.com/emanueledimarco/cmssw.git
#git cms-addpkg EgammaAnalysis/ElectronTools
##git checkout -b from-277de3c 277de3c # old 
#git checkout -b from-52f192a 52f192a # updated full 12.9
# fixed recipe
git cms-merge-topic emanueledimarco:ecal_smear_fix_80X

# download the txt files with the corrections
pushd EgammaAnalysis/ElectronTools/data
# corrections calculated with the first 4/fb of 2016 data
#git clone -b ICHEP2016_approval_4fb https://github.com/ECALELFS/ScalesSmearings.git
# or, alternatively, corrections calculated with first 7.65/fb of 2016 data
#git clone -b ICHEP2016_approval_7p65fb https://github.com/emanueledimarco/ScalesSmearings.git
# corrections calculated with 12.9 fb-1 of 2016 data (ICHEP 16 dataset).
git clone -b ICHEP2016_v2 https://github.com/ECALELFS/ScalesSmearings.git
popd

# MET
git cms-merge-topic -u cms-met:CMSSW_8_0_X-METFilterUpdate
#echo /PhysicsTools/PatUtils/ >> .git/info/sparse-checkout
#git cms-merge-topic cms-met:metTool80X

popd

