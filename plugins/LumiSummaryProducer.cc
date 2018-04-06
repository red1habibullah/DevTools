
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

//
// class declaration
//

class LumiSummaryProducer : public edm::one::EDProducer<edm::EndLuminosityBlockProducer,
                                                        edm::one::WatchLuminosityBlocks>
{
   public:
      explicit LumiSummaryProducer(const edm::ParameterSet&);
      ~LumiSummaryProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void beginLuminosityBlock(edm::LuminosityBlock const& Lumi, edm::EventSetup const&) override;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const& Lumi, edm::EventSetup const&) override;
      virtual void endLuminosityBlockProduce(edm::LuminosityBlock& Lumi, const edm::EventSetup& iSetup) override;
      virtual void endJob() ;
      
      // ----------member data ---------------------------
      edm::EDGetTokenT<GenEventInfoProduct> genEventInfoToken_;

      int nevents_;
      float summedWeights_;

};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
LumiSummaryProducer::LumiSummaryProducer(const edm::ParameterSet& iConfig):
  genEventInfoToken_(consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("genEventInfo")))
{

  //register your products
  produces<int,   edm::Transition::EndLuminosityBlock>("numberOfEvents");
  produces<float, edm::Transition::EndLuminosityBlock>("sumOfWeightedEvents");

}


LumiSummaryProducer::~LumiSummaryProducer() { }


//
// member functions
//

void
LumiSummaryProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<GenEventInfoProduct> genEventInfo;
  iEvent.getByToken(genEventInfoToken_, genEventInfo);

  nevents_++;
  float genWeight = 0.;
  if (genEventInfo.isValid()) {
      genWeight = genEventInfo->weight();
  }
  summedWeights_ += genWeight;

}

void LumiSummaryProducer::beginJob() { }

void LumiSummaryProducer::endJob() { }

void LumiSummaryProducer::beginLuminosityBlock(edm::LuminosityBlock const& Lumi, edm::EventSetup const& iSetup) {
    nevents_ = 0;
    summedWeights_ = 0;
}

void LumiSummaryProducer::endLuminosityBlock(edm::LuminosityBlock const& Lumi, edm::EventSetup const& iSetup) { }

void LumiSummaryProducer::endLuminosityBlockProduce(edm::LuminosityBlock& Lumi, const edm::EventSetup& iSetup) {
    std::unique_ptr<int> neventsProduct(new int(nevents_));
    Lumi.put(std::move(neventsProduct),       "numberOfEvents");
    std::unique_ptr<float> summedWeightsProduct(new float(summedWeights_));
    Lumi.put(std::move(summedWeightsProduct), "sumOfWeightedEvents");
}



void
LumiSummaryProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(LumiSummaryProducer);
