# Setup parameters to validate ntuplizer

params = {
    'data': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2017F/SingleMuon/MINIAOD/17Nov2017-v1/010000/183BE17C-A5EC-E711-8F69-0025905A607E.root',
            'isMC': 0,
        },
    },
    'SingleMuon': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2017F/SingleMuon/MINIAOD/17Nov2017-v1/010000/183BE17C-A5EC-E711-8F69-0025905A607E.root',
            'isMC': 0,
        },
    },
    'JetHT': {
        'type': 'data',
        'kwargs': {
            'inputFiles': '/store/data/Run2017F/JetHT/MINIAOD/17Nov2017-v1/50000/801B2658-4FDF-E711-8A33-FA163E6013D7.root',
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
    'QCD': {
        'type': 'mc',
        'kwargs': {
            'inputFiles': '/store/mc/RunIIFall17MiniAODv2/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/068CC22F-FF41-E811-8073-0025901FB188.root',
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
