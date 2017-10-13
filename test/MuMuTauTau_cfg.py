import os

import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'mumutautau.root'
#options.inputFiles= '/store/mc/RunIISummer16MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/2E1C211C-05C2-E611-90D3-02163E01306F.root' # WZ
#options.inputFiles = '/store/mc/RunIISummer16MiniAODv2/HPlusPlusHMinusHTo3L_M-500_13TeV-calchep-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/08ECD723-E4CA-E611-8C93-0CC47A1E0DC2.root' # Hpp3l
options.inputFiles = '/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-19_TuneCUETP8M1_13TeV_madgraph_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/0CB90DE6-93DE-E611-8DAF-0025905B855C.root' # HToAA
#options.inputFiles = '/store/data/Run2016G/DoubleMuon/MINIAOD/03Feb2017-v1/100000/00182C13-EEEA-E611-8897-001E675A6C2A.root' # ReReco
options.maxEvents = -1
options.register('skipEvents', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Events to skip")
options.register('reportEvery', 100, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Report every")
#options.register('isMC', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")
options.register('isMC', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")
options.register('reHLT', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is reHLT")
options.register('runMetFilter', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Run the recommended MET filters")
options.register('crab', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Make changes needed for crab")
options.register('numThreads', 4, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Set number of threads")

options.parseArguments()

#####################
### setup process ###
#####################

process = cms.Process("MuMuTauTau")

process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.Services_cff')

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    #wantSummary = cms.untracked.bool(True),
)

process.options.numberOfThreads=cms.untracked.uint32(options.numThreads)
process.options.numberOfStreams=cms.untracked.uint32(0)

process.RandomNumberGeneratorService = cms.Service(
    "RandomNumberGeneratorService",
    calibratedPatElectrons = cms.PSet(
        initialSeed = cms.untracked.uint32(1),
        engineName = cms.untracked.string('TRandom3')
    ),
    calibratedPatPhotons = cms.PSet(
        initialSeed = cms.untracked.uint32(2),
        engineName = cms.untracked.string('TRandom3')
    ),
    mRoch = cms.PSet(
        initialSeed = cms.untracked.uint32(3),
        engineName = cms.untracked.string('TRandom3')
    ),
)

#################
### GlobalTag ###
#################
envvar = 'mcgt' if options.isMC else 'datagt'
from Configuration.AlCa.GlobalTag import GlobalTag
#GT = {'mcgt': 'auto:run2_mc', 'datagt': 'auto:run2_data'}
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
# https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
GT = {'mcgt': '80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'datagt': '80X_dataRun2_2016SeptRepro_v7'}
process.GlobalTag = GlobalTag(process.GlobalTag, GT[envvar], '')

##################
### JEC source ###
##################
# this is if we need to override the jec in global tag
#sqfile = 'DevTools/Ntuplizer/data/{0}.db'.format('Summer16_23Sep2016V3_MC' if options.isMC else 'Summer16_23Sep2016AllV3_DATA')
#if options.crab: sqfile = 'src/{0}'.format(sqfile) # uncomment to submit to crab
#tag = 'JetCorrectorParametersCollection_Summer16_23Sep2016AllV3_DATA_AK4PFchs'
#if options.isMC: tag = 'JetCorrectorParametersCollection_Summer16_23Sep2016V3_MC_AK4PFchs' # MoriondMC
#process.load("CondCore.DBCommon.CondDBCommon_cfi")
#from CondCore.DBCommon.CondDBSetup_cfi import *
#process.jec = cms.ESSource("PoolDBESSource",
#    DBParameters = cms.PSet(
#        messageLevel = cms.untracked.int32(0)
#    ),
#    timetype = cms.string('runnumber'),
#    toGet = cms.VPSet(
#        cms.PSet(
#            record = cms.string('JetCorrectionsRecord'),
#            tag    = cms.string(tag),
#            label  = cms.untracked.string('AK4PFchs')
#        ),
#    ), 
#    connect = cms.string('sqlite:{0}'.format(sqfile)),
#)
#process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

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

# first create collections to analyze
collections = {
    'genParticles' : 'prunedGenParticles',
    'electrons'    : 'slimmedElectrons',
    'muons'        : 'slimmedMuons',
    'taus'         : 'slimmedTaus',
    'tausBoosted'  : 'slimmedTausBoosted',
    'photons'      : 'slimmedPhotons',
    'jets'         : 'slimmedJets',
    'pfmet'        : 'slimmedMETs',
    'rho'          : 'fixedGridRhoFastjetAll',
    'vertices'     : 'offlineSlimmedPrimaryVertices',
    'packed'       : 'packedPFCandidates',
}
if not options.isMC: collections['pfmet'] = 'slimmedMETsMuEGClean'

# the selections for each object (to be included in ntuple)
# will always be the last thing done to the collection, so can use embedded things from previous steps
selections = {
    'electrons'   : 'pt>5 && abs(eta)<2.5 && userInt("mvaEleID-Spring16-GeneralPurpose-V1-wp90")',
    'muons'       : 'pt>0 && abs(eta)<2.4 && isMediumMuon && abs(userFloat("dz"))<0.5 && abs(userFloat("dxy"))<0.2 && (pfIsolationR04().sumChargedHadronPt + max(0., pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5*pfIsolationR04().sumPUPt))/pt<0.25',
    #'muons'       : 'pt>0 && abs(eta)<2.4 && isMediumMuon && abs(userFloat("dz"))<0.5 && abs(userFloat("dxy"))<0.2',
    'taus'        : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding") && tauID("againstElectronVLooseMVA6") && tauID("againstMuonLoose3") && tauID("byLooseIsolationMVArun2v1DBoldDMwLT")',
    #'taus'        : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding") && tauID("againstElectronVLooseMVA6")',
    #'taus'        : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding") && tauID("againstMuonLoose3")',
    #'taus'        : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding")',
    'tausBoosted' : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding") && tauID("againstElectronVLooseMVA6") && tauID("againstMuonLoose3") && tauID("byLooseIsolationMVArun2v1DBoldDMwLT")',
    #'tausBoosted' : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding") && tauID("againstElectronVLooseMVA6")',
    #'tausBoosted' : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding") && tauID("againstMuonLoose3")',
    #'tausBoosted' : 'pt>18 && abs(eta)<2.3 && tauID("decayModeFinding")',
    'photons'     : 'pt>10 && abs(eta)<3.0',
    'jets'        : 'pt>15 && abs(eta)<4.7',
}
if options.isMC:
    selections['genParticles'] = 'pt>0'

# requirements to store events
minCounts = {
    'electrons'  : 0,
    'muons'      : 2,
    'taus'       : 0,
    'tausBoosted': 0,
    'photons'    : 0,
    'jets'       : 0,
}

# maximum candidates to store
# selects the first n in the collection
# patobjects are pt ordered
# vertices has pv first
maxCounts = {
    'vertices': 1,
}

# filters
filters = []

# met filters
#if options.runMetFilter:
# run all the time and store result
print 'Preparing MET filters'
from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
hltFilter = hltHighLevel.clone()
# PAT if miniaod by itself (MC) and RECO if at the same time as reco (data)
hltFilter.TriggerResultsTag = cms.InputTag('TriggerResults', '', 'PAT') if options.isMC else cms.InputTag('TriggerResults', '', 'RECO')
hltFilter.throw = cms.bool(True)
# Moriond17 recommendation
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Moriond_2017
for flag in ['HBHENoiseFilter','HBHENoiseIsoFilter','EcalDeadCellTriggerPrimitiveFilter','goodVertices','eeBadScFilter','globalTightHalo2016Filter']:
    mod = hltFilter.clone(HLTPaths=cms.vstring('Flag_{0}'.format(flag)))
    modName = 'filter{0}'.format(flag)
    setattr(process,modName,mod)
    if options.isMC and flag in ['eeBadScFilter']: continue
    filters += [getattr(process,modName)]
process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
filters += [process.BadChargedCandidateFilter]
    
#########################
### Customize objects ###
#########################
print 'Customizing jets'
from DevTools.Ntuplizer.customizeJets import customizeJets
collections = customizeJets(
    process,
    collections,
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

print 'Customizing electrons'
from DevTools.Ntuplizer.customizeElectrons import customizeElectrons
collections = customizeElectrons(
    process,
    collections,
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

print 'Customizing muons'
from DevTools.Ntuplizer.customizeMuons import customizeMuons
collections = customizeMuons(
    process,
    collections,
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

print 'Customizing taus'
from DevTools.Ntuplizer.customizeTaus import customizeTaus
collections = customizeTaus(
    process,
    collections,
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

print 'Customizing tausBoosted'
collections = customizeTaus(
    process,
    collections,
    srcLabel='tausBoosted',
    postfix='Boosted',
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

print 'Customizing photons'
from DevTools.Ntuplizer.customizePhotons import customizePhotons
collections = customizePhotons(
    process,
    collections,
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

print 'Customizing METs'
from DevTools.Ntuplizer.customizeMets import customizeMets
collections = customizeMets(
    process,
    collections,
    isMC=bool(options.isMC),
    reHLT=bool(options.reHLT),
)

######################
### select objects ###
######################
process.main_path = cms.Path()
process.main_path_boosted = cms.Path()

print 'Selecting objects'
from DevTools.Ntuplizer.objectTools import objectSelector, objectCleaner, objectCountFilter
for coll in selections:
    if coll=='tausBoosted':
        collections[coll] = objectSelector(process,'taus',collections[coll],selections[coll],postfix='Boosted')
    else:
        collections[coll] = objectSelector(process,coll,collections[coll],selections[coll])
collections['pfmet'] = objectSelector(process,'mets',collections['pfmet'],'')
# TODO: memory problem
#for coll in cleaning:
#    collections[coll] = objectCleaner(process,coll,collections[coll],collections,cleaning[coll])
for coll in minCounts:
    objectCountFilter(process,process.main_path,coll,collections[coll],minCounts[coll])
    objectCountFilter(process,process.main_path_boosted,coll,collections[coll],minCounts[coll])
process.schedule.append(process.main_path)
process.schedule.append(process.main_path_boosted)

#######################
### Combine objects ###
#######################
process.mumu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {0}@-".format(collections['muons'])),
    cut   = cms.string(""),
)
objectCountFilter(process,process.main_path,'mumu','mumu',1)
objectCountFilter(process,process.main_path_boosted,'mumu','mumu',1)

process.tautau = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {0}@-".format(collections['taus'])),
    cut   = cms.string(""),
)

process.mutau = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {1}@-".format(collections['muons'],collections['taus'])),
    cut   = cms.string(""),
)

process.etau = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {1}@-".format(collections['electrons'],collections['taus'])),
    cut   = cms.string(""),
)

process.emu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {1}@-".format(collections['electrons'],collections['muons'])),
    cut   = cms.string(""),
)

process.tautauBoosted = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {0}@-".format(collections['tausBoosted'])),
    cut   = cms.string(""),
)

process.mutauBoosted = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {1}@-".format(collections['muons'],collections['tausBoosted'])),
    cut   = cms.string(""),
)

process.etauBoosted = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("{0}@+ {1}@-".format(collections['electrons'],collections['tausBoosted'])),
    cut   = cms.string(""),
)

process.mumutautau = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu tautau"),
    cut   = cms.string(""),
)

process.mumumutau = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu mutau"),
    cut   = cms.string(""),
)

process.mumuetau = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu etau"),
    cut   = cms.string(""),
)

process.mumuemu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu emu"),
    cut   = cms.string(""),
)

process.mumutautauBoosted = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu tautauBoosted"),
    cut   = cms.string(""),
)

