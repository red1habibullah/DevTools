import FWCore.ParameterSet.Config as cms

def customizeJets(process,coll,**kwargs):
    '''Customize jets'''
    isMC = kwargs.pop('isMC',False)
    jSrc = coll['jets']
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']

    # customization path
    process.jetCustomization = cms.Path()

    #################################
    ### add updated pileup jet id ###
    #################################
    process.load("RecoJets.JetProducers.PileupJetID_cfi")
    process.pileupJetIdUpdated = process.pileupJetId.clone(
        jets=cms.InputTag(jSrc),
        inputIsCorrected=True,
        applyJec=True,
        vertexes=cms.InputTag(pvSrc),
    )
    process.jetCustomization *= process.pileupJetIdUpdated
    jSrc = 'pileupJetIdUpdated'

    ######################
    ### recorrect jets ###
    ######################
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

    jetCorr = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None')
    if isMC:
        jetCorr = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')
    updateJetCollection(
        process,
        jetSource = cms.InputTag(jSrc),
        jetCorrections = jetCorr,
    )
    jSrc = 'updatedPatJets'

    #################
    ### embed ids ###
    #################
    process.jID = cms.EDProducer(
        "JetIdEmbedder",
        src = cms.InputTag(jSrc),
        discriminator = cms.string('pileupJetIdUpdated:fullDiscriminant'),
    )
    process.jetCustomization *= process.jID
    jSrc = "jID"

    #################
    ### embed rho ###
    #################
    process.jRho = cms.EDProducer(
        "JetRhoEmbedder",
        src = cms.InputTag(jSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    jSrc = 'jRho'

    process.jetCustomization *= process.jRho

    ##########################
    ### embed jet gen jets ###
    ##########################
    if isMC:
        process.jGenJetMatching = cms.EDProducer(
            "JetGenJetEmbedder",
            src = cms.InputTag(jSrc),
            genJets = cms.InputTag("slimmedGenJets"),
            excludeLeptons = cms.bool(False),
            deltaR = cms.double(0.5),
        )
        jSrc = "jGenJetMatching"
        process.jetCustomization *= process.jGenJetMatching


    # add to schedule
    process.schedule.append(process.jetCustomization)

    coll['jets'] = jSrc

    return coll
