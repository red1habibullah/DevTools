# Setup parameters to validate ntuplizer

params = {
    'data': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2016G/DoubleMuon/MINIAOD/03Feb2017-v1/100000/00182C13-EEEA-E611-8897-001E675A6C2A.root',
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
