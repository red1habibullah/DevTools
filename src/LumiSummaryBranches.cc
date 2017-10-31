#include "DevTools/Ntuplizer/interface/LumiSummaryBranches.h"

LumiSummaryBranches::LumiSummaryBranches(TTree * tree, const edm::ParameterSet& iConfig, edm::ConsumesCollector cc):
    genEventInfoToken_(cc.consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("genEventInfo")))
{
  hasSummary_ = iConfig.exists("nevents") && iConfig.exists("summedWeights");
  if (hasSummary_) {
    neventsToken_ = cc.consumes<int, edm::InLumi>(iConfig.getParameter<edm::InputTag>("nevents"));
    summedWeightsToken_ = cc.consumes<float, edm::InLumi>(iConfig.getParameter<edm::InputTag>("summedWeights"));
  }
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
  if (hasSummary_) {
    edm::Handle<int> neventsHandle;
    iEvent.getByToken(neventsToken_, neventsHandle);

    edm::Handle<float> summedWeightsHandle;
    iEvent.getByToken(summedWeightsToken_, summedWeightsHandle);

    hasSummary_ = neventsHandle.isValid() and summedWeightsHandle.isValid();

    neventsBranch_ = hasSummary_ ? *neventsHandle : 0;
    summedWeightsBranch_ = hasSummary_ ? *summedWeightsHandle : 0;
  }
  else {
    neventsBranch_ = 0;
    summedWeightsBranch_ = 0;
  }
}

void LumiSummaryBranches::fill(const edm::Event& iEvent)
{
  if (hasSummary_) return;

  edm::Handle<GenEventInfoProduct> genEventInfo;
  iEvent.getByToken(genEventInfoToken_, genEventInfo);

  neventsBranch_++;
  Float_t genWeight = 0.;
  if (genEventInfo.isValid()) {
      genWeight = genEventInfo->weight();
  }
  summedWeightsBranch_ += genWeight;
}

