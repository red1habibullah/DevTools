# Setup parameters to validate ntuplizer

params = {
    'data': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2017F/SingleMuon/MINIAOD/17Nov2017-v1/010000/183BE17C-A5EC-E711-8F69-0025905A607E.root',
            'isMC': 0,
        },
    },
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
