# BasalGangliaData
Basal Ganglia Data for Snudda

### Description of models

The multicompartmental models are described a parameter set, a morphology file (.swc) and the mechanisms.json (which describes how the ion channels are distributed on the reconstructed morphology). 

In each model folder, there is an additional file, meta.json.

Meta.json is a dictionary which contains - two levels of hash_keys, p* and m* and (nm* for neuromodulation). The * is calculated from the contents of the parameter set or morphology file (.swc) using hashlib.md5(contents_of_the_parameter_or_morphology).hexdigest(). This gives a hash specific for the contents of parameter/morphology. The hash is prefixed with either "p" or "m" for parameter and morphology, respectively.

The advantage of hash keys:
  - They are calculated from the contents of the file, hence is the model changes, the hash keys will change. Good for testing
  - Each model become identifiable based on two keys, p* and m*, which can be used during the simulation
  - We do not use lists for model files, which are dependent on the order of the models. Hence, sensitive for changes to files structure. 

For further information and help with converting new models into the abovedescribed format, email Johanna Frost Nylen, johanna.frost.nylen@ki.se.

### Access
First request access from Johannes, currently only internal use for our group. But if you see this text, you probably already have access.

### How to use BasalGangliaData
Download the git repository, both Snudda and BasalGangliaData should be in the same folder, eg. HBP/Snudda and HBP/BasalGangliaData.

```
git clone git@github.com:Hjorthmedh/BasalGangliaData.git
```

If you look at [runSnuddaSmall.sh](https://github.com/Hjorthmedh/Snudda/blob/master/examples/runSnuddaSmall.sh) you can see the line:

```
export SNUDDA_DATA="../../BasalGangliaData/data"
```

This is the key, it tells Snudda where BasalGangliaData is. If you run from a folder outer than Snudda/examples, or if you put BasalGangliaData somewhere else then this path might need to be different. So you need to set ```SNUDDA_DATA``` in your shellscript.


### Morphologies - new morphologies have to be centered

Before commiting new morphologies, please verify that they are centred at (0,0,0) using ```test_segmentid.py``` in ```Snudda/tests```.

```
export SNUDDA_DATA=/home/hjorth/HBP/BasalGangliaData/data/
python3 -m unittest test_segmentid.py
```
### Previous commits of the repository

When changes are made to the models, their hash names will changes and this affects the simulations. If you have to move to a previous commit, see below which commit could match when your network was created.

#### 2021-01-12

New hash to work with tests of models

if you have created a network prior to january 8, either regenerate the network and rerun (the models are the same, only keys have changed) or revert back to the old keys, by

git checkout 2768cd6

