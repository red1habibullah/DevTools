#!/usr/bin/env bash

# CMSSW packages
pushd $CMSSW_BASE/src

# Bad muon filter
git cms-merge-topic gpetruc:badMuonFilters_80X_v2

# IDs
# https://twiki.cern.ch/twiki/bin/view/CMS/HEEPElectronIdentificationRun2
git cms-merge-topic Sam-Harper:HEEPV70VID_8010_ReducedCheckout
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2
# integrated in 8_0_26
#git cms-merge-topic ikrav:egm_id_80X_v2
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2
git cms-merge-topic ikrav:egm_id_80X_v3_photons

# no longer needed since 8_0_25
## MVA
#pushd $CMSSW_BASE/external/$SCRAM_ARCH
#
## https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
## integrated in 8_0_25
#git clone https://github.com/ikrav/RecoEgamma-ElectronIdentification.git data/RecoEgamma/ElectronIdentification/data
#pushd data/RecoEgamma/ElectronIdentification/data
#git checkout egm_id_80X_v1
#popd
#
## https://twiki.cern.ch/twiki/bin/view/CMS/MultivariatePhotonIdentificationRun2
#git clone https://github.com/ikrav/RecoEgamma-PhotonIdentification.git data/RecoEgamma/PhotonIdentification/data
#pushd data/RecoEgamma/PhotonIdentification/data
#git checkout egm_id_80X_v1
#popd
#
#popd

# EGMRegressions
# https://twiki.cern.ch/twiki/bin/view/CMS/EGMRegression
git cms-merge-topic rafaellopesdesa:EgammaAnalysis80_EGMSmearer_Moriond17_23Jan
pushd EgammaAnalysis/ElectronTools/data
git clone https://github.com/ECALELFS/ScalesSmearings.git
popd

# EGMSmearer
# https://twiki.cern.ch/twiki/bin/view/CMS/EGMSmearer
# included in EGMRegression merge
#git cms-merge-topic shervin86:Moriond17_23Jan
#pushd EgammaAnalysis/ElectronTools/data
#git clone https://github.com/ECALELFS/ScalesSmearings.git
#git checkout Moriond17_23Jan_v1
#popd

# MET
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
git cms-merge-topic -u cms-met:fromCMSSW_8_0_20_postICHEPfilter
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription
git cms-merge-topic cms-met:METRecipe_8020

popd

