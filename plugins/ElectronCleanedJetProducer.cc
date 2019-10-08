// -*- C++ -*-
//
// Package:    ElectronCleanedJetProducer
// Class:      ElectronCleanedJetProducer
// 
/**\class ElectronCleanedJetProducer MuonCleanedJetProducer.cc
   
 1;5202;0c  
   Description: Removes PF Electrons from PFJet candidates and reconstructs the jets
	          Associates those Electrons to the jets from which they were removed
		  
		  Implementation:
		  [Notes on implementation]
*/
//
// Original Author:  Francesca Ricci-Tam,6 R-025,+41227672274,
//     Contributer:  Devin Taylor,
//         Contributor: Redwan Habibullah
//         Created:  Fri Aug 31 13:01:48 CEST 2012
//
//


// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronCore.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronCoreFwd.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "TLorentzVector.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"


#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "TMath.h"

//
// class declaration
//

class ElectronCleanedJetProducer : public edm::stream::EDProducer<>
{
   public:
      explicit ElectronCleanedJetProducer(const edm::ParameterSet&);
      ~ElectronCleanedJetProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
 
  typedef edm::AssociationMap<edm::OneToMany<std::vector<reco::PFJet>, std::vector<reco::PFCandidate>, unsigned int> >
  JetToPFCandidateAssociation;     
      // ----------member data ---------------------------

      // source of the jets to be cleaned of electrons
  edm::EDGetTokenT<reco::PFJetCollection> jetSrc_;
  
  // source of electrons that, if found within jet, should be removed
  //edm::EDGetTokenT<reco::MuonCollection> muonSrc_;
  edm::EDGetTokenT<reco::GsfElectronRefVector> electronSrc_;
  //edm::EDGetTokenT<edm::RefVector<reco::GsfElectronCollection> > electronSrc_;
  // source of PF candidates
  edm::EDGetTokenT<reco::PFCandidateCollection> pfCandSrc_;
  edm::EDGetTokenT<edm::View<reco::PFCandidate> > pfCandToken_;
  
  //edm::EDGetTokenT<edm::View<reco::PFCandidate> > pfCandSrc_;
  //edm::EDGetTokenT<reco::TrackCollection> TKOrigs_;
  //edm::EDGetTokenT<edm::Association<reco::PFCandidateCollection> > pfCandMapSrc_;

  //edm::EDGetTokenT<pat::PackedCandidateCollection> packedCandSrc_;

  //edm::EDGetTokenT<edm::Association<reco::PFCandidateCollection> > pfCandMapSrc_;

  edm::ParameterSet* cfg_;

