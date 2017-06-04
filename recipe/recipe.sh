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
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2
git cms-merge-topic ikrav:egm_id_80X_v3_photons

# MVA
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariatePhotonIdentificationRun2
# integrated in 8_0_25


# Consistent EGMRegression and EGMSmearer
# https://twiki.cern.ch/twiki/bin/view/CMS/EGMRegression
# https://twiki.cern.ch/twiki/bin/view/CMS/EGMSmearer
git cms-merge-topic cms-egamma:EGM_gain_v1
pushd EgammaAnalysis/ElectronTools/data
git clone -b Moriond17_gainSwitch_unc https://github.com/ECALELFS/ScalesSmearings.git
popd

# MET
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
git cms-merge-topic -u cms-met:fromCMSSW_8_0_20_postICHEPfilter
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription
git cms-merge-topic cms-met:METRecipe_8020

popd

