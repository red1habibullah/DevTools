#include "DevTools/Ntuplizer/interface/LumiSummaryBranches.h"

LumiSummaryBranches::LumiSummaryBranches(TTree * tree, const edm::ParameterSet& iConfig, edm::ConsumesCollector cc):
    genEventInfoToken_(cc.consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("genEventInfo")))
{
  // add branches
  tree->Branch("run", &runBranch_, "run/I");
  tree->Branch("lumi", &lumiBranch_, "lumi/I");
  tree->Branch("nevents", &neventsBranch_, "nevents/I");
  tree->Branch("summedWeights", &summedWeightsBranch_, "summedWeights/F");
}

void LumiSummaryBranches::beginLumi(const edm::LuminosityBlock& iEvent)
{
  runBranch_ = iEvent.run();
  lumiBranch_ = iEvent.luminosityBlock();
  neventsBranch_ = 0;
  summedWeightsBranch_ = 0;
}

void LumiSummaryBranches::fill(const edm::Event& iEvent)
{
  edm::Handle<GenEventInfoProduct> genEventInfo;
  iEvent.getByToken(genEventInfoToken_, genEventInfo);

  neventsBranch_++;
  Float_t genWeight = 0.;
  if (genEventInfo.isValid()) {
      genWeight = genEventInfo->weight();
  }
  summedWeightsBranch_ += genWeight;
}

