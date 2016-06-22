import FWCore.ParameterSet.Config as cms

def customizePhotons(process,coll,**kwargs):
    '''Customize photons'''
    isMC = kwargs.pop('isMC',False)
    pSrc = coll['photons']
    rhoSrc = coll['rho']

    # customization path
    process.photonCustomization = cms.Path()

    ###################################
    ### scale and smear corrections ###
    ###################################
    #process.load('EgammaAnalysis.ElectronTools.calibratedPhotonsRun2_cfi')
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
        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring15_25ns_V1_cff',
        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Spring15_25ns_nonTrig_V2_cff',
    ]
    
    # add them to the VID producer
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

    # update the collection
    process.egmPhotonIDs.physicsObjectSrc = cms.InputTag(pSrc)
    process.photonIDValueMapProducer.srcMiniAOD = cms.InputTag(pSrc)
    process.photonMVAValueMapProducer.srcMiniAOD = cms.InputTag(pSrc)
    process.photonRegressionValueMapProducer.srcMiniAOD = cms.InputTag(pSrc)

    idDecisionLabels = [
        'cutBasedPhotonID-Spring15-25ns-V1-standalone-loose',
        'cutBasedPhotonID-Spring15-25ns-V1-standalone-medium',
        'cutBasedPhotonID-Spring15-25ns-V1-standalone-tight',
        'mvaPhoID-Spring15-25ns-nonTrig-V2-wp90',
    ]
    idDecisionTags = [
        cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-loose'),
        cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-medium'),
        cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-tight'),
        cms.InputTag('egmPhotonIDs:mvaPhoID-Spring15-25ns-nonTrig-V2-wp90'),
    ]
    mvaValueLabels = [
        'PhotonMVAEstimatorRun2Spring15NonTrig25nsV2Values',
        'phoFull5x5SigmaIEtaIEta',
        'phoChargedIsolation',
        'phoNeutralHadronIsolation',
        'phoPhotonIsolation',
    ]
    mvaValueTags = [
        cms.InputTag('photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring15NonTrig25nsV2Values'),
        cms.InputTag('photonIDValueMapProducer:phoFull5x5SigmaIEtaIEta'),
        cms.InputTag('photonIDValueMapProducer:phoChargedIsolation'),
        cms.InputTag('photonIDValueMapProducer:phoNeutralHadronIsolation'),
        cms.InputTag('photonIDValueMapProducer:phoPhotonIsolation'),
    ]
    mvaCategoryLabels = [
        'PhotonMVAEstimatorRun2Spring15NonTrig25nsV2Categories',
    ]
    mvaCategoryTags = [
        cms.InputTag('photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring15NonTrig25nsV2Categories'),
    ]

    process.pidEmbedder = cms.EDProducer(
        "PhotonVIDEmbedder",
        src=cms.InputTag(pSrc),
        idLabels = cms.vstring(*idDecisionLabels),        # labels for bool maps
        ids = cms.VInputTag(*idDecisionTags),             # bool maps
        valueLabels = cms.vstring(*mvaValueLabels),       # labels for float maps
        values = cms.VInputTag(*mvaValueTags),            # float maps
        categoryLabels = cms.vstring(*mvaCategoryLabels), # labels for int maps
        categories = cms.VInputTag(*mvaCategoryTags),     # int maps
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
    eaChargedHadronsFile = 'RecoEgamma/PhotonIdentification/data/Spring15/effAreaPhotons_cone03_pfChargedHadrons_25ns_NULLcorrection.txt'
    eaNeutralHadronsFile = 'RecoEgamma/PhotonIdentification/data/Spring15/effAreaPhotons_cone03_pfNeutralHadrons_25ns_90percentBased.txt'
    eaPhotonsFile = 'RecoEgamma/PhotonIdentification/data/Spring15/effAreaPhotons_cone03_pfPhotons_25ns_90percentBased.txt'

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
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
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
