from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR

import itertools
import operator

import ROOT

class DijetFakeRateAnalysis(AnalysisBase):
    '''
    Select a single lepton to performa dijet control fake rate
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','dijetTree.root')
        outputTreeName = kwargs.pop('outputTreeName','DijetTree')
        super(WZAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup cut tree
        self.cutTree.add(self.vetoSecond,'vetoSecond')
        self.cutTree.add(self.trigger,'trigger')

        # setup analysis tree

        # chan string
        self.tree.add(self.getChannelString, 'channel', ['C',2])

        # event counts
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',15), 'numJetsLoose15', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',15), 'numJetsTight15', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',15), 'numBjetsTight15', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',20), 'numJetsLoose20', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',20), 'numJetsTight20', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',20), 'numBjetsTight20', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',30), 'numJetsLoose30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',30), 'numJetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',30), 'numBjetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passLoose)), 'numLooseElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passMedium)), 'numMediumElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passTight)), 'numTightElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passLoose)), 'numLooseMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passMedium)), 'numMediumMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passTight)), 'numTightMuons', 'I')

        # pileup
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'vertices_count'), 'numVertices', 'I')

        # gen
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'nTrueVertices'), 'numTrueVertices', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'NUP'), 'NUP', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'isData'), 'isData', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'genWeight'), 'genWeight', 'I')

        # trigger
        triggers = [
            'Mu8_TrkIsoVVL',
            'Mu17_TrkIsoVVL',
            'Mu24_TrkIsoVVL',
            'Mu34_TrkIsoVVL',
            'Ele12_CaloIdL_TrackIdL_IsoVL',
            'Ele17_CaloIdL_TrackIdL_IsoVL',
            'Ele23_CaloIdL_TrackIdL_IsoVL',
        ]
        for trigger in triggers:
            self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'{0}Pass'.format(trigger)), 'pass{0}'.format(trigger), 'I')

        # lead jet
        self.addJet('leadJet')

        # lepton
        self.addLeptonMet('w','l1',('pfmet',0))
        self.addLepton('l1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['l1']), 'l1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['l1']), 'l1_passTight', 'I')

        # met
        self.addMet('met',('pfmet',0))

    #############################
    ### select fake candidate ###
    #############################
    def selectCandidates(self,rtrow):
        candidate = {
            'l1' : (),
            'leadJet' : (),
        }

        # get leptons
        colls = ['electrons','muons']
        pts = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        if len(leps)<1: return candidate # need at least 1 lepton

        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')

        # choose highest pt
        l = sorted(pts.items(), key=operator.itemgetter(1))[-1][0]

        candidate['l1'] = l

        # add jet
        jets = self.getCands(rtrow, 'jets', lambda rtrow,cand: self.getObjectVariable(rtrow,cand,'isLoose')>0.5)
        if len(jets)>0:
            candidate['leadJet'] = jets[0]
        else:
            candidate['leadJet'] = ('jets',-1)

        return candidate

    ##################
    ### lepton IDs ###
    ##################
    def passLoose(self,rtrow,cand):
        pt = self.getObjectVariable(rtrow,cand,'pt')
        eta = self.getObjectVariable(rtrow,cand,'eta')
        if cand[0]=="electrons":
            if pt<=10: return False
            if abs(eta)>=2.5: return False
            if self.getObjectVariable(rtrow,cand,'wwLoose')<0.5: return False
        elif cand[0]=="muons":
            if pt<=10: return False
            if abs(eta)>=2.4: return False
            isMediumMuon = self.getObjectVariable(rtrow,cand,'isMediumMuon')
            if isMediumMuon<0.5: return False
            trackIso = self.getObjectVariable(rtrow,cand,'trackIso')
            if trackIso/pt>=0.4: return False
            pfRelIsoDB = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
            if pfRelIsoDB>=0.4: return False
        else:
            return False
        return True

    def passMedium(self,rtrow,cand):
        if not self.passLoose(rtrow,cand): return False
        if cand[0]=="electrons":
            if self.getObjectVariable(rtrow,cand,'cutBasedMedium')<0.5: return False
        elif cand[0]=="muons":
            dz = self.getObjectVariable(rtrow,cand,'dz')
            if abs(dz)>=0.1: return False
            pt = self.getObjectVariable(rtrow,cand,'pt')
            dxy = self.getObjectVariable(rtrow,cand,'dxy')
            if abs(dxy)>=0.01 and pt<20: return False
            if abs(dxy)>=0.02 and pt>=20: return False
            pfRelIsoDB = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
            if pfRelIsoDB>=0.15: return False
        else:
            return False
        return True

    def passTight(self,rtrow,cand):
        if not self.passLoose(rtrow,cand): return False
        if cand[0]=="electrons":
            if self.getObjectVariable(rtrow,cand,'cutBasedTight')<0.5: return False
        elif cand[0]=="muons":
            return self.passMedium(rtrow,cand)
        else:
            return False
        return True

    def getPassingCands(self,rtrow,mode):
        if mode=='Loose':
            passMode = self.passLoose
        elif mode=='Medium':
            passMode = self.passMedium
        elif mode=='Tight':
            passMode = self.passTight
        else:
            return []
        cands = []
        for coll in ['electrons','muons']:
            cands += self.getCands(rtrow,coll,passMode)
        return cands

    def numJets(self,rtrow,mode,pt):
        return len(
            self.getCands(
                rtrow,
                'jets',
                lambda rtrow,cand: self.getObjectVariable(rtrow,cand,mode)>0.5 
                                   and self.getObjectVariable(rtrow,cand,'pt')>pt
            )
        )

    ######################
    ### channel string ###
    ######################
    def getChannelString(self,rtrow,cands):
        '''Get the channel string'''
        chanString = ''
        for c in ['l1']:
            chanString += self.getCollectionString(cands[c])
        return chanString

    ###########################
    ### analysis selections ###
    ###########################
    def vetoSecond(self,rtrow,cands):
        return len(self.getPassingCands(rtrow,'Loose'))==1

    def trigger(self,rtrow,cands):
        triggerNames = {
            'DoubleMuon'     : [
                ['Mu8_TrkIsoVVL', 0],
                ['Mu17_TrkIsoVVL', 20],
                ['Mu24_TrkIsoVVL', 30],
                ['Mu34_TrkIsoVVL', 40],
            ],
            'DoubleEG'       : [
                ['Ele12_CaloIdL_TrackIdL_IsoVL', 0],
                ['Ele17_CaloIdL_TrackIdL_IsoVL', 20],
                ['Ele23_CaloIdL_TrackIdL_IsoVL', 30],
            ],
        }
        # here we need to accept only a specific trigger after a certain pt threshold
        pt = self.getObjectVariable(rtrow,cands['l1'],'pt')
        dataset = 'DoubleEG' if cands['l1'][0] == 'electrons' else 'DoubleMuon'
        # accept the event only if it is triggered in the current dataset
        reject = True if rtrow.isData>0.5 else False
        if dataset in self.fileNames[0]: reject = False
        # now pick the appropriate trigger for the pt
        theTrigger = ''
        for trig, ptThresh in triggerNames[dataset]:
            if pt < ptThresh: break
            theTrigger = trig
        # and check if we pass
        passTrigger = self.getTreeVariable(rtrow,'{0}Pass'.format(theTrigger))
        if passTrigger>0.5: return False if reject else True
        return False











