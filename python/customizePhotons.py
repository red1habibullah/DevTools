import FWCore.ParameterSet.Config as cms

def customizePhotons(process,coll,**kwargs):
    '''Customize photons'''
    reHLT = kwargs.pop('reHLT',False)
    isMC = kwargs.pop('isMC',False)
    pSrc = coll['photons']
    rhoSrc = coll['rho']

    # customization path
    process.photonCustomization = cms.Path()

    ###################################
    ### scale and smear corrections ###
    ###################################
    # embed the uncorrected stuff
    process.uncorPho = cms.EDProducer(
        "ShiftedPhotonEmbedder",
        src=cms.InputTag(pSrc),
        label=cms.string('uncorrected'),
        shiftedSrc=cms.InputTag('slimmedPhotons::PAT'),
    )
    pSrc = "uncorPho"
    process.photonCustomization *= process.uncorPho

    # TODO: reenable when new recipe released
    #process.load('EgammaAnalysis.ElectronTools.calibratedPatPhotonsRun2_cfi')
    #process.calibratedPatPhotons.photons = pSrc
    #process.calibratedPatPhotons.isMC = isMC
    #process.photonCustomization *= process.calibratedPatPhotons
    #pSrc = 'calibratedPatPhotons'

    #######################
    ### embed Isolation ###
    #######################
    process.load("RecoEgamma/PhotonIdentification/PhotonIDValueMapProducer_cfi")

    process.photonCustomization *= process.photonIDValueMapProducer

    #################
    ### embed VID ###
    #################
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDPhotonIdProducer, setupAllVIDIdsInModule, DataFormat, setupVIDPhotonSelection
    switchOnVIDPhotonIdProducer(process, DataFormat.MiniAOD)
    
    # define which IDs we want to produce
    my_id_modules = [
        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff',
        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Spring16_nonTrig_V1_cff',
    ]
    
    # add them to the VID producer
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

    # update the collection
    process.egmPhotonIDs.physicsObjectSrc = cms.InputTag(pSrc)
    process.egmPhotonIsolation.srcToIsolate = cms.InputTag(pSrc)
    process.photonIDValueMapProducer.srcMiniAOD = cms.InputTag(pSrc)
    process.photonMVAValueMapProducer.srcMiniAOD = cms.InputTag(pSrc)
    process.photonRegressionValueMapProducer.srcMiniAOD = cms.InputTag(pSrc)

    idDecisionLabels = [
        'cutBasedPhotonID-Spring16-25ns-V2p2-loose',
        'cutBasedPhotonID-Spring16-25ns-V2p2-medium',
        'cutBasedPhotonID-Spring16-25ns-V2p2-tight',
        #'mvaPhoID-Spring16-nonTrig-V1-wp80', # EGM recommends not to use
        'mvaPhoID-Spring16-nonTrig-V1-wp90',
    ]
    idDecisionTags = [
        cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose'),
        cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium'),
        cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight'),
        #cms.InputTag('egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-wp80'), # EGM recommends not to use
        cms.InputTag('egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-wp90'),
    ]
    fullIDDecisionLabels = [
    ]
    fullIDDecisionTags = [
    ]
    nMinusOneIDNames = [
    ]
    nMinusOneIDLabels = [
    ]
    mvaValueLabels = [
        'PhotonMVAEstimatorRun2Spring16NonTrigV1Values',
        'gammaDR030',
        "phoWorstChargedIsolationWithConeVeto",
        "phoESEffSigmaRR",
        "phoFull5x5E1x3",
        "phoFull5x5E2x2",
        "phoFull5x5E2x5Max",
        "phoFull5x5E5x5",
        "phoFull5x5SigmaIEtaIEta",
        "phoFull5x5SigmaIEtaIPhi",
        "phoChargedIsolation",
        "phoNeutralHadronIsolation",
        "phoPhotonIsolation",
    ]
    mvaValueTags = [
        cms.InputTag('photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring16NonTrigV1Values'),
        cms.InputTag("egmPhotonIsolation","gamma-DR030-"),
        cms.InputTag("photonIDValueMapProducer","phoWorstChargedIsolationWithConeVeto"),
        cms.InputTag("photonIDValueMapProducer","phoESEffSigmaRR"),
        cms.InputTag("photonIDValueMapProducer","phoFull5x5E1x3"),
        cms.InputTag("photonIDValueMapProducer","phoFull5x5E2x2"),
        cms.InputTag("photonIDValueMapProducer","phoFull5x5E2x5Max"),
        cms.InputTag("photonIDValueMapProducer","phoFull5x5E5x5"),
        cms.InputTag("photonIDValueMapProducer","phoFull5x5SigmaIEtaIEta"),
        cms.InputTag("photonIDValueMapProducer","phoFull5x5SigmaIEtaIPhi"),
        cms.InputTag("photonIDValueMapProducer","phoChargedIsolation"),
        cms.InputTag("photonIDValueMapProducer","phoNeutralHadronIsolation"),
        cms.InputTag("photonIDValueMapProducer","phoPhotonIsolation"),
    ]
    mvaCategoryLabels = [
        'PhotonMVAEstimatorRun2Spring16NonTrigV1Categories',
    ]
    mvaCategoryTags = [
        cms.InputTag('photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring16NonTrigV1Categories'),
    ]

    process.pidEmbedder = cms.EDProducer(
        "PhotonVIDEmbedder",
        src=cms.InputTag(pSrc),
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
    pSrc = 'pidEmbedder'

    process.photonCustomization *= process.egmPhotonIDSequence
    process.photonCustomization *= process.pidEmbedder

    #################
    ### embed rho ###
    #################
    process.pRho = cms.EDProducer(
        "PhotonRhoEmbedder",
        src = cms.InputTag(pSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    pSrc = 'pRho'

    process.photonCustomization *= process.pRho

    #############################
    ### embed effective areas ###
    #############################
    eaChargedHadronsFile = 'RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfChargedHadrons_90percentBased.txt'
    eaNeutralHadronsFile = 'RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfNeutralHadrons_90percentBased.txt'
    #eaPhotonsFile = 'RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfPhotons_90percentBased_3bins.txt'
    eaPhotonsFile = 'RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfPhotons_90percentBased.txt'

    process.pChargedHadronsEffArea = cms.EDProducer(
        "PhotonEffectiveAreaEmbedder",
        src = cms.InputTag(pSrc),
        label = cms.string("EffectiveAreaChargedHadrons"), # embeds a user float with this name
        configFile = cms.FileInPath(eaChargedHadronsFile), # the effective areas file
    )
    pSrc = 'pChargedHadronsEffArea'

    process.pNeutralHadronsEffArea = cms.EDProducer(
        "PhotonEffectiveAreaEmbedder",
        src = cms.InputTag(pSrc),
        label = cms.string("EffectiveAreaNeutralHadrons"), # embeds a user float with this name
        configFile = cms.FileInPath(eaNeutralHadronsFile), # the effective areas file
    )
    pSrc = 'pNeutralHadronsEffArea'

    process.pPhotonsEffArea = cms.EDProducer(
        "PhotonEffectiveAreaEmbedder",
        src = cms.InputTag(pSrc),
        label = cms.string("EffectiveAreaPhotons"), # embeds a user float with this name
        configFile = cms.FileInPath(eaPhotonsFile), # the effective areas file
    )
    pSrc = 'pPhotonsEffArea'

    process.photonCustomization *= process.pChargedHadronsEffArea
    process.photonCustomization *= process.pNeutralHadronsEffArea
    process.photonCustomization *= process.pPhotonsEffArea

    ##############################
    ### embed trigger matching ###
    ##############################
    labels = []
    paths = []
    from triggers import triggerMap
    for trigger in triggerMap:
        if 'photon' in triggerMap[trigger]['objects']:
            labels += ['matches_{0}'.format(trigger)]
            paths += [triggerMap[trigger]['path']]
    process.pTrig = cms.EDProducer(
        "PhotonHLTMatchEmbedder",
        src = cms.InputTag(pSrc),
        #triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT2') if reHLT else cms.InputTag('TriggerResults', '', 'HLT'),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        deltaR = cms.double(0.5),
        labels = cms.vstring(*labels),
        paths = cms.vstring(*paths),
    )
    pSrc = 'pTrig'

    process.photonCustomization *= process.pTrig

    # add to schedule
    process.schedule.append(process.photonCustomization)

    coll['photons'] = pSrc

    return coll
