#!/usr/bin/env bash

# CMSSW packages
pushd $CMSSW_BASE/src
git cms-merge-topic -u matteosan1:smearer_76X
popd