process.mumumutauBoosted = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu mutauBoosted"),
    cut   = cms.string(""),
)

process.mumuetauBoosted = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("mumu etauBoosted"),
    cut   = cms.string(""),
)

#####################
### define output ###
#####################
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('lumi_'+options.outputFile),
)

process.lumiTree = cms.EDAnalyzer("LumiTree",
    genEventInfo = cms.InputTag("generator"),
)
process.lumi_step = cms.Path(process.lumiTree)
process.schedule.append(process.lumi_step)

process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_TriggerResults_*_*',
        'keep *_generator_*_*',
        'keep *_fixedGridRho*_*_*',
        'keep *_patTrigger_*_*',
        'keep *_selectedPatTrigger_*_*',
        'keep *_*PileupInfo_*_*',
        #'keep *_bunchSpacingProducer_*_*',
        'keep *_{0}_*_*'.format(collections['vertices']),
        'keep *_{0}_*_*'.format(collections['electrons']),
        'keep *_{0}_*_*'.format(collections['muons']),
        'keep *_{0}_*_*'.format(collections['taus']),
        'keep *_{0}_*_*'.format(collections['tausBoosted']),
        #'keep *_{0}_*_*'.format(collections['photons']),
        #'keep *_{0}_*_*'.format(collections['jets']),
        'keep *_{0}_*_*'.format(collections['pfmet']),
        #'keep *_{0}_*_*'.format(collections['packed']),
        'keep *_{0}_*_*'.format(collections['genParticles']),
        'keep *_packedGenParticles_*_*',
        'keep *_mumu_*_*',
        'keep *_tautau*_*_*',
        'keep *_mutau*_*_*',
        'keep *_etau*_*_*',
        'keep *_emu*_*_*',
        'keep *_mumutautau*_*_*',
        'keep *_mumumutau*_*_*',
        'keep *_mumuetau*_*_*',
        'keep *_mumuemu*_*_*',
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('main_path','main_path_boosted'),
    ),
)
process.out_step = cms.EndPath(process.out)
process.schedule.append(process.out_step)
