import os

import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'miniTree.root'
#options.inputFiles= '/store/mc/RunIISummer16MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/2E1C211C-05C2-E611-90D3-02163E01306F.root' # WZ
#options.inputFiles = '/store/mc/RunIISummer16MiniAODv2/HPlusPlusHMinusHTo3L_M-500_13TeV-calchep-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/08ECD723-E4CA-E611-8C93-0CC47A1E0DC2.root' # Hpp3l
options.inputFiles = '/store/data/Run2016G/DoubleMuon/MINIAOD/23Sep2016-v1/100000/0A30F7A9-ED8F-E611-91F1-008CFA1C6564.root' # ReReco
#options.inputFiles = '/store/data/Run2016H/DoubleMuon/MINIAOD/PromptReco-v3/000/284/036/00000/64591DD7-A79F-E611-954C-FA163E5A1368.root' # PromptReco
options.maxEvents = -1
options.register('skipEvents', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Events to skip")
options.register('reportEvery', 100, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Report every")
options.register('isMC', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")
options.register('reHLT', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is reHLT")
options.register('runMetFilter', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Run the recommended MET filters")

options.parseArguments()

#####################
### setup process ###
#####################

process = cms.Process("MiniNtuple")

process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.Services_cff')

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
)

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
)

#################
### GlobalTag ###
#################
envvar = 'mcgt' if options.isMC else 'datagt'
from Configuration.AlCa.GlobalTag import GlobalTag
#GT = {'mcgt': 'auto:run2_mc', 'datagt': 'auto:run2_data'}
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
# https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
GT = {'mcgt': '80X_mcRun2_asymptotic_2016_TrancheIV_v6', 'datagt': '80X_dataRun2_2016SeptRepro_v4'}
process.GlobalTag = GlobalTag(process.GlobalTag, GT[envvar], '')

##################
### JEC source ###
##################
# this is if we need to override the jec in global tag
sqfile = 'DevTools/Ntuplizer/data/{0}.db'.format('Spring16_23Sep2016V2_MC' if options.isMC else 'Spring16_23Sep2016AllV2_DATA')
#sqfile = 'src/DevTools/Ntuplizer/data/{0}.db'.format('Spring16_23Sep2016V2_MC' if options.isMC else 'Spring16_23Sep2016AllV2_DATA') # uncomment to submit to crab
tag = 'JetCorrectorParametersCollection_Spring16_23Sep2016AllV2_DATA_AK4PFchs'
if options.isMC: tag = 'JetCorrectorParametersCollection_Spring16_23Sep2016V2_MC_AK4PFchs' # MoriondMC
process.load("CondCore.DBCommon.CondDBCommon_cfi")
from CondCore.DBCommon.CondDBSetup_cfi import *
process.jec = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0)
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string(tag),
            label  = cms.untracked.string('AK4PFchs')
        ),
    ), 
    connect = cms.string('sqlite:{0}'.format(sqfile)),
)
process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

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

process.TFileService = cms.Service("TFileService", 
    fileName = cms.string(options.outputFile),
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
    'photons'      : 'slimmedPhotons',
    'jets'         : 'slimmedJets',
    'pfmet'        : 'slimmedMETs',
    'rho'          : 'fixedGridRhoFastjetAll',
    'vertices'     : 'offlineSlimmedPrimaryVertices',
    'packed'       : 'packedPFCandidates',
}

# the selections for each object (to be included in ntuple)
# will always be the last thing done to the collection, so can use embedded things from previous steps
selections = {
    'electrons' : 'pt>7 && abs(eta)<3.0',
    'muons'     : 'pt>5 && abs(eta)<2.5',
    'taus'      : 'pt>17 && abs(eta)<2.3',
    'photons'   : 'pt>10 && abs(eta)<3.0',
    'jets'      : 'pt>15 && abs(eta)<4.7',
}

