# BasalGangliaData
Basal Ganglia Data for Snudda


First request access from Johannes, currently only internal use for our group. But if you see this text, you probably already have access.

Download the git repository, both Snudda and BasalGangliaData should be in the same folder, eg. HBP/Snudda and HBP/BasalGangliaData.

```
git clone git@github.com:Hjorthmedh/BasalGangliaData.git
```

If you look at [runSnuddaSmall.sh](https://github.com/Hjorthmedh/Snudda/blob/master/examples/runSnuddaSmall.sh) you can see the line:

```
export SNUDDA_DATA="../../BasalGangliaData/data"
```

This is the key, it tells Snudda where BasalGangliaData is. If you run from a folder outer than Snudda/examples, or if you put BasalGangliaData somewhere else then this path might need to be different. So you need to set ```SNUDDA_DATA``` in your shellscript.




Before commiting new morphologies, please verify that they are centred at (0,0,0) using ```test_segmentid.py``` in ```Snudda/tests```.

```
export SNUDDA_DATA=/home/hjorth/HBP/BasalGangliaData/data/
python3 -m unittest test_segmentid.py
```

2021-01-12

New hash to work with tests of models

if you have created a network prior to january 8, either regenerate the network and rerun (the models are the same, only keys have changed) or revert back to the old keys, by

git checkout 2768cd6

