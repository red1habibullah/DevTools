import FWCore.ParameterSet.Config as cms

def customizeElectrons(process,coll,**kwargs):
    '''Customize electrons'''
    reHLT = kwargs.pop('reHLT',False)
    isMC = kwargs.pop('isMC',False)
    eSrc = coll['electrons']
    jSrc = coll['jets']
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']
    pfSrc = coll['packed']

    # customization path
    process.electronCustomization = cms.Path()

    ###################################
    ### scale and smear corrections ###
    ###################################
    # embed the uncorrected stuff
    process.uncorElec = cms.EDProducer(
        "ElectronSelfEmbedder",
        src=cms.InputTag(eSrc),
        label=cms.string('uncorrected'),
    )
    eSrc = "uncorElec"
    process.electronCustomization *= process.uncorElec

    # first need to add a manual protection for the corrections
    process.selectedElectrons = cms.EDFilter(
        "PATElectronSelector",
        src = cms.InputTag(eSrc),
        cut = cms.string("pt > 5 && abs(eta)<2.5")
    )
    eSrc = "selectedElectrons"
    process.electronCustomization *= process.selectedElectrons

    process.load('EgammaAnalysis.ElectronTools.calibratedElectronsRun2_cfi')
    process.calibratedPatElectrons.electrons = eSrc
    process.calibratedPatElectrons.isMC = isMC
    process.electronCustomization *= process.calibratedPatElectrons
    eSrc = 'calibratedPatElectrons'

    #################
    ### embed VID ###
    #################
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDElectronIdProducer, setupAllVIDIdsInModule, DataFormat, setupVIDElectronSelection
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    
    # define which IDs we want to produce
    my_id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',
    ]
    
    # add them to the VID producer
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

    # update the collection
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    process.electronMVAValueMapProducer.srcMiniAOD = cms.InputTag(eSrc)
    process.electronRegressionValueMapProducer.srcMiniAOD = cms.InputTag(eSrc)

    idDecisionLabels = [
        'cutBasedElectronID-Summer16-80X-V1-veto',
        'cutBasedElectronID-Summer16-80X-V1-loose',
        'cutBasedElectronID-Summer16-80X-V1-medium',
        'cutBasedElectronID-Summer16-80X-V1-tight',
        'cutBasedElectronHLTPreselection-Summer16-V1',
        'heepElectronID-HEEPV60',
        'mvaEleID-Spring15-25ns-nonTrig-V1-wp80',
        'mvaEleID-Spring15-25ns-nonTrig-V1-wp90',
        'mvaEleID-Spring15-25ns-Trig-V1-wp90',
        'mvaEleID-Spring15-25ns-Trig-V1-wp80',
    ]
    idDecisionTags = [
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1'),
        cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp90'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp80'),
    ]
    fullIDDecisionLabels = [
        'cutBasedElectronID-Summer16-80X-V1-veto',
        'cutBasedElectronID-Summer16-80X-V1-loose',
        'cutBasedElectronID-Summer16-80X-V1-medium',
        'cutBasedElectronID-Summer16-80X-V1-tight',
    ]
    fullIDDecisionTags = [
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight'),
    ]
    nMinusOneIDNames = [
        'GsfEleEffAreaPFIsoCut_0',
    ]
    nMinusOneIDLabels = [
        'NoIso',
    ]
    mvaValueLabels = [
        #"ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values",
        #"ElectronMVAEstimatorRun2Spring15Trig25nsV1Values",
    ]
    mvaValueTags = [
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),
    ]
    mvaCategoryLabels = [
        #"ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories",
        #"ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories",
    ]
    mvaCategoryTags = [
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories"),
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories"),
    ]

    process.eidEmbedder = cms.EDProducer(
        "ElectronVIDEmbedder",
        src=cms.InputTag(eSrc),
        idLabels = cms.vstring(*idDecisionLabels),          # labels for bool maps
        ids = cms.VInputTag(*idDecisionTags),               # bool maps
        fullIDLabels = cms.vstring(*fullIDDecisionLabels),  # labels for bool maps for n-1
        fullIDs = cms.VInputTag(*fullIDDecisionTags),       # bool maps for n-1
        nMinusOneIDNames = cms.vstring(*nMinusOneIDNames),  # n-1 cut names
        nMinusOneIDLabels = cms.vstring(*nMinusOneIDLabels),# n-1 cut labels
        valueLabels = cms.vstring(*mvaValueLabels),         # labels for float maps
        values = cms.VInputTag(*mvaValueTags),              # float maps
        categoryLabels = cms.vstring(*mvaCategoryLabels),   # labels for int maps
        categories = cms.VInputTag(*mvaCategoryTags),       # int maps
    )
    eSrc = 'eidEmbedder'

    process.electronCustomization *= process.egmGsfElectronIDSequence
    process.electronCustomization *= process.eidEmbedder


    #########################
    ### embed nearest jet ###
    #########################
    process.eJet = cms.EDProducer(
        "ElectronJetEmbedder",
        src = cms.InputTag(eSrc),
        jetSrc = cms.InputTag(jSrc),
        dRmax = cms.double(0.4),
        L1Corrector = cms.InputTag("ak4PFCHSL1FastjetCorrector"),
        L1L2L3ResCorrector= cms.InputTag("ak4PFCHSL1FastL2L3Corrector"),
    )
    eSrc = 'eJet'

    process.electronCustomization *= process.eJet

    ##########################
    ### embed missing hits ###
    ##########################
    process.eMissingHits = cms.EDProducer(
        "ElectronMissingHitsEmbedder",
        src = cms.InputTag(eSrc),
    )
    eSrc = 'eMissingHits'

    process.electronCustomization *= process.eMissingHits

    ###################
    ### embed ww id ###
    ###################
    process.eWW = cms.EDProducer(
        "ElectronWWIdEmbedder",
        src = cms.InputTag(eSrc),
        vertexSrc = cms.InputTag(pvSrc),
    )
    eSrc = 'eWW'

    process.electronCustomization *= process.eWW

    #############################
    ### embed effective areas ###
    #############################
    eaFile = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'
    process.eEffArea = cms.EDProducer(
        "ElectronEffectiveAreaEmbedder",
        src = cms.InputTag(eSrc),
        label = cms.string("EffectiveArea"), # embeds a user float with this name
        configFile = cms.FileInPath(eaFile), # the effective areas file
    )
    eSrc = 'eEffArea'

    process.electronCustomization *= process.eEffArea

    #################
    ### embed rho ###
    #################
    process.eRho = cms.EDProducer(
        "ElectronRhoEmbedder",
        src = cms.InputTag(eSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    eSrc = 'eRho'

    process.electronCustomization *= process.eRho

    ################
    ### embed pv ###
    ################
    process.ePV = cms.EDProducer(
        "ElectronIpEmbedder",
        src = cms.InputTag(eSrc),
        vertexSrc = cms.InputTag(pvSrc),
        beamspotSrc = cms.InputTag("offlineBeamSpot"),
    )
    eSrc = 'ePV'

    process.electronCustomization *= process.ePV

    ##############################
    ### embed trigger matching ###
    ##############################
    labels = []
    paths = []
    from triggers import triggerMap
    for trigger in triggerMap:
        if 'electron' in triggerMap[trigger]['objects']:
            labels += ['matches_{0}'.format(trigger)]
            paths += [triggerMap[trigger]['path']]
    process.eTrig = cms.EDProducer(
        "ElectronHLTMatchEmbedder",
        src = cms.InputTag(eSrc),
        #triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT2') if reHLT else cms.InputTag('TriggerResults', '', 'HLT'),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        deltaR = cms.double(0.5),
        labels = cms.vstring(*labels),
        paths = cms.vstring(*paths),
    )
    eSrc = 'eTrig'

    process.electronCustomization *= process.eTrig

    #####################
    ### embed HZZ IDs ###
    #####################
    # https://github.com/nwoods/UWVV/blob/ichep/AnalysisTools/python/templates/ZZID.py
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2016
    process.eHZZEmbedder = cms.EDProducer(
        "PATElectronZZIDEmbedder",
        src = cms.InputTag(eSrc),
        vtxSrc = cms.InputTag(pvSrc),
        bdtLabel = cms.string('ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values'),
        idCutLowPtLowEta = cms.double(-.211),
        idCutLowPtMedEta = cms.double(-.396),
        idCutLowPtHighEta = cms.double(-.215),
        idCutHighPtLowEta = cms.double(-.870),
        idCutHighPtMedEta = cms.double(-.838),
        idCutHighPtHighEta = cms.double(-.763),
        missingHitsCut = cms.int32(999),
        ptCut = cms.double(7.), 
    )
    eSrc = 'eHZZEmbedder'
    process.electronCustomization *= process.eHZZEmbedder

    ######################
    ### embed SUSY IDs ###
    ######################
    # https://twiki.cern.ch/twiki/bin/view/CMS/LeptonMVA
    process.eMiniIsoEmbedder = cms.EDProducer(
        "ElectronMiniIsolationEmbedder",
        src = cms.InputTag(eSrc),
        packedSrc = cms.InputTag(pfSrc),
    )
    eSrc = 'eMiniIsoEmbedder'
    process.electronCustomization *= process.eMiniIsoEmbedder

    process.eSUSYEmbedder = cms.EDProducer(
        "ElectronSUSYMVAEmbedder",
        src = cms.InputTag(eSrc),
        vertexSrc = cms.InputTag(pvSrc),
        rhoSrc = cms.InputTag('fixedGridRhoFastjetCentralNeutral'),
        mva = cms.string('ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values'),
        weights = cms.FileInPath('DevTools/Ntuplizer/data/forMoriond16_el_sigTTZ_bkgTT_BDTG.weights.xml'),
    )
    eSrc = 'eSUSYEmbedder'
    process.electronCustomization *= process.eSUSYEmbedder

    # add to schedule
    process.schedule.append(process.electronCustomization)

    coll['electrons'] = eSrc

    return coll
