import FWCore.ParameterSet.Config as cms


from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'mumutautau.root'
options.inputFiles = '/store/data/Run2016H/SingleMuon/AOD/PromptReco-v2/000/284/035/00000/5849226D-569F-E611-B874-02163E011EAC.root'
#options.inputFiles = '/store/mc/RunIISummer16DR80Premix/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/60001/D04F22AE-3FF1-E611-BDB5-02163E019C78.root'
#options.inputFiles = '/store/mc/RunIISummer16DR80Premix/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-15_TuneCUETP8M1_13TeV_madgraph_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/82114092-19BB-E611-926B-FA163E0D86FB.root'
options.maxEvents = -1
options.register('skipEvents', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Events to skip")
options.register('reportEvery', 100, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Report every")
options.register('isMC', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")
#options.register('isMC', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")
#options.register('runMetFilter', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Run the recommended MET filters")
options.register('crab', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Make changes needed for crab")
options.register('numThreads', 4, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Set number of threads")
#options.register('runH', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Make changes needed for Run2016H")
options.register('runH', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Make changes needed for Run2016H")

options.parseArguments()

#####################
### Setup Process ###
#####################
from Configuration.StandardSequences.Eras import eras

process = cms.Process("PAT",eras.Run2_2016)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True),
)

process.options.numberOfThreads=cms.untracked.uint32(options.numThreads)
process.options.numberOfStreams=cms.untracked.uint32(0)



#################
### GlobalTag ###
#################
envvar = 'mcgt' if options.isMC else 'datagt'
if options.runH and not options.isMC: envvar = 'datagtH'
from Configuration.AlCa.GlobalTag import GlobalTag
#GT = {'mcgt': 'auto:run2_mc', 'datagt': 'auto:run2_data'}
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
# https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
GT = {'mcgt': '80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'datagt': '80X_dataRun2_2016SeptRepro_v7', 'datagtH': '80X_dataRun2_Prompt_v16'}
process.GlobalTag = GlobalTag(process.GlobalTag, GT[envvar], '')


#############################
### Setup rest of running ###
#############################
process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
)

process.schedule = cms.Schedule()

###########################
### Profiling utilities ###
###########################

#process.ProfilerService = cms.Service (
#      "ProfilerService",
#       firstEvent = cms.untracked.int32(2),
#       lastEvent = cms.untracked.int32(500),
#       paths = cms.untracked.vstring('schedule')
#)

#process.SimpleMemoryCheck = cms.Service(
#    "SimpleMemoryCheck",
#    ignoreTotal = cms.untracked.int32(1)
#)

### To use IgProf's neat memory profiling tools, uncomment the following
### lines then run this cfg with igprof like so:
###      $ igprof -d -mp -z -o igprof.mp.gz cmsRun ...
### this will create a memory profile every 250 events so you can track use
### Turn the profile into text with
###      $ igprof-analyse -d -v -g -r MEM_LIVE igprof.yourOutputFile.gz > igreport_live.res
### To do a performance profile instead of a memory profile, change -mp to -pp
### in the first command and remove  -r MEM_LIVE from the second
### For interpretation of the output, see http://igprof.org/text-output-format.html

#from IgTools.IgProf.IgProfTrigger import igprof
#process.load("IgTools.IgProf.IgProfTrigger")
#process.igprofPath = cms.Path(process.igprof)
#process.igprof.reportEventInterval     = cms.untracked.int32(250)
#process.igprof.reportToFileAtBeginJob  = cms.untracked.string("|gzip -c>igprof.begin-job.gz")
#process.igprof.reportToFileAtEvent = cms.untracked.string("|gzip -c>igprof.%I.%E.%L.%R.event.gz")
#process.schedule.append(process.igprofPath)


#########################
### Output Definition ###
#########################

process.MINIAODoutput = cms.OutputModule('PoolOutputModule',
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAODSIM' if options.isMC else 'MINIAOD'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    outputCommands = process.MINIAODEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True),
    fileName = cms.untracked.string(options.outputFile),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('main_path'),
    ),
)
if options.isMC: process.MINIAODoutput.outputCommands = process.MINIAODSIMEventContent.outputCommands


#####################
### MINIAOD stuff ###
#####################
# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_BadChargedCandidateSummer16Filter = cms.Path(process.BadChargedCandidateSummer16Filter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_BadPFMuonFilter = cms.Path(process.BadPFMuonFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_BadChargedCandidateFilter = cms.Path(process.BadChargedCandidateFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_BadPFMuonSummer16Filter = cms.Path(process.BadPFMuonSummer16Filter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODoutput_step = cms.EndPath(process.MINIAODoutput)

process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_CSCTightHaloTrkMuUnvetoFilter,process.Flag_CSCTightHalo2015Filter,process.Flag_globalTightHalo2016Filter,process.Flag_globalSuperTightHalo2016Filter,process.Flag_HcalStripHaloFilter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_chargedHadronTrackResolutionFilter,process.Flag_muonBadTrackFilter,process.Flag_BadChargedCandidateFilter,process.Flag_BadPFMuonFilter,process.Flag_BadChargedCandidateSummer16Filter,process.Flag_BadPFMuonSummer16Filter,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.endjob_step,process.MINIAODoutput_step)

from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)

if options.isMC:
    process.load('Configuration.StandardSequences.PATMC_cff')
else:
    process.load('Configuration.StandardSequences.PAT_cff')

from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC, miniAOD_customizeAllData
# ReMiniAOD fix for 2017: https://github.com/cms-sw/cmssw/pull/17308
from PhysicsTools.PatAlgos.slimming.customizeMiniAOD_MuEGFixMoriond2017 import customizeAll

if options.isMC:
    process = miniAOD_customizeAllMC(process)
else:
    process = miniAOD_customizeAllData(process)
    process = customizeAll(process)

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

from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag

process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

jetSrc = 'ak4PFJetsMuonCleaned'

process.PATTauSequence = cms.Sequence(process.PFTau+process.makePatTaus+process.selectedPatTaus)
process.PATTauSequenceMuonCleaned = cloneProcessingSnippet(process,process.PATTauSequence, 'MuonCleaned')
process.recoTauAK4PFJets08RegionMuonCleaned.pfCandSrc = cms.InputTag(jetSrc,'particleFlowMuonCleaned')
massSearchReplaceAnyInputTag(process.PATTauSequenceMuonCleaned,cms.InputTag('ak4PFJets'),cms.InputTag(jetSrc))
process.slimmedTausMuonCleaned = process.slimmedTaus.clone(src = cms.InputTag('selectedPatTausMuonCleaned'))

process.selectedPatTausMuonCleaned.cut = cms.string("pt > 10. && tauID(\'decayModeFindingNewDMs\')> 0.5")

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

# input for slimmedMuons
process.selectedPatMuons = cms.EDFilter('PATMuonSelector',
    src = cms.InputTag('patMuons'),
    cut = cms.string('pt > 3.0 && isPFMuon && (isGlobalMuon || isTrackerMuon)'),
)

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
process.z_path = cms.Path()
process.z_alt_path = cms.Path()

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
process.z_path *= process.HLT

process.HLTalt =cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
     HLTPaths = cms.vstring("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*"),
     eventSetupPathsKey = cms.string(''),
     andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
     throw = cms.bool(False) # throw exception on unknown path names
)
process.z_alt_path *= process.HLTalt

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
     minNumber = cms.uint32(3),
     maxNumber = cms.uint32(999),
     src = cms.InputTag('analysisMuonsNoIso'),
)
process.analysisMuonsIsoCount = cms.EDFilter("PATCandViewCountFilter",
     minNumber = cms.uint32(2),
     maxNumber = cms.uint32(999),
     src = cms.InputTag('analysisMuonsIso'),
)
process.main_path *= process.analysisMuonsNoIso
process.main_path *= process.analysisMuonsNoIsoCount
process.main_path *= process.analysisMuonsIso
process.main_path *= process.analysisMuonsIsoCount
process.z_path *= process.analysisMuonsNoIso
process.z_path *= process.analysisMuonsIso
process.z_path *= process.analysisMuonsIsoCount
process.z_alt_path *= process.analysisMuonsNoIso
process.z_alt_path *= process.analysisMuonsIso
process.z_alt_path *= process.analysisMuonsIsoCount

