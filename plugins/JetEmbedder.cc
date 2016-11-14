#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "DataFormats/Math/interface/deltaR.h"

template<class T>
class JetEmbedder : public edm::stream::EDProducer<>
{
  public:
    explicit JetEmbedder(const edm::ParameterSet&);
    ~JetEmbedder() {}

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


  private:
    // Methods
    void beginJob() {}
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
    void endJob() {}

    edm::EDGetTokenT<edm::View<T> > collectionToken_;
    edm::EDGetTokenT<edm::View<pat::Jet> > jetSrcToken_;
    std::auto_ptr<std::vector<T> > out;
};

// Constructors and destructors
template<class T>
JetEmbedder<T>::JetEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<T> >(iConfig.getParameter<edm::InputTag>("src"))),
  jetSrcToken_(consumes<edm::View<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jetSrc")))
{
  produces<std::vector<T> >();
}

template<class T>
void JetEmbedder<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<T> >(new std::vector<T>);

  edm::Handle<edm::View<T> > collection;
  iEvent.getByToken(collectionToken_, collection);

  edm::Handle<edm::View<pat::Jet> > jets;
  iEvent.getByToken(jetSrcToken_, jets);

  for (size_t c = 0; c < collection->size(); ++c) {
    const auto obj = collection->at(c);
    T newObj = obj;

    edm::Ptr<pat::Jet> closestJet;
    double closestDeltaR = std::numeric_limits<double>::infinity();

    for (size_t j = 0; j < jets->size(); ++j) {
      edm::Ptr<pat::Jet> jet = jets->ptrAt(j);
      double deltaR = reco::deltaR(obj,*jet);
      if (deltaR < closestDeltaR) {
        closestDeltaR = deltaR;
        closestJet = jet;
      }
    }

    newObj.addUserCand("jet", closestJet);
    newObj.addUserInt("jet_chargedHadronMultiplicity", closestJet->chargedHadronMultiplicity());
    newObj.addUserFloat("jet_pfCombinedInclusiveSecondaryVertexV2BJetTags", closestJet->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"));

    out->push_back(newObj);
  }

  iEvent.put(out);
}

template<class T>
void JetEmbedder<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}



#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
typedef JetEmbedder<pat::Tau> TauJetEmbedder;
typedef JetEmbedder<pat::Muon> MuonJetEmbedder;
typedef JetEmbedder<pat::Electron> ElectronJetEmbedder;
typedef JetEmbedder<pat::Photon> PhotonJetEmbedder;
DEFINE_FWK_MODULE(TauJetEmbedder);
DEFINE_FWK_MODULE(MuonJetEmbedder);
DEFINE_FWK_MODULE(ElectronJetEmbedder);
DEFINE_FWK_MODULE(PhotonJetEmbedder);
