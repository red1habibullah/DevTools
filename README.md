Ntuplizer
=========

The ntuplizer produces flat root files from MiniAOD EDM files.

Events are stored if they include at least one electron, muon, or tau.

Usage
-----

Use the configuration file [MiniTree_cfg.py](test/MiniTree_cfg.py).
This configuration supports the following files:
 * MC
   * RunIISpring16MiniAODv2 (and reHLT)
 * Data
   * PromptReco (2016)

Options:
 * `inputFiles`: Standard cmsRun inputFiles argument for PoolSource.
 * `outputFile`: Standard cmsRun outputFile argument (uses TFileService). Default: `miniTree.root`.
 * `isMC`: Use if you are running over Monte Carlo. Default: `0` (for data).
 * `runMetFilter`: For use with data to apply the recommended MET filters. Default: `0`.
 * `reHLT`: For use with reHLT MC. Default: `0`.

### Example

 * Data
```
cmsRun DevTools/Ntuplizer/test/MiniTree_cfg.py runMetFilter=1 inputFiles=/store/data/Run2016D/DoubleEG/MINIAOD/PromptReco-v2/000/276/363/00000/108E3BB6-5F46-E611-94C5-02163E01381C.root
```

 * MC
```
cmsRun DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1 inputFiles=/store/mc/RunIISpring16MiniAODv2/ZZTo4L_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/00000/024C8A3E-7D1A-E611-A094-002590494C82.root
```

Grid Submission
---------------

Jobs can be submitted to the grid using the [submit_job.py](../Utilities/scripts/submit_job.py) script.

See `submit_job.py -h` for help.

You must first source the crab environment:

```
source /cvmfs/cms.cern.ch/crab3/crab.sh
```

The `--dryrun` option will tell crab to submit a test job and report the success or failure.
It will also give you estimated runtimes. When you are ready to submit, remove the `--dryrun` option.
You will also need to change the `jobName` option.

### Example

 * Data
```
submit_job.py crabSubmit --sampleList datasetList_Data.txt --applyLumiMask --dryrun testDataSubmission_v1 DevTools/Ntuplizer/test/MiniTree_cfg.py runMetFilter=1
```

 * MC
```
submit_job.py crabSubmit --sampleList datasetList_MC.txt --dryrun testMCSubmission_v1 DevTools/Ntuplizer/test/MiniTree_cfg.py isMC=1
```