#############################
### Second muon threshold ###
#############################
#process.secondMuon = cms.EDFilter('PATMuonSelector',
process.secondMuon = cms.EDFilter('MuonSelector',
    src = cms.InputTag('analysisMuonsIso'),
    cut = cms.string('pt > 3.0'),
)
process.secondMuonCount = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(2),
    maxNumber = cms.uint32(999),
    src = cms.InputTag('secondMuon'),
)
process.main_path *= process.secondMuon
process.main_path *= process.secondMuonCount
process.z_path *= process.secondMuon
process.z_path *= process.secondMuonCount


process.secondMuonAlt = cms.EDFilter('MuonSelector',
    src = cms.InputTag('analysisMuonsIso'),
    cut = cms.string('pt > 8.0'),
)
process.secondMuonAltCount = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(2),
    maxNumber = cms.uint32(999),
    src = cms.InputTag('secondMuonAlt'),
)
process.z_alt_path *= process.secondMuonAlt
process.z_alt_path *= process.secondMuonAltCount

#########################
### Trigger Threshold ###
#########################
#process.triggerMuon = cms.EDFilter('PATMuonSelector',
process.triggerMuon = cms.EDFilter('MuonSelector',
    src = cms.InputTag('secondMuon'),
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
process.z_path *= process.triggerMuon
process.z_path *= process.triggerMuonCount

process.firstMuonAlt = cms.EDFilter('MuonSelector',
    src = cms.InputTag('secondMuonAlt'),
    cut = cms.string('pt > 17.0'),
)
process.firstMuonAltCount = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999),
    src = cms.InputTag('firstMuonAlt'),
)
process.z_alt_path *= process.firstMuonAlt
process.z_alt_path *= process.firstMuonAltCount

