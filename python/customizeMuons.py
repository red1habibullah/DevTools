import FWCore.ParameterSet.Config as cms

def customizeMuons(process,coll,**kwargs):
    '''Customize muons'''
    reHLT = kwargs.pop('reHLT',False)
    isMC = kwargs.pop('isMC',False)
    mSrc = coll['muons']
    jSrc = coll['jets']
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']
    pfSrc = coll['packed']

    # customization path
    process.muonCustomization = cms.Path()

    #########################
    ### embed nearest jet ###
    #########################
    process.mJet = cms.EDProducer(
        "MuonJetEmbedder",
        src = cms.InputTag(mSrc),
        jetSrc = cms.InputTag(jSrc),
        dRmax = cms.double(0.4),
        L1Corrector = cms.InputTag("ak4PFCHSL1FastjetCorrector"),
        L1L2L3ResCorrector= cms.InputTag("ak4PFCHSL1FastL2L3Corrector"),
    )
    mSrc = 'mJet'

    process.muonCustomization *= process.mJet

    ###################################
    ### embed rochester corrections ###
    ###################################
    process.mRoch = cms.EDProducer(
        "RochesterCorrectionEmbedder",
        src = cms.InputTag(mSrc),
        isData = cms.bool(not isMC),
    )
    mSrc = 'mRoch'

    process.muonCustomization *= process.mRoch

    #####################
    ### embed muon id ###
    #####################
    process.mID = cms.EDProducer(
        "MuonIdEmbedder",
        src = cms.InputTag(mSrc),
        vertexSrc = cms.InputTag(pvSrc),
    )
    mSrc = 'mID'

    process.muonCustomization *= process.mID

    #################
    ### embed rho ###
    #################
    process.mRho = cms.EDProducer(
        "MuonRhoEmbedder",
        src = cms.InputTag(mSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    mSrc = 'mRho'

    process.muonCustomization *= process.mRho

    ################
    ### embed pv ###
    ################
    process.mPV = cms.EDProducer(
        "MuonIpEmbedder",
        src = cms.InputTag(mSrc),
        vertexSrc = cms.InputTag(pvSrc),
        beamspotSrc = cms.InputTag("offlineBeamSpot"),
    )
    mSrc = 'mPV'

    process.muonCustomization *= process.mPV

    ##############################
    ### embed trigger matching ###
    ##############################
    labels = []
    paths = []
    from triggers import triggerMap
    for trigger in triggerMap:
        if 'muon' in triggerMap[trigger]['objects']:
            labels += ['matches_{0}'.format(trigger)]
            paths += [triggerMap[trigger]['path']]
    process.mTrig = cms.EDProducer(
        "MuonHLTMatchEmbedder",
        src = cms.InputTag(mSrc),
        #triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT2') if reHLT else cms.InputTag('TriggerResults', '', 'HLT'),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        deltaR = cms.double(0.5),
        labels = cms.vstring(*labels),
        paths = cms.vstring(*paths),
    )
    mSrc = 'mTrig'

    process.muonCustomization *= process.mTrig

    #####################
    ### embed HZZ IDs ###
    #####################
    # https://github.com/nwoods/UWVV/blob/ichep/AnalysisTools/python/templates/ZZID.py
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2016
    process.mHZZEmbedder = cms.EDProducer(
        "PATMuonZZIDEmbedder",
        src = cms.InputTag(mSrc),
        vtxSrc = cms.InputTag(pvSrc),
        ptCut = cms.double(5.),
    )
    mSrc = 'mHZZEmbedder'
    process.muonCustomization *= process.mHZZEmbedder

    ######################
    ### embed SUSY IDs ###
    ######################
    # https://twiki.cern.ch/twiki/bin/view/CMS/LeptonMVA
    process.mMiniIsoEmbedder = cms.EDProducer(
        "MuonMiniIsolationEmbedder",
        src = cms.InputTag(mSrc),
        packedSrc = cms.InputTag(pfSrc),
    )
    mSrc = 'mMiniIsoEmbedder'
    process.muonCustomization *= process.mMiniIsoEmbedder

    process.mSUSYEmbedder = cms.EDProducer(
        "MuonSUSYMVAEmbedder",
        src = cms.InputTag(mSrc),
        vertexSrc = cms.InputTag(pvSrc),
        rhoSrc = cms.InputTag('fixedGridRhoFastjetCentralNeutral'),
        weights = cms.FileInPath('DevTools/Ntuplizer/data/susy_mu_BDTG.weights.xml'), # https://github.com/CERN-PH-CMG/cmgtools-lite/blob/80X/TTHAnalysis/data/leptonMVA/tth
    )
    mSrc = 'mSUSYEmbedder'
    process.muonCustomization *= process.mSUSYEmbedder

    # add to schedule
    process.schedule.append(process.muonCustomization)

    coll['muons'] = mSrc

    return coll
