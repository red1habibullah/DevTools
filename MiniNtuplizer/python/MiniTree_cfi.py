import FWCore.ParameterSet.Config as cms

# load branches
from AnalysisTools.MiniNtuplizer.branchTemplates import *

miniTree = cms.EDAnalyzer("MiniTree",
    isData = cms.bool(True),
    genEventInfo = cms.InputTag("generator"),
    lheEventProduct = cms.InputTag("externalLHEProducer"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    pileupSummaryInfo = cms.InputTag("slimmedAddPileupInfo"),
    triggerResults = cms.InputTag("TriggerResults","","HLT"),
    filterResults = cms.InputTag("TriggerResults","","PAT"),
    triggerObjects = cms.InputTag("selectedPatTrigger"),
    triggerPrescales = cms.InputTag("patTrigger"),
    triggerBranches = triggerBranches,
    filterBranches = filterBranches,
    vertices = cms.InputTag("slimmedOfflinePrimaryVertices"),
    vertexBranches = cms.PSet(
        vertices = cms.PSet(
            maxCount = cms.uint32(100),
            branches = vertexBranches,
        ),
    ),
    genParticles = cms.InputTag("prunedGenParticles"),
    genParticleBranches = cms.PSet(
        genParticles = cms.PSet(
            maxCount = cms.uint32(10000),
            branches = genParticleBranches,
        ),
    ),
    electrons = cms.InputTag("slimmedElectrons"),
    electronBranches = cms.PSet(
        electrons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = electronBranches,
        ),
    ),
    muons = cms.InputTag("slimmedMuons"),
    muonBranches = cms.PSet(
        muons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = muonBranches,
        ),
    ),
    taus = cms.InputTag("slimmedTaus"),
    tauBranches = cms.PSet(
        taus = cms.PSet(
            maxCount = cms.uint32(100),
            branches = tauBranches,
        ),
    ),
    photons = cms.InputTag("slimmedPhotons"),
    photonBranches = cms.PSet(
        photons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = photonBranches,
        ),
    ),
    jets = cms.InputTag("slimmedJets"),
    jetBranches = cms.PSet(
        jets = cms.PSet(
            maxCount = cms.uint32(100),
            branches = jetBranches,
        ),
    ),
    mets = cms.InputTag("slimmedMETs"),
    metBranches = cms.PSet(
        pfmet = cms.PSet(
            maxCount = cms.uint32(1),
            branches = metBranches,
        ),
    ),
)
