import FWCore.ParameterSet.Config as cms

# lower the pt threshold
def lowerTauPt(process,postfix='',tauPt=8, jetPt=5):
    from FWCore.ParameterSet.MassReplace import massSearchReplaceParam
    massSearchReplaceParam(getattr(process,'PATTauSequence'+postfix),'minJetPt',14,jetPt)
    getattr(process,'selectedPatTaus'+postfix).cut = cms.string("pt > {} && tauID(\'decayModeFindingNewDMs\')> 0.5".format(tauPt))

def addMuMuTauTau(process,options,**kwargs):
    doMM = kwargs.pop('doMM',False)
    doMT = kwargs.pop('doMT',False)

    #########################
    ### Muon Cleaned Taus ###
    #########################
    process.recoMuonsForJetCleaning = cms.EDFilter('MuonRefSelector',
        src = cms.InputTag('muons'),
        cut = cms.string('pt > 3.0 && isPFMuon && (isGlobalMuon || isTrackerMuon)'),
    )
    
    process.ak4PFJetsMuonCleaned = cms.EDProducer(
        'MuonCleanedJetProducer',
        jetSrc = cms.InputTag("ak4PFJets"),
        muonSrc = cms.InputTag("recoMuonsForJetCleaning"),
        pfCandSrc = cms.InputTag("particleFlow"),
    )
    
    process.muonCleanedHPSPFTausTask = cms.Task(
        process.recoMuonsForJetCleaning,
        process.ak4PFJetsMuonCleaned
    )
    
    import PhysicsTools.PatAlgos.tools.helpers as configtools
    from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
    from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag
    
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    patAlgosToolsTask = configtools.getPatAlgosToolsTask(process)
    patAlgosToolsTask.add(process.muonCleanedHPSPFTausTask)
    
    jetSrc = 'ak4PFJetsMuonCleaned'
    pfCandSrc = cms.InputTag(jetSrc,'particleFlowMuonCleaned')
    
    process.PATTauSequence = cms.Sequence(process.PFTau+process.makePatTaus+process.selectedPatTaus)
    process.PATTauSequenceMuonCleaned = cloneProcessingSnippet(process,process.PATTauSequence, 'MuonCleaned', addToTask = True)
    massSearchReplaceAnyInputTag(process.PATTauSequenceMuonCleaned,cms.InputTag('ak4PFJets'),cms.InputTag(jetSrc))
    massSearchReplaceAnyInputTag(process.PATTauSequenceMuonCleaned,cms.InputTag('particleFlow'),pfCandSrc)
    # currently, the tau reco requires same pf coll for both the jets and the following:
    process.combinatoricRecoTausMuonCleaned.builders[0].pfCandSrc = cms.InputTag('particleFlow')
    ## change the packedPFCandidates
    #process.NewPackedTask = cms.Task(process.primaryVertexAssociation,process.packedPFCandidatesTask)
    #process.PackedPFCandsSequence = cms.Sequence(process.NewPackedTask)
    #process.PackedPFCandsSequenceMuonCleaned = cloneProcessingSnippet(process,process.PackedPFCandsSequence, 'MuonCleaned', addToTask = True)
    #massSearchReplaceAnyInputTag(process.PackedPFCandsSequenceMuonCleaned,cms.InputTag('particleFlow'),pfCandSrc)
    #process.primaryVertexAssociationMuonCleaned.jets = cms.InputTag(jetSrc)
    #process.packedPFCandidatesMuonCleaned.vertexAssociator = cms.InputTag("primaryVertexAssociationMuonCleaned","original")
    #process.packedPFCandidatesMuonCleaned.PuppiSrc = ""
    #process.packedPFCandidatesMuonCleaned.PuppiNoLepSrc = ""
    #process.slimmedTausMuonCleaned = process.slimmedTaus.clone(
    #    src = cms.InputTag('selectedPatTausMuonCleaned'),
    #    packedPFCandidates = cms.InputTag('packedPFCandidatesMuonCleaned'),
    #)
    #patAlgosToolsTask.add(process.slimmedTausMuonCleaned)
    
    #process.combinatoricRecoTausMuonCleaned.minJetPt = cms.double(8.0)
    #process.recoTauAK4PFJets08RegionMuonCleaned.minJetPt = cms.double(8.0)
    #process.ak4PFJetsLegacyHPSPiZerosMuonCleaned.minJetPt = cms.double(8.0)
    #process.ak4PFJetsRecoTauChargedHadronsMuonCleaned.minJetPt = cms.double(8.0)
    #process.selectedPatTausMuonCleaned.cut = cms.string("pt > 8. && tauID(\'decayModeFindingNewDMs\')> 0.5")
    lowerTauPt(process,'MuonCleaned')
    
    if options.isMC:
        process.tauGenJetsMuonCleaned.GenParticles = "prunedGenParticles"
        process.patTausMuonCleaned.embedGenMatch = False
    else:
        from PhysicsTools.PatAlgos.tools.coreTools import _removeMCMatchingForPATObject
        attrsToDelete = []
        postfix = ''
        print "removing MC dependencies for tausMuonCleaned"
        _removeMCMatchingForPATObject(process, 'tauMatch', 'patTausMuonCleaned',postfix)
        ## remove mc extra configs for taus
        tauProducer = getattr(process,'patTausMuonCleaned'+postfix)
        tauProducer.addGenJetMatch   = False
        tauProducer.embedGenJetMatch = False
        attrsToDelete += [tauProducer.genJetMatch.getModuleLabel()]
        tauProducer.genJetMatch      = ''
        attrsToDelete += ['tauGenJetsMuonCleaned'+postfix]
        attrsToDelete += ['tauGenJetsSelectorAllHadronsMuonCleaned'+postfix]
        for attr in attrsToDelete:
            if hasattr(process,attr): delattr(process,attr)
    
    #############################
    ### lower pt for nonclean ###
    #############################
    #process.combinatoricRecoTaus.minJetPt = cms.double(8.0)
    #process.recoTauAK4PFJets08Region.minJetPt = cms.double(8.0)
    #process.ak4PFJetsLegacyHPSPiZeros.minJetPt = cms.double(8.0)
    #process.ak4PFJetsRecoTauChargedHadrons.minJetPt = cms.double(8.0)
    #process.selectedPatTaus.cut = cms.string("pt > 8. && tauID(\'decayModeFindingNewDMs\')> 0.5")
    lowerTauPt(process)
    
    ############################
    ### lower pt for boosted ###
    ############################
    process.ca8PFJetsCHSprunedForBoostedTaus.jetPtMin = cms.double(20.0)
    process.ca8PFJetsCHSprunedForBoostedTaus.subjetPtMin = cms.double(8.0)
    #process.combinatoricRecoTausBoosted.minJetPt = cms.double(8.0)
    #process.recoTauAK4PFJets08RegionBoosted.minJetPt = cms.double(8.0)
    #process.selectedPatTausBoosted.cut = cms.string("pt > 8. && tauID(\'decayModeFindingNewDMs\')> 0.5")
    lowerTauPt(process,'Boosted')

    #######################################
    ### Update btagging for cleaned jet ###
    #######################################
    
    from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import j2tParametersVX
    process.ak4PFJetsMuonCleanedTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
        j2tParametersVX,
        jets = cms.InputTag("ak4PFJetsMuonCleaned")
    )
    process.patJetMuonCleanedCharge = cms.EDProducer("JetChargeProducer",
        src = cms.InputTag("ak4PFJetsMuonCleanedTracksAssociatorAtVertex"),
        var = cms.string('Pt'),
        exp = cms.double(1.0)
    )
    
    from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
    addJetCollection(process, postfix   = "", labelName = 'MuonCleaned', jetSource = cms.InputTag('ak4PFJetsMuonCleaned'),
                    jetCorrections = ('AK4PF', ['L2Relative', 'L3Absolute'], ''),
                    algo= 'AK', rParam = 0.4, btagDiscriminators = map(lambda x: x.value() ,process.patJets.discriminatorSources)
                    )
    
    if options.isMC: process.patJetGenJetMatchMuonCleaned.matched = 'slimmedGenJets'
    process.patJetsMuonCleaned.jetChargeSource = cms.InputTag("patJetMuonCleanedCharge")
    
    process.slimmedJetsMuonCleaned = process.slimmedJets.clone(src = cms.InputTag("selectedPatJetsMuonCleaned"))


    #################
    ### Skim Path ###
    #################
    process.main_path = cms.Path()
    process.main_path_em = cms.Path()
    process.main_path_et = cms.Path()
    process.main_path_mt = cms.Path()
    process.main_path_tt = cms.Path()
    process.z_path = cms.Path()
    process.z_tau_eff_path = cms.Path()
    process.z_tau_eff_muclean_path = cms.Path()
    
    # currently set to be fast, only using collections in AOD
    # can switch back to using MINIAOD collections but they will need to be produced first
    
    # preskim
    
    ###############
    ### Trigger ###
    ###############
    process.HLT =cms.EDFilter("HLTHighLevel",
         TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
         #HLTPaths = cms.vstring("HLT_IsoMu27_v*", "HLT_IsoTkMu27_v*"), # 2017
         HLTPaths = cms.vstring("HLT_IsoMu24_v*", "HLT_IsoTkMu24_v*", "HLT_IsoMu27_v*", "HLT_IsoTkMu27_v*"),
         eventSetupPathsKey = cms.string(''),
         andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
         throw = cms.bool(False) # throw exception on unknown path names
    )
    process.main_path *= process.HLT
    process.main_path_em *= process.HLT
    process.main_path_et *= process.HLT
    process.main_path_mt *= process.HLT
    process.main_path_tt *= process.HLT
    process.z_path *= process.HLT
    process.z_tau_eff_path *= process.HLT
    process.z_tau_eff_muclean_path *= process.HLT
    
    #########################
    ### Muon ID embedding ###
    #########################
    #process.slimmedMuonsWithID = cms.EDProducer("MuonIdEmbedder",
    #    src = cms.InputTag('slimmedMuons'),
    #    vertexSrc = cms.InputTag('offlineSlimmedPrimaryVertices'),
    #)
    #process.main_path *= process.slimmedMuonsWithID
    #process.z_path *= process.slimmedMuonsWithID
    
    ###############
    ### Muon ID ###
    ###############
    #process.analysisMuonsNoIso = cms.EDFilter('PATMuonSelector',
    process.analysisMuonsNoIso = cms.EDFilter('MuonSelector',
        #src = cms.InputTag('slimmedMuonsWithID'),
        src = cms.InputTag('muons'),
        #cut = cms.string('pt > 3.0 && abs(eta)<2.4 && (isMediumMuon || userInt("isMediumMuonICHEP"))'),
        cut = cms.string('pt > 3.0 && abs(eta)<2.4 && isPFMuon && (isGlobalMuon || isTrackerMuon)'),
    )
    #process.analysisMuonsIso = cms.EDFilter('PATMuonSelector',
    process.analysisMuonsIso = cms.EDFilter('MuonSelector',
        src = cms.InputTag('analysisMuonsNoIso'),
        cut = cms.string('(pfIsolationR04().sumChargedHadronPt'
                         '+ max(0., pfIsolationR04().sumNeutralHadronEt'
                         '+ pfIsolationR04().sumPhotonEt'
                         '- 0.5*pfIsolationR04().sumPUPt))'
                         '/pt()<0.25'),
    )
    process.analysisMuonsNoIsoCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(2),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('analysisMuonsNoIso'),
    )
    process.analysisMuonsIsoCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(2),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('analysisMuonsIso'),
    )
    process.analysisMuonsNoIsoCountTauEff = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('analysisMuonsNoIso'),
    )
    process.main_path *= process.analysisMuonsNoIso
    process.main_path *= process.analysisMuonsNoIsoCount
    process.main_path_em *= process.analysisMuonsNoIso
    process.main_path_em *= process.analysisMuonsNoIsoCount
    process.main_path_et *= process.analysisMuonsNoIso
    process.main_path_et *= process.analysisMuonsNoIsoCount
    process.main_path_mt *= process.analysisMuonsNoIso
    process.main_path_mt *= process.analysisMuonsNoIsoCount
    process.main_path_tt *= process.analysisMuonsNoIso
    process.main_path_tt *= process.analysisMuonsNoIsoCount
    process.z_path *= process.analysisMuonsNoIso
    process.z_path *= process.analysisMuonsNoIsoCount
    process.z_tau_eff_path *= process.analysisMuonsNoIso
    process.z_tau_eff_path *= process.analysisMuonsNoIsoCountTauEff
    process.z_tau_eff_muclean_path *= process.analysisMuonsNoIso
    process.z_tau_eff_muclean_path *= process.analysisMuonsNoIsoCountTauEff
    
    #########################
    ### Trigger Threshold ###
    #########################
    #process.triggerMuon = cms.EDFilter('PATMuonSelector',
    process.triggerMuon = cms.EDFilter('MuonSelector',
        #src = cms.InputTag('secondMuon'),
        src = cms.InputTag('analysisMuonsNoIso'),
        #cut = cms.string('pt > 27.0'),
        cut = cms.string('pt > 24.0'),
    )
    process.triggerMuonCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('triggerMuon'),
    )
    process.main_path *= process.triggerMuon
    process.main_path *= process.triggerMuonCount
    process.main_path_em *= process.triggerMuon
    process.main_path_em *= process.triggerMuonCount
    process.main_path_et *= process.triggerMuon
    process.main_path_et *= process.triggerMuonCount
    process.main_path_mt *= process.triggerMuon
    process.main_path_mt *= process.triggerMuonCount
    process.main_path_tt *= process.triggerMuon
    process.main_path_tt *= process.triggerMuonCount
    process.z_path *= process.triggerMuon
    process.z_path *= process.triggerMuonCount
    process.z_tau_eff_path *= process.triggerMuon
    process.z_tau_eff_path *= process.triggerMuonCount
    process.z_tau_eff_muclean_path *= process.triggerMuon
    process.z_tau_eff_muclean_path *= process.triggerMuonCount
    
    ############################
    ### Require two OS muons ###
    ############################
    process.mumu = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("{0}@+ {0}@-".format('slimmedMuons')),
        #cut   = cms.string("deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi)<1.5 && mass<60"),
        cut   = cms.string("1<mass<65"),
    )
    process.mumuCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('mumu'),
    )
    process.main_path *= process.mumu
    process.main_path *= process.mumuCount
    process.main_path_em *= process.mumu
    process.main_path_em *= process.mumuCount
    process.main_path_et *= process.mumu
    process.main_path_et *= process.mumuCount
    process.main_path_mt *= process.mumu
    process.main_path_mt *= process.mumuCount
    process.main_path_tt *= process.mumu
    process.main_path_tt *= process.mumuCount
    
    process.mumuZ = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("{0}@+ {0}@-".format('slimmedMuons')),
        cut   = cms.string("60<mass<120"),
    )
    process.mumuZCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('mumuZ'),
    )
    process.z_path *= process.mumuZ
    process.z_path *= process.mumuZCount
    
    ########################
    ### Tau requirements ###
    ########################
    process.analysisTaus = cms.EDFilter('PATTauSelector',
        src = cms.InputTag('slimmedTaus'),
        cut = cms.string('pt > 8.0 && abs(eta)<2.3 && tauID(\'decayModeFinding\')> 0.5'),
    )
    process.analysisTausCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('analysisTaus'),
    )
    process.analysisTausMuonCleaned = cms.EDFilter('PATTauSelector',
        #src = cms.InputTag('slimmedTausMuonCleaned'),
        src = cms.InputTag('selectedPatTausMuonCleaned'),
        cut = cms.string('pt > 8.0 && abs(eta)<2.3 && tauID(\'decayModeFinding\')> 0.5'),
    )
    process.analysisTausMuonCleanedCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('analysisTaus'),
    )
    process.analysisMuonsNoIsoMTCount = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(3),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('analysisMuonsNoIso'),
    )
    process.main_path_mt *= process.analysisMuonsNoIsoMTCount
    process.main_path_mt *= process.analysisTausMuonCleaned
    process.main_path_mt *= process.analysisTausMuonCleanedCount
    process.z_tau_eff_path *= process.analysisTaus
    process.z_tau_eff_path *= process.analysisTausCount
    process.z_tau_eff_muclean_path *= process.analysisTausMuonCleaned
    process.z_tau_eff_muclean_path *= process.analysisTausMuonCleanedCount

    # and for mt require third muon
    
    ############################
    ### Tau Eff requirements ###
    ############################
    process.mumuZTauEff = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("{0} {1}".format('slimmedMuons','analysisTaus')),
        checkCharge = cms.bool(False),
        cut   = cms.string("30<mass<210 && deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi)>0.5"),
    )
    process.mumuZCountTauEff = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('mumuZTauEff'),
    )
    process.mumuZMuonCleanedTauEff = cms.EDProducer("CandViewShallowCloneCombiner",
        decay = cms.string("{0} {1}".format('slimmedMuons','analysisTausMuonCleaned')),
        checkCharge = cms.bool(False),
        cut   = cms.string("30<mass<210 && deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi)>0.5"),
    )
    process.mumuZMuonCleanedCountTauEff = cms.EDFilter("PATCandViewCountFilter",
         minNumber = cms.uint32(1),
         maxNumber = cms.uint32(999),
         src = cms.InputTag('mumuZMuonCleanedTauEff'),
    )
    process.z_tau_eff_path *= process.mumuZTauEff
    process.z_tau_eff_path *= process.mumuZCountTauEff
    process.z_tau_eff_muclean_path *= process.mumuZMuonCleanedTauEff
    process.z_tau_eff_muclean_path *= process.mumuZMuonCleanedCountTauEff
    
    #################
    ### Finish up ###
    #################
    # add to schedule
    process.schedule.append(process.main_path)
    process.schedule.append(process.main_path_em)
    process.schedule.append(process.main_path_et)
    process.schedule.append(process.main_path_mt)
    process.schedule.append(process.main_path_tt)
    process.schedule.append(process.z_path)
    process.schedule.append(process.z_tau_eff_path)
    process.schedule.append(process.z_tau_eff_muclean_path)
    
    # lumi summary
    process.TFileService = cms.Service("TFileService",
        fileName = cms.string(options.outputFile.split('.root')[0]+'_lumi.root'),
    )
    
    process.lumiTree = cms.EDAnalyzer("LumiTree",
        genEventInfo = cms.InputTag("generator"),
        lheEventProduct = cms.InputTag("externalLHEProducer"),
    )
    process.lumi_step = cms.Path(process.lumiTree)
    process.schedule.append(process.lumi_step)
    
    process.lumiSummary = cms.EDProducer("LumiSummaryProducer",
        genEventInfo = cms.InputTag("generator"),
        lheEventProduct = cms.InputTag("externalLHEProducer"),
    )
    process.lumiSummary_step = cms.Path(process.lumiSummary)
    process.schedule.append(process.lumiSummary_step)
    
    
    # additional changes to standard MiniAOD content
    process.MINIAODoutput.outputCommands += [
        #'keep *_slimmedTausMuonCleaned_*_*',
        'keep *_selectedPatTausMuonCleaned_*_*',
        #'keep *_slimmedJetsMuonCleaned_*_*', # can't keep without warnings, can be recreated later anyway
        'keep *_lumiSummary_*_*',
    ]
    if not options.isMC:
        process.MINIAODoutput.outputCommands += [
            'drop *_ctppsLocalTrackLiteProducer_*_*', # Don't know what this is, but it prevents running in older releases
        ]

    process.MINIAODoutput.SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('main_path'),
        #SelectEvents = cms.vstring('main_path_em','main_path_et','main_path_mt','main_path_tt'),
    )
    
    # additional skims
    if doMM:
        process.MINIAODoutputZSKIM = process.MINIAODoutput.clone(
            SelectEvents = cms.untracked.PSet(
                SelectEvents = cms.vstring('z_path'),
            ),
            fileName = cms.untracked.string(options.outputFile.split('.root')[0]+'_zskim.root'),
        )
        process.MINIAODoutputZSKIM_step = cms.EndPath(process.MINIAODoutputZSKIM)
        process.schedule.append(process.MINIAODoutputZSKIM_step)
    
    if doMT:
        process.MINIAODoutputZMUTAUSKIM = process.MINIAODoutput.clone(
            SelectEvents = cms.untracked.PSet(
                SelectEvents = cms.vstring('z_tau_eff_path','z_tau_eff_muclean_path'),
            ),
            fileName = cms.untracked.string(options.outputFile.split('.root')[0]+'_zmutauskim.root'),
        )
        process.MINIAODoutputZMUTAUSKIM_step = cms.EndPath(process.MINIAODoutputZMUTAUSKIM)
        process.schedule.append(process.MINIAODoutputZMUTAUSKIM_step)