  int E_count=0;
  int PF_count=0;
  int Rem_count=0;
  //std::vector<int> Count; 
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
ElectronCleanedJetProducer::ElectronCleanedJetProducer(const edm::ParameterSet& iConfig):
  jetSrc_(consumes<reco::PFJetCollection>(iConfig.getParameter<edm::InputTag>("jetSrc"))),
  //muonSrc_(consumes<reco::MuonCollection>(iConfig.getParameter<edm::InputTag>("muonSrc"))),
  electronSrc_(consumes<reco::GsfElectronRefVector>(iConfig.getParameter<edm::InputTag>("electronSrc"))),
  //electronSrc_(consumes<edm::RefVector<reco::GsfElectronCollection> >(iConfig.getParameter<edm::InputTag>("electronSrc"))),
  pfCandSrc_(consumes<reco::PFCandidateCollection>(iConfig.getParameter<edm::InputTag>("pfCandSrc"))),
  pfCandToken_(consumes<edm::View<reco::PFCandidate> >( iConfig.getParameter<edm::InputTag>("pfCandCollection")))
  //TKOrigs_(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("originalTracks"))),
  //pfCandMapSrc_(consumes<edm::Association<reco::PFCandidateCollection> >(iConfig.getParameter<edm::InputTag>("pfCandMapSrc"))),
  //packedCandSrc_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("packedCandSrc")))

  
  //pfCandSrc_(consumes<edm::View<reco::PFCandidate> >( iConfig.getParameter<edm::InputTag>("pfCandSrc") ))
{
  cfg_ = const_cast<edm::ParameterSet*>(&iConfig);
  
  //register your products
  produces<reco::PFJetCollection>();
  produces<edm::ValueMap<bool> >( "jetCleanedValueMap" );
  //produces<edm::ValueMap<reco::MuonRefVector> >( "cleanedMuonsRefValueMap" );
  //produces<edm::ValueMap<reco::PFJetRef> >( "uncleanedJetRefValueMap" );
  //produces<reco::PFCandidateCollection>( "particleFlowElectronCleaned" );
  produces<JetToPFCandidateAssociation>("pfCandAssocMapForIsolation");
  //produces<pat::PackedCandidateCollection>("packedPFCandidatesElectronCleaned");
  //produces<edm::Association<pat::PackedCandidateCollection> >("packedPFCandidatesElectronCleanedAssociation");
  ////produces<reco::PFCandidateCollection > ("JetPfCandidates");
  //produces<edm::Ref<reco::PFCandidateCollection> >("particleFlowElectronCleaned"); 
  //produces<edm::PtrVector<reco::PFCandidate> >("particleFlowElectronCleaned");
}


ElectronCleanedJetProducer::~ElectronCleanedJetProducer()
{
  
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
ElectronCleanedJetProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace std;
  edm::Handle<reco::PFJetCollection> pfJets;
  iEvent.getByToken(jetSrc_, pfJets);
  std::unique_ptr<reco::PFJetCollection> SetOfJets( new reco::PFJetCollection );
  std::unique_ptr<reco::PFJetCollection> cleanedJets = std::make_unique<reco::PFJetCollection>();
  
//edm::Handle<reco::MuonCollection> muons;
  edm::Handle<reco::GsfElectronRefVector> electrons;
  //edm::Handle<edm::RefVector<reco::GsfElectronCollection> > electrons;
  iEvent.getByToken(electronSrc_, electrons);
  
  edm::Handle<reco::PFCandidateCollection> pfCands;
  iEvent.getByToken(pfCandSrc_, pfCands);
  
  edm::Handle< edm::View<reco::PFCandidate> > pfCandHandle;
  iEvent.getByToken( pfCandToken_, pfCandHandle );
  
  //std::unique_ptr<reco::PFCandidateCollection> pfCandsExcludingElectrons(new reco::PFCandidateCollection);
  std::unique_ptr<reco::PFCandidateCollection> JetPFCand= std::make_unique<reco::PFCandidateCollection>();
  edm::RefProd<reco::PFJetCollection> selectedJetRefProd = iEvent.getRefBeforePut<reco::PFJetCollection>();
  ////edm::RefProd<reco::PFCandidateCollection> PfCandRefProd = iEvent.getRefBeforePut<reco::PFCandidateCollection> ("JetPfCandidates");


    auto selectedJetPFCandidateAssociationForIsolation =
      std::make_unique<JetToPFCandidateAssociation>(&iEvent.productGetter());

  //edm::Handle<reco::TrackCollection> TKOrigs;
  //iEvent.getByToken( TKOrigs_, TKOrigs );
  
  
  
  //edm::Handle<edm::Association<reco::PFCandidateCollection> > pfCandsMap;
  //iEvent.getByToken(pfCandMapSrc_, pfCandsMap);
  
  //edm::Handle<pat::PackedCandidateCollection> packedCands;
  // iEvent.getByToken(packedCandSrc_, packedCands);


  //std::unique_ptr<edm::Ref<reco::PFCandidateCollection> > pfCandsExcludingElectrons(new edm::Ref<reco::PFCandidateCollection>());
  //std::unique_ptr<edm::PtrVector<reco::PFCandidate> > pfCandsExcludingElectrons(new edm::PtrVector<reco::PFCandidate>()); 
  //fill an STL container with muon ref keys
  std::vector<unsigned int> electronRefKeys;
  std::vector<int> Count;
  //Count.clear();
  if (electrons.isValid()) 
  {
      for (reco::GsfElectronRefVector::const_iterator iElectron = electrons->begin(); iElectron != electrons->end(); ++iElectron)
	{
	  //std::cout << " Electron Loop " << std::endl;
	  electronRefKeys.push_back(iElectron->key());
	  //std::cout << "Electron in Loose Collection: " << iElectron->key() <<  " " << (*iElectron)->pt() <<  " "  << (*iElectron)->eta() <<  " "  << (*iElectron)->phi() <<std::endl;
	  ++E_count;
	}
  }
  
  //vector of bools holding the signal electron tag decision for each jet
  std::vector<bool> electronTagDecisions;
  // bool CountFlag=false;
 
  //map between new jet and refs to muons in the original collection that were removed
  //std::vector<reco::MuonRefVector> removedMuonMap;
  
  //map between new jet and ref to original jet
  //std::vector<reco::PFJetRef> oldJets;
  
  // Do cleaning
  //std::vector<unsigned int> JetPFRefKeys;
  //int iPf = 0;
  for (reco::PFJetCollection::const_iterator iJet = pfJets->begin(); iJet != pfJets->end(); ++iJet)
    {
      std::vector<reco::PFCandidatePtr> jetPFCands = iJet->getPFConstituents();
      reco::PFJet::Specific specs = iJet->getSpecific();
      math::XYZTLorentzVector pfmomentum;
      std::vector<edm::Ptr<reco::Candidate> > jetConstituents;
      jetConstituents.clear();
      //JetPFRefKeys.push_back(jetPFCands->key()); 
      //JetPFRefKeys.push_back(jetPFCands.key()); 
      //reco::PFCandidateRef jetPFCandRef(jetPFCands,iPf);
      //JetPFRefKeys.push_back(jetPFCandRef->key()); 
      //JetPFRefKeys.push_back(jetPFCandRef.key());
      //flag indicating whether >=0 muons were tagged for removal
      bool taggedElectronForRemoval = false;
      //bool CountFlag=false;
      //vector of removed muons for this jet
      //reco::MuonRefVector removedMuons;
      
      
      
      
      
      ////std::vector<unsigned int> JetPFRefKeys; 
      
      //std::cout<< " Jet Particle Content : "<< jetPFCands.size() << std::endl;
      /*for (std::vector<reco::PFCandidatePtr>::const_iterator i = jetPFCands.begin(); i != jetPFCands.end(); ++i)
	{
	  
	  cout<< " Jet ID : " <<i->id()<< endl;
	  cout<< "++++++++++++++++++++"<<endl;
	  //JetPFCand->push_back(**i);                                                                                                                                                                                                                                         
          //edm::Ref<reco::PFCandidateCollection> JetCollRef( PfCandRefProd, JetPFCand->size() - 1);                                                                                                                                                                           
          //JetPFRefKeys.push_back(JetCollRef.key());
	}
      
      */
      for (std::vector<edm::Ptr<reco::PFCandidate> >::iterator i = jetPFCands.begin(); i != jetPFCands.end(); ++i)
	{
	  reco::PFCandidate pfCand = *i;
       
	  
	  //bool CountFlag=false;
	  // Is the PF Candidate a muon?
	  if (pfCand.particleId() == 2) //Reference: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_7_1_17/doc/html/d8/d17/PFCandidate_8h_source.html
	    {
	      //std::cout << "Found a electron to check: "<< pfCand.gsfElectronRef().key() << " " << pfCand.pt() << " " << pfCand.eta() << " " << pfCand.phi() << std::endl;
	    ++PF_count;
	    //std::cout << "PF-Electrons in event:" << std::endl;
	    //for (reco::MuonRefVector::const_iterator iMuon = muons->begin(); iMuon != muons->end(); ++iMuon)
	    //{
	    //  //std::cout << " "<< "" << " " << iMuon->pt() << " " << iMuon->eta() << " " << iMuon->phi() << std::endl;
	    //  std::cout << " "<< iMuon->key() << std::endl;
	    //}
	    // get the ref to the corresponding muon
	    // and count one more PF muon
	    reco::GsfElectronRef theRecoElectron = pfCand.gsfElectronRef();
	    
	    //does this muon pass the desired muon ID?
	    std::vector<unsigned int>::const_iterator iElectron = std::find(electronRefKeys.begin(), electronRefKeys.end(), theRecoElectron.key());
	    
	    if (iElectron != electronRefKeys.end()) 
	      {
		specs.mElectronEnergy -= pfCand.p4().e();
		specs.mElectronMultiplicity -= 1;
		specs.mChargedEmEnergy -= pfCand.p4().e();
		specs.mChargedMultiplicity -= 1;
		//save tag decision for this muon
		taggedElectronForRemoval = true;
		//CountFlag= true;
		// add this muon ref to the vector of removed muons for this jet
		// iMuon - muonRefKeys.begin() is the index into muonRefKeys of the soft muon
		// since muonRefKeys was filled in order of muons, it is also the index into 
		// muons of the soft muon
		//removedMuons.push_back(muons->at(iMuon - muonRefKeys.begin())->masterRef());
		
		//std::cout << "Found an Electron to remove: "<< pfCand.gsfElectronRef().key() << " " << pfCand.pt() << " " << pfCand.eta() << " " << pfCand.phi() << std::endl;
		//std::cout <<" ********************************************************************************************************************************** " << std::endl;
		//++Rem_count;
		Count.push_back(pfCand.gsfElectronRef().key());
	      }
	    else
	      {
		pfmomentum += pfCand.p4(); // total p4()
		jetConstituents.push_back((*i));
		// cout<<"Electrons found to check but not matced and so not removed,but jet constitiuents still pushed back"<<endl; 
	      }
	  } //If its an electron->loop
	else // if it's not a muon
	  {
	    pfmomentum += pfCand.p4(); // total p4()
	    jetConstituents.push_back((*i));
	    //cout<<"No electron in pfCands but Jet const still pushed back"<<endl;
	  }
	//if(CountFlag)
	//{++Rem_count;
	//}
      } // loop over PF candidates
    
    // Build a new jet without the muon
    reco::PFJet electronfreePFJet(pfmomentum, specs, jetConstituents);
    SetOfJets->push_back( electronfreePFJet );
    cleanedJets->push_back( electronfreePFJet );
    //if at least 1 muon was tagged for removal, save a positive muon tag decision for this jet
    electronTagDecisions.push_back(taggedElectronForRemoval);
    
    edm::Ref<reco::PFJetCollection> jetRef(selectedJetRefProd, SetOfJets->size() - 1);
    //save the ref vector of removed muons
    //removedMuonMap.push_back(removedMuons);
    
    //ref to this (old) jet
    //oldJets.push_back(reco::PFJetRef(pfJets, iJet - pfJets->begin()));
    //if(CountFlag)                                                                                                                                                                                                                                                        
    //{++Rem_count;                                                                                                                                                                                                                                                      
    //} 
    for (size_t i = 0; i < pfCands->size(); ++i) 
      {
	reco::PFCandidateRef pfCandRef(pfCands,i);
	//cout<< " pfCandRef ptr: "<< pfCandRef->sourceCandidatePtr(0) << endl;
	//reco::
	bool ElectronFlag=false;
	if ((*pfCands)[i].particleId() == 2) {
	  reco::GsfElectronRef removedElRef = (*pfCands)[i].gsfElectronRef(); 
	  
	  std::vector<unsigned int>::const_iterator iElectron = std::find(electronRefKeys.begin(), electronRefKeys.end(), removedElRef.key());
	  if(iElectron != electronRefKeys.end())
	  {
	    //selectedJetPFCandidateAssociationForIsolation->insert(jetRef, pfCandRef);
	    ElectronFlag=true;
	  }
	  
	}
	

	/*
	
	  for (std::vector<reco::PFCandidatePtr>::const_iterator i = jetPFCands.begin(); i != jetPFCands.end(); ++i)                                                                                                                                                               
      {                                                                                                                                                                                                                                                                        
        //JetPFCand->push_back(**i);                                                                                                                                                                                                                                             
        //edm::Ref<reco::PFCandidateCollection> JetCollRef( PfCandRefProd, JetPFCand->size() - 1);                                                                                                                                                                               
        //JetPFRefKeys.push_back(JetCollRef.key());                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                               
	}                                                                                                                                                                                                                                                                        */
                                                                                                                                                                                                                                                                               
	
	
	/*
	else
	  {
	    std::vector<unsigned int>::const_iterator iJetPF = std::find(JetPFRefKeys.begin(), JetPFRefKeys.end(), pfCandRef.key());
	    
	    if(iJetPF != JetPFRefKeys.end())
	      {
		selectedJetPFCandidateAssociationForIsolation->insert(jetRef, pfCandRef);	  
		//cout<< " Makes no sense to me "<<endl;
	      }
	    if(iJetPF == JetPFRefKeys.end())
              {
                cout<<"Unmatched Jet and PF Candidate->Electron Case"<<endl; 
              }
	    
	  }
	*/
	
	if(!(ElectronFlag==true))
	  {
	    selectedJetPFCandidateAssociationForIsolation->insert(jetRef, pfCandRef);
	  }
	
      }
    
    } // loop over jets
  
  //fill an STL container of keys of removed muons
  //std::vector<unsigned int> removedMuRefKeys;
//for (std::vector<reco::MuonRefVector>::const_iterator iJet = removedMuonMap.begin(); iJet != removedMuonMap.end(); ++iJet)
//{
//  for (reco::MuonRefVector::const_iterator iRemovedMu = iJet->begin(); iRemovedMu != iJet->end(); ++iRemovedMu) 
//  {
//    removedMuRefKeys.push_back(iRemovedMu->key()); 
//  }
//}
 
// build a collection of PF candidates excluding muons
// we will still tag the jet as signal-like by the presence of a muon IN the jet, but this 
// ensures that such jets also cannot have the muon enter the isolation candidate collection
//unsigned int iCand=0; 
//std::unique_ptr<pat::PackedCandidateCollection> packedCandsExcludingElectrons(new pat::PackedCandidateCollection);
//std::vector<int> oldToNewPacked;
 

   
  
  
  /*for (reco::PFCandidateCollection::const_iterator iPFCand = pfCands->begin(); iPFCand != pfCands->end(); ++iPFCand) 
   {
     //reco::GsfElectronRef removedElRef = iPFCand->gsfElectronRef();
     //reco::PFCandidatePtr pfCandPtr(reco::PFCandidatePtr(pfCands,iCand));
     //reco::PFCandidateRef oldPFRef(pfCands, iCand);
     cout << " PF ID : " << iPFCand->sourceCandidatePtr(0).id() <<endl;
     cout<< "###############################################"<<endl;
   }
  */
 
     /*
     if ((removedElRef.isNonnull() && (std::find(electronRefKeys.begin(), electronRefKeys.end(), removedElRef.key()) == electronRefKeys.end())) || removedElRef.isNull()) 
       {
	 pfCandsExcludingElectrons->push_back(*iPFCand);
	 //packedCandsExcludingElectrons->push_back(packedCands->at(iCand));
	 //oldToNewPacked.push_back((*pfCandsMap)[oldPFRef].key());

	 //pfCandsExcludingElectrons->push_back(pfCandPtr);
	 //cout<<" Happening "<<endl;
       }
     
     
     */
  
  
      
  /* edm::ProductID viewProductID;
  if (!pfCandHandle->empty()) 
    {
    viewProductID = pfCandHandle->ptrAt(0).id();
    cout<< " pfHandle Product ID: " << viewProductID <<endl;
    }   
  */
  
  /*for(size_t i=0;i<pfCandHandle->size(); ++i) 
    {
      cout << " PF ID : " << pfCandHandle->ptrAt(i).id() <<endl;   
  
    }
  */

  //std::cout<< " PfCand Content : " << pfCands->size() <<std::endl;



 /*std::vector<int> oldToNewTk;
 unsigned int ntk= TKOrigs->size();
 for (unsigned int itk = 0; itk < ntk; itk++) {
   reco::TrackRef oldTkRef(TKOrigs, itk);
   oldToNewTk.push_back((*pfCandsMap)[oldTkRef].key());
 }

 */
  
const edm::OrphanHandle<reco::PFJetCollection> cleanedJetsRefProd = iEvent.put(std::move(cleanedJets));

//fill the value map of muon tag decision for each cleaned jet
  std::unique_ptr<edm::ValueMap<bool> > valMap(new edm::ValueMap<bool>());
  edm::ValueMap<bool>::Filler filler(*valMap);
  filler.insert(cleanedJetsRefProd, electronTagDecisions.begin(), electronTagDecisions.end());
  filler.fill();
  iEvent.put(std::move(valMap), "jetCleanedValueMap" );
  //std::cout<< " Electrons in Loose Collection: " <<  E_count  << " Electrons found among the PFCands in Jet:  " <<  PF_count  << " Electrons removed : " << Rem_count <<std::endl;  
  
  //fill the value map of removed muon refs for each cleaned jet
  //std::unique_ptr<edm::ValueMap<reco::MuonRefVector> > muonValMap(new edm::ValueMap<reco::MuonRefVector>());
  //edm::ValueMap<reco::MuonRefVector>::Filler muonFiller(*muonValMap);
  //muonFiller.insert(cleanedJetsRefProd, removedMuonMap.begin(), removedMuonMap.end());
  //muonFiller.fill();
  //iEvent.put(std::move(muonValMap), "cleanedMuonsRefValueMap" );

  //fill the value map of old jet refs for each cleaned jet
  //std::unique_ptr<edm::ValueMap<reco::PFJetRef> > jetValMap(new edm::ValueMap<reco::PFJetRef>());
  //edm::ValueMap<reco::PFJetRef>::Filler jetFiller(*jetValMap);
  //jetFiller.insert(cleanedJetsRefProd, oldJets.begin(), oldJets.end());
  //jetFiller.fill();
  //iEvent.put(std::move(jetValMap), "uncleanedJetRefValueMap" );

  //put the soft-muon-free PF cands into the event
  iEvent.put(std::move(SetOfJets));
  ////iEvent.put(std::move(JetPFCand), "JetPfCandidates" );
  //iEvent.put(std::move(pfCandsExcludingElectrons), "particleFlowElectronCleaned");
  iEvent.put(std::move(selectedJetPFCandidateAssociationForIsolation), "pfCandAssocMapForIsolation");
  /*
  const edm::OrphanHandle<pat::PackedCandidateCollection> newpacked = iEvent.put(std::move(packedCandsExcludingElectrons), "packedPFCandidatesElectronCleaned");
  
  std::unique_ptr<edm::Association<pat::PackedCandidateCollection> > packedCandsExcludingElectronsAssociation(new edm::Association<pat::PackedCandidateCollection>);
  edm::Association<pat::PackedCandidateCollection>::Filler fillerPackedCandsAssociation(*packedCandsExcludingElectronsAssociation);
  fillerPackedCandsAssociation.insert(newpacked, oldToNewPacked.begin(), oldToNewPacked.end());
  fillerPackedCandsAssociation.insert(TKOrigs, oldToNewTk.begin(), oldToNewTk.end());
  fillerPackedCandsAssociation.fill();
  iEvent.put(std::move(packedCandsExcludingElectronsAssociation),"packedPFCandidatesElectronCleanedAssociation");
  */

  /*if(CountFlag)
    {
      //++Rem_count;
      
   std::cout<< " Electron removed" <<std::endl;
   
   
    }
  */
  //std::cout<<" No of Electrons Removed "<<Count.size()<<endl;
}

// ------------ method called once each job just before starting event loop  ------------
void 
ElectronCleanedJetProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ElectronCleanedJetProducer::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ElectronCleanedJetProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ElectronCleanedJetProducer);
