import FWCore.ParameterSet.Config as cms

def customizeJets(process,coll,srcLabel='jets',postfix='',**kwargs):
    '''Customize jets'''
    isMC = kwargs.pop('isMC',False)
    jSrc = coll[srcLabel]
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']

    # customization path
    pathName = 'jetCustomization{0}'.format(postfix)
    setattr(process,pathName,cms.Path())
    path = getattr(process,pathName)

    #################################
    ### add updated pileup jet id ###
    #################################
    process.load("RecoJets.JetProducers.PileupJetID_cfi")
    module = process.pileupJetId.clone(
        jets=cms.InputTag(jSrc),
        inputIsCorrected=True,
        applyJec=True,
        vertexes=cms.InputTag(pvSrc),
    )
    modName = 'pileupJetIdUpdated{0}'.format(postfix)
    setattr(process,modName,module)

    path *= getattr(process,modName)

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
        postfix=postfix,
    )
    modName = 'updatedPatJets{0}'.format(postfix)
    getattr(process,modName).userData.userFloats.src += ['pileupJetIdUpdated{0}:fullDiscriminant'.format(postfix)]
    jSrc = modName

    #################
    ### embed ids ###
    #################
    module = cms.EDProducer(
        "JetIdEmbedder",
        src = cms.InputTag(jSrc),
        discriminator = cms.string('pileupJetIdUpdated:fullDiscriminant'),
    )
    modName = 'jID{0}'.format(postfix)
    setattr(process,modName,module)
    jSrc = modName

    path *= getattr(process,modName)

    #################
    ### embed rho ###
    #################
    module = cms.EDProducer(
        "JetRhoEmbedder",
        src = cms.InputTag(jSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    modName = 'jRho{0}'.format(postfix)
    setattr(process,modName,module)
    jSrc = modName

    path *= getattr(process,modName)

    ##########################
    ### embed jet gen jets ###
    ##########################
    if isMC:
        module = cms.EDProducer(
            "JetGenJetEmbedder",
            src = cms.InputTag(jSrc),
            genJets = cms.InputTag("slimmedGenJets"),
            excludeLeptons = cms.bool(False),
            deltaR = cms.double(0.5),
        )
        modName = 'jGenJetMatching{0}'.format(postfix)
        setattr(process,modName,module)
        jSrc = modName

        path *= getattr(process,modName)


    # add to schedule
    process.schedule.append(path)

    coll[srcLabel] = jSrc

    return coll