############################
### Require two OS muons ###
############################
process.mumu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {0}@-".format('slimmedMuons')),
    cut   = cms.string("deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi)<1.5 && mass<30"),
)
process.mumuCount = cms.EDFilter("PATCandViewCountFilter",
     minNumber = cms.uint32(1),
     maxNumber = cms.uint32(999),
     src = cms.InputTag('mumu'),
)
process.main_path *= process.mumu
process.main_path *= process.mumuCount

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
process.z_alt_path *= process.mumuZ
process.z_alt_path *= process.mumuZCount

########################
### Tau requirements ###
########################
# first step that requires the new collection
process.analysisTaus = cms.EDFilter('PATTauSelector',
    src = cms.InputTag('slimmedTausMuonCleaned'),
    cut = cms.string('pt > 10.0 && abs(eta)<2.3 && tauID(\'decayModeFinding\')> 0.5'),
)
process.analysisTausCount = cms.EDFilter("PATCandViewCountFilter",
     minNumber = cms.uint32(1),
     maxNumber = cms.uint32(999),
     src = cms.InputTag('analysisTaus'),
)
process.main_path *= process.analysisTaus
process.main_path *= process.analysisTausCount

#################
### Finish up ###
#################
# add to schedule
process.schedule.append(process.main_path)
process.schedule.append(process.z_path)
process.schedule.append(process.z_alt_path)

# lumi summary
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(options.outputFile.split('.root')[0]+'_lumi.root'),
)

process.lumiTree = cms.EDAnalyzer("LumiTree",
    genEventInfo = cms.InputTag("generator"),
)
process.lumi_step = cms.Path(process.lumiTree)
process.schedule.append(process.lumi_step)

process.lumiSummary = cms.EDProducer("LumiSummaryProducer",
    genEventInfo = cms.InputTag("generator"),
)
process.lumiSummary_step = cms.Path(process.lumiSummary)
process.schedule.append(process.lumiSummary_step)


# additional changes to standard MiniAOD content
process.MINIAODoutput.outputCommands += [
    'keep *_slimmedTausMuonCleaned_*_*',
    'keep *_slimmedJetsMuonCleaned_*_*',
    'drop *_slimmedTaus_*_*',
    'drop *_slimmedTausBoosted_*_*',
    'drop *_slimmedJetsAK8*_*_*',
    'drop *_slimmedGenJetsAK8*_*_*',
    'drop *_*Puppi*_*_*',
    'drop *_*Digi*_*_*',
    'drop *_*Backup_*_*',
    'keep *_lumiSummary_*_*',
]

# additional skims
process.MINIAODoutputZSKIM = process.MINIAODoutput.clone(
    SelectEvents = cms.untracked.PSet(
        #SelectEvents = cms.vstring('z_path'),
        SelectEvents = cms.vstring('z_path','z_alt_path'),
    ),
    fileName = cms.untracked.string(options.outputFile.split('.root')[0]+'_zskim.root'),
)
process.MINIAODoutputZSKIM_step = cms.EndPath(process.MINIAODoutputZSKIM)
process.schedule.append(process.MINIAODoutputZSKIM_step)

