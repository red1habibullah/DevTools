# Setup parameters to validate ntuplizer

params = {
    'promptreco': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2016H/DoubleMuon/MINIAOD/PromptReco-v3/000/284/036/00000/64591DD7-A79F-E611-954C-FA163E5A1368.root',
            'isMC': 0,
        },
    },
    'rereco': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2016G/DoubleMuon/MINIAOD/23Sep2016-v1/100000/0A30F7A9-ED8F-E611-91F1-008CFA1C6564.root',
            'isMC': 0,
        },
    },
    'mc': {
        'type': 'mc',
        'kwargs': {
            'inputFiles': '/store/mc/RunIISummer16MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/2E1C211C-05C2-E611-90D3-02163E01306F.root',
            'isMC': 1,
        },
    },
    'signal': {
        'type': 'mc',
        'kwargs': {
            'inputFiles': '/store/mc/RunIISummer16MiniAODv2/HPlusPlusHMinusHTo3L_M-500_13TeV-calchep-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/08ECD723-E4CA-E611-8C93-0CC47A1E0DC2.root',
            'isMC': 1,
        },
    }
}
