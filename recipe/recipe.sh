#!/usr/bin/env bash

# CMSSW packages
pushd $CMSSW_BASE/src
#git cms-merge-topic -u matteosan1:smearer_76X
git cms-merge-topic -u cms-met:CMSSW_8_0_X-METFilterUpdate
echo /PhysicsTools/PatUtils/ >> .git/info/sparse-checkout
git cms-merge-topic cms-met:metTool80X
popd