# selection for cleaning (objects should match final selection)
# just do at analysis level
cleaning = {
    #'jets' : {
    #    'electrons' : {
    #        'cut' : 'pt>10 && abs(eta)<2.5 && userInt("cutBasedElectronID-Spring15-25ns-V1-standalone-medium")>0.5 && userInt("WWLoose")>0.5',
    #        'dr'  : 0.3,
    #    },
    #    'muons' : {
    #        'cut' : 'pt>10 && abs(eta)<2.4 && isMediumMuon>0.5 && trackIso/pt<0.4 && userFloat("dxy")<0.02 && userFloat("dz")<0.1 && (pfIsolationR04().sumChargedHadronPt+max(0.,pfIsolationR04().sumNeutralHadronEt+pfIsolationR04().sumPhotonEt-0.5*pfIsolationR04().sumPUPt))/pt<0.15',
    #        'dr'  : 0.3,
    #    },
    #    'taus' : {
    #        'cut' : 'pt>20 && abs(eta)<2.3 && tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")>0.5 && tauID("decayModeFinding")>0.5',
    #        'dr'  : 0.3,
    #    },
    #},
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
# ICHEP recommendation
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#MiniAOD_8011_ICHEP_dataset
for flag in ['HBHENoiseFilter','HBHENoiseIsoFilter','EcalDeadCellTriggerPrimitiveFilter','goodVertices','eeBadScFilter','globalTightHalo2016Filter']:
    mod = hltFilter.clone(HLTPaths=cms.vstring('Flag_{0}'.format(flag)))
    modName = 'filter{0}'.format(flag)
    setattr(process,modName,mod)
    filters += [getattr(process,modName)]
process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
filters += [process.BadChargedCandidateFilter]
# bad muon filters
process.badGlobalMuonTagger = cms.EDFilter("BadGlobalMuonTagger",
    muons = cms.InputTag(collections['muons']),
    vtx   = cms.InputTag(collections['vertices']),
    muonPtCut = cms.double(20),
    selectClones = cms.bool(False),
    taggingMode = cms.bool(False),
    verbose = cms.untracked.bool(False),
)
process.cloneGlobalMuonTagger = process.badGlobalMuonTagger.clone(
    selectClones = True
)

process.noBadGlobalMuons = cms.Sequence(~process.cloneGlobalMuonTagger + ~process.badGlobalMuonTagger)
filters += [process.cloneGlobalMuonTagger, process.badGlobalMuonTagger]
    

# now do any customization/cleaning
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

# select desired objects
print 'Selecting objects'
from DevTools.Ntuplizer.objectTools import objectSelector, objectCleaner
for coll in selections:
    collections[coll] = objectSelector(process,coll,collections[coll],selections[coll])
# TODO: memory problem
#for coll in cleaning:
#    collections[coll] = objectCleaner(process,coll,collections[coll],collections,cleaning[coll])

# add the analyzer
process.load("DevTools.Ntuplizer.MiniTree_cfi")

process.miniTree.isData = not options.isMC
process.miniTree.filterResults = cms.InputTag('TriggerResults', '', 'PAT') if options.isMC else cms.InputTag('TriggerResults', '', 'RECO')
if options.reHLT:
    process.miniTree.triggerResults = cms.InputTag('TriggerResults', '', 'HLT2')
process.miniTree.vertexCollections.vertices.collection = collections['vertices']
if options.isMC:
    from DevTools.Ntuplizer.branchTemplates import genParticleBranches 
    process.miniTree.collections.genParticles = cms.PSet(
        collection = cms.InputTag(collections['genParticles']),
        branches = genParticleBranches,
    )
process.miniTree.collections.electrons.collection = collections['electrons']
process.miniTree.collections.muons.collection = collections['muons']
process.miniTree.collections.taus.collection = collections['taus']
#process.miniTree.collections.photons.collection = collections['photons']
process.miniTree.collections.jets.collection = collections['jets']
process.miniTree.collections.pfmet.collection = collections['pfmet']
process.miniTree.rho = collections['rho']

# add the bad muons (condensed info)
from DevTools.Ntuplizer.branchTemplates import *
process.miniTree.collections.muonsBadGlobal = cms.PSet(
    collection = cms.InputTag("badGlobalMuonTagger","bad"),
    branches = commonCandidates.clone(),
)
process.miniTree.collections.muonsCloneGlobal = cms.PSet(
    collection = cms.InputTag("cloneGlobalMuonTagger","bad"),
    branches = commonCandidates.clone(),
)

process.miniTreePath = cms.Path()
for f in filters:
    process.miniTreePath += cms.ignore(f)
process.miniTreePath += process.miniTree
process.schedule.append(process.miniTreePath)
