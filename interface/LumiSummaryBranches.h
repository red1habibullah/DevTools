#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "TTree.h"

class LumiSummaryBranches {
  public:
    LumiSummaryBranches(TTree * tree, const edm::ParameterSet& iConfig, edm::ConsumesCollector cc);
    void beginLumi(const edm::LuminosityBlock& iEvent);
    void fill(const edm::Event& iEvent);

  private:
    edm::EDGetTokenT<GenEventInfoProduct> genEventInfoToken_;
    edm::EDGetTokenT<int> neventsToken_;
    edm::EDGetTokenT<float> summedWeightsToken_;
    bool hasSummary_;

    // branches
    Int_t   runBranch_;
    Int_t   lumiBranch_;
    Int_t   neventsBranch_;
    Float_t summedWeightsBranch_;

};
