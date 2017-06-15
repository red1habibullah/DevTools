# Setup parameters to validate ntuplizer

params = {
    # TODO: update to later sample when available
    'data': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2017A/DoubleMuon/MINIAOD/PromptReco-v2/000/296/174/00000/320C645C-6C4C-E711-B097-02163E01A59A.root',
            'isMC': 0,
        },
    },
    # TODO: update when campaign begins
    'mc': {
        'type': 'mc',
        'kwargs': {
            'inputFiles': '/store/relval/CMSSW_9_2_0/RelValZMM_13/MINIAODSIM/91X_upgrade2017_realistic_v5-v1/10000/AA51A5A2-1E3C-E711-950B-0CC47A78A440.root',
            'isMC': 1,
        },
    },
    # TODO: no MC yet
    #'signal': {
    #    'type': 'mc',
    #    'kwargs': {
    #        'inputFiles': '/store/mc/RunIISummer16MiniAODv2/HPlusPlusHMinusHTo3L_M-500_13TeV-calchep-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/08ECD723-E4CA-E611-8C93-0CC47A1E0DC2.root',
    #        'isMC': 1,
    #    },
    #},
    #'private': {
    #    'type': 'mc',
    #    'kwargs': {
    #        'inputFiles': '/store/user/dntaylor/HPlusPlusHMinusMinusHTo4L_M-500_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2_MINIAODSIM_v1/170217_204448/0000/dblh_1_1.root',
    #        'isMC': 1,
    #    },
    #},
}
