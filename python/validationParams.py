# Setup parameters to validate ntuplizer

params = {
    # TODO: update to later sample when available
    'data': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2017F/DoubleMuon/MINIAOD/17Nov2017-v1/50000/009DC3A2-A7DE-E711-99F7-02163E013717.root',
            'isMC': 0,
        },
    },
    # TODO: update when campaign begins
    'mc': {
        'type': 'mc',
        'kwargs': {
            'inputFiles': '/store/mc/RunIIFall17MiniAOD/WZ_TuneCP5_13TeV-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/60000/1C7C7FB8-14E6-E711-90A9-0025905A60FE.root',
            'isMC': 1,
        },
    },
    # TODO: no MC yet
    #'signal': {
    #    'type': 'mc',
    #    'kwargs': {
    #        'inputFiles': '',
    #        'isMC': 1,
    #    },
    #},
    #'private': {
    #    'type': 'mc',
    #    'kwargs': {
    #        'inputFiles': '',
    #        'isMC': 1,
    #    },
    #},
}
