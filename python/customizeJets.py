import FWCore.ParameterSet.Config as cms

def customizeJets(process,coll,**kwargs):
    '''Customize jets'''
    isMC = kwargs.pop('isMC',False)
    jSrc = coll['jets']
    rhoSrc = coll['rho']

    # customization path
    process.jetCustomization = cms.Path()

    ######################
    ### recorrect jets ###
    ######################
    #from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

    #updateJetCollection(
    #    process,
    #    jetSource = cms.InputTag(jSrc),
    #    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')  # Do not forget 'L2L3Residual' on data!
    #)
    #jSrc = 'updatedPatJets'

    #################
    ### embed ids ###
    #################
    process.jID = cms.EDProducer(
        "JetIdEmbedder",
        src = cms.InputTag(jSrc),
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
