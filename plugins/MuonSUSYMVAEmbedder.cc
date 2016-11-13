// MuonSUSYMVAEmbedder.cc
// Embeds muons ids as userInts for later

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

class MuonSUSYMVAEmbedder : public edm::stream::EDProducer<>
{
public:
  explicit MuonSUSYMVAEmbedder(const edm::ParameterSet&);
  ~MuonSUSYMVAEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  void beginJob() {}
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endJob() {}

  bool isPreselection(const pat::Muon& mu, const reco::Vertex& pv);
  float getEA(const pat::Muon& mu);

  // Data
  edm::EDGetTokenT<edm::View<pat::Muon> > collectionToken_;       // input collection
  edm::EDGetTokenT<reco::VertexCollection> vertexToken_;          // vertices
  edm::EDGetTokenT<double> rhoToken_;                             // rho
  std::auto_ptr<std::vector<pat::Muon> > out;                     // Collection we'll output at the end
};

// Constructors and destructors
MuonSUSYMVAEmbedder::MuonSUSYMVAEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("src"))),
  vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc"))),
  rhoToken_(consumes<double>(iConfig.getParameter<edm::InputTag>("rhoSrc")))
{
  produces<std::vector<pat::Muon> >();
}

void MuonSUSYMVAEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Muon> >(new std::vector<pat::Muon>);

  edm::Handle<edm::View<pat::Muon> > collection;
  iEvent.getByToken(collectionToken_, collection);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vertexToken_, vertices);

  const reco::Vertex& pv = *vertices->begin();

  edm::Handle<double> rho;
  iEvent.getByToken(rhoToken_, rho);

  for (size_t c = 0; c < collection->size(); ++c) {
    const auto obj = collection->at(c);
    pat::Muon newObj = obj;

    newObj.addUserFloat("SUSYEA", getEA(obj));
    newObj.addUserFloat("SUSYRho", (float)(*rho));
    newObj.addUserInt("isSUSYMVAPreselection", isPreselection(obj,pv));
    
    out->push_back(newObj);
  }

  iEvent.put(out);
}

// Preselection
// https://twiki.cern.ch/twiki/bin/view/CMS/LeptonMVA
bool MuonSUSYMVAEmbedder::isPreselection(const pat::Muon & mu, const reco::Vertex& pv) 
  {
    bool pre = muon::isLooseMuon(mu) &&
               mu.userFloat("MiniIsolation") < 0.4 &&
               fabs(mu.dB(pat::Muon::PV3D))/mu.edB(pat::Muon::PV3D) < 8. &&
               fabs(mu.innerTrack()->dxy(pv.position())) < 0.05 &&
               fabs(mu.innerTrack()->dz(pv.position())) < 0.1;
    return pre;
  }

// Isolation and EA
// https://twiki.cern.ch/twiki/bin/view/CMS/SUSLeptonSF
float MuonSUSYMVAEmbedder::getEA(const pat::Muon & mu)
  {
    float ea = 0.;
    if (std::abs(mu.eta()) < 0.8)
      ea = 0.0735;
    if (std::abs(mu.eta()) >= 0.8 && std::abs(mu.eta()) < 1.3)
      ea = 0.0619;
    if (std::abs(mu.eta()) >= 1.3 && std::abs(mu.eta()) < 2.0)
      ea = 0.0465;
    if (std::abs(mu.eta()) >= 2.0 && std::abs(mu.eta()) < 2.2)
      ea = 0.0433;
    if (std::abs(mu.eta()) >= 2.2 && std::abs(mu.eta()) <= 2.5)
      ea = 0.0577;
    return ea;
  }


void MuonSUSYMVAEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(MuonSUSYMVAEmbedder);
