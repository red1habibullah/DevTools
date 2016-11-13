// ElectronSUSYMVAEmbedder.cc
// Embeds elons ids as userInts for later

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

class ElectronSUSYMVAEmbedder : public edm::stream::EDProducer<>
{
public:
  explicit ElectronSUSYMVAEmbedder(const edm::ParameterSet&);
  ~ElectronSUSYMVAEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  void beginJob() {}
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endJob() {}

  bool isPreselection(const pat::Electron& el, const reco::Vertex& pv, bool passID);
  bool isTight(const pat::Electron & el, std::string nonTrigLabel);
  bool isVLoose(const pat::Electron & el, std::string nonTrigLabel);
  bool isVLooseFOIDEmu(const pat::Electron & el, std::string nonTrigLabel);
  bool isVLooseFOIDISOEmu(const pat::Electron & el, std::string nonTrigLabel);
  float getEA(const pat::Electron& el);

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > collectionToken_;  // input collection
  edm::EDGetTokenT<reco::VertexCollection> vertexToken_;         // vertices
  edm::EDGetTokenT<double> rhoToken_;                            // rho
  std::string nonTrigLabel_;                                     // embedded mva
  std::auto_ptr<std::vector<pat::Electron> > out;                // Collection we'll output at the end
};

// Constructors and destructors
ElectronSUSYMVAEmbedder::ElectronSUSYMVAEmbedder(const edm::ParameterSet& iConfig):
  collectionToken_(consumes<edm::View<pat::Electron> >(iConfig.getParameter<edm::InputTag>("src"))),
  vertexToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc"))),
  rhoToken_(consumes<double>(iConfig.getParameter<edm::InputTag>("rhoSrc"))),
  nonTrigLabel_(iConfig.getParameter<std::string>("mva"))
{
  produces<std::vector<pat::Electron> >();
}

void ElectronSUSYMVAEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > collection;
  iEvent.getByToken(collectionToken_, collection);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vertexToken_, vertices);

  const reco::Vertex& pv = *vertices->begin();

  edm::Handle<double> rho;
  iEvent.getByToken(rhoToken_, rho);

  for (size_t c = 0; c < collection->size(); ++c) {
    const auto obj = collection->at(c);
    pat::Electron newObj = obj;

    newObj.addUserFloat("SUSYEA", getEA(obj));
    newObj.addUserFloat("SUSYRho", (float)(*rho));
    bool isTightVal = isTight(obj,nonTrigLabel_);
    bool isVLooseVal = isVLoose(obj,nonTrigLabel_);
    bool isVLooseFOIDEmuVal = isVLooseFOIDEmu(obj,nonTrigLabel_);
    bool isVLooseFOIDISOEmuVal = isVLooseFOIDISOEmu(obj,nonTrigLabel_);
    newObj.addUserInt("isSUSYTight",isTightVal);
    newObj.addUserInt("isSUSYVLoose",isVLooseVal);
    newObj.addUserInt("isSUSYVLooseFOIDEmu",isVLooseFOIDEmuVal);
    newObj.addUserInt("isSUSYVLooseFOIDISOEmu",isVLooseFOIDISOEmuVal);
    newObj.addUserInt("isSUSYMVAPreselection", isPreselection(obj,pv,isVLooseFOIDEmuVal));
    
    out->push_back(newObj);
  }

  iEvent.put(out);
}

// Preselection
// https://twiki.cern.ch/twiki/bin/view/CMS/LeptonMVA
bool ElectronSUSYMVAEmbedder::isPreselection(const pat::Electron & el, const reco::Vertex& pv, bool passID)
  {
    bool pre = passID &&
               el.userFloat("MiniIsolation") < 0.4 &&
               fabs(el.dB(pat::Electron::PV3D))/el.edB(pat::Electron::PV3D) < 8. &&
               fabs(el.gsfTrack()->dxy(pv.position())) < 0.05 &&
               fabs(el.gsfTrack()->dz(pv.position())) < 0.1;
    return pre;
  }

// MVA working points
bool ElectronSUSYMVAEmbedder::isTight(const pat::Electron & el, std::string nonTrigLabel) 
  {
    double abseta = fabs(el.eta());
    float mva = el.userFloat(nonTrigLabel);
    bool pass = false;
    if (abseta<0.8) {
      pass = (mva>0.87);
    }
    else if (abseta<1.479) {
      pass = (mva>0.6);
    }
    else if (abseta<2.5) {
      pass = (mva>0.17);
    }

    return pass;
  }

bool ElectronSUSYMVAEmbedder::isVLoose(const pat::Electron & el, std::string nonTrigLabel) 
  {
    double abseta = fabs(el.eta());
    float mva = el.userFloat(nonTrigLabel);
    bool pass = false;
    if (abseta<0.8) {
      pass = (mva>-0.16);
    }
    else if (abseta<1.479) {
      pass = (mva>-0.65);
    }
    else if (abseta<2.5) {
      pass = (mva>-0.74);
    }

    return pass;
  }

bool ElectronSUSYMVAEmbedder::isVLooseFOIDEmu(const pat::Electron & el, std::string nonTrigLabel) 
  {
    double abseta = fabs(el.eta());
    float mva = el.userFloat(nonTrigLabel);
    bool pass = false;
    if (abseta<0.8) {
      pass = (mva>-0.7);
    }
    else if (abseta<1.479) {
      pass = (mva>-0.83);
    }
    else if (abseta<2.5) {
      pass = (mva>-0.92);
    }

    return pass;
  }

bool ElectronSUSYMVAEmbedder::isVLooseFOIDISOEmu(const pat::Electron & el, std::string nonTrigLabel) 
  {
    double abseta = fabs(el.eta());
    float mva = el.userFloat(nonTrigLabel);
    bool pass = false;
    if (abseta<0.8) {
      pass = (mva>-0.155);
    }
    else if (abseta<1.479) {
      pass = (mva>-0.56);
    }
    else if (abseta<2.5) {
      pass = (mva>-0.76);
    }

    return pass;
  }

// Isolation and EA
// https://twiki.cern.ch/twiki/bin/view/CMS/SUSLeptonSF
float ElectronSUSYMVAEmbedder::getEA(const pat::Electron & el)
  {
    float ea = 0.;
    if (std::abs(el.eta()) < 1.0)
      ea = 0.1752;
    if (std::abs(el.eta()) >= 1.0 && std::abs(el.eta()) < 1.479)
      ea = 0.1862;
    if (std::abs(el.eta()) >= 1.479 && std::abs(el.eta()) < 2.0)
      ea = 0.1411;
    if (std::abs(el.eta()) >= 2.0 && std::abs(el.eta()) < 2.2)
      ea = 0.1534;
    if (std::abs(el.eta()) >= 2.2 && std::abs(el.eta()) < 2.3)
      ea = 0.1903;
    if (std::abs(el.eta()) >= 2.3 && std::abs(el.eta()) < 2.4)
      ea = 0.2243;
    if (std::abs(el.eta()) >= 2.4 && std::abs(el.eta()) <= 2.5)
      ea = 0.2687;
    return ea;
  }


void ElectronSUSYMVAEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(ElectronSUSYMVAEmbedder);
