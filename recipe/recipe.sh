#!/usr/bin/env bash

# CMSSW packages
pushd $CMSSW_BASE/src

# IDs
# https://twiki.cern.ch/twiki/bin/view/CMS/HEEPElectronIdentificationRun2
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariatePhotonIdentificationRun2
git cms-merge-topic lsoffi:CMSSW_9_4_0_pre3_TnP
git cms-merge-topic guitargeek:ElectronID_MVA2017_940pre3

# needed for MVA
pushd $CMSSW_BASE/external/$SCRAM_ARCH

git clone https://github.com/lsoffi/RecoEgamma-PhotonIdentification.git data/RecoEgamma/PhotonIdentification/data
pushd data/RecoEgamma/PhotonIdentification/data
git checkout CMSSW_9_4_0_pre3_TnP
popd

git clone https://github.com/lsoffi/RecoEgamma-ElectronIdentification.git data/RecoEgamma/ElectronIdentification/data
pushd data/RecoEgamma/ElectronIdentification/data
git checkout CMSSW_9_4_0_pre3_TnP
popd

popd


# Consistent EGMRegression and EGMSmearer
# TODO: update to 94X
# https://twiki.cern.ch/twiki/bin/view/CMS/EGMRegression
# https://twiki.cern.ch/twiki/bin/view/CMS/EGMSmearer
#git cms-merge-topic cms-egamma:EGM_gain_v1
#pushd EgammaAnalysis/ElectronTools/data
#git clone -b Moriond17_gainSwitch_unc https://github.com/ECALELFS/ScalesSmearings.git
#popd

# MET
# Not needed in 94X
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription

popd

