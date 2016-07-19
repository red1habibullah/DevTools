#!/usr/bin/env bash

# CMSSW packages
pushd $CMSSW_BASE/src

# MET
git cms-merge-topic -u cms-met:CMSSW_8_0_X-METFilterUpdate
echo /PhysicsTools/PatUtils/ >> .git/info/sparse-checkout
git cms-merge-topic cms-met:metTool80X

# EGMSmearer
git remote add -f -t ecal_smear_fix_80X emanueledimarco https://github.com/emanueledimarco/cmssw.git
git cms-addpkg EgammaAnalysis/ElectronTools
git checkout -b from-277de3c 277de3c

# download the txt files with the corrections
pushd EgammaAnalysis/ElectronTools/data
# corrections calculated with the first 4/fb of 2016 data
#git clone -b ICHEP2016_approval_4fb https://github.com/ECALELFS/ScalesSmearings.git
# or, alternatively, corrections calculated with first 7.65/fb of 2016 data
git clone -b ICHEP2016_approval_7p65fb https://github.com/emanueledimarco/ScalesSmearings.git
popd

popd

