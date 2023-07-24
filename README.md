# BasalGangliaData

## TODO in the next merge  

  * Update the morphologies for dSPN and iSPN without the in-soma dendrite point problem
  * Reoptimize the FS - morphology key and parameter key pairs in filters/striatum/fs/
  * Update the synapses from Cortex-Striatum
  * 

* To clean both BasalGangliaData and Snudda from previous commits of large files (data, models etc..) and remove from git history use: https://rtyley.github.io/bfg-repo-cleaner/

## Models within the Microcircuit group:

	* The striatum - healthy:
		found in: data/neurons/striatum; data/synapses/striatum; meshes/Striatum-d-*; density/ and nest/
		description: The control/healthy mouse striatum model
	* The striatum - Parkinsons:
		found in: Parkinson/20221213/PD0 (the striatum - healthy); Parkinson/20221213/PD1; Parkinson/20221213/PD2; Parkinson/20221213/PD3; Parkinson/20221213/PD_lesion;   
		description: Parkinsonian models - 3 stages and PD_lesion - which is equivalent to PD2 and contains completely models, the rest is morphological changes

## Versions of Basal Ganglia Data

To move between the different tags :

```
git checkout tags/tag_name
```

## Basal Ganglia Data for Snudda

### Description of models

The multicompartmental models are described by a parameter set, a morphology file (.swc), and the mechanisms.json (which describes how the ion channels are distributed on the reconstructed morphology). 

In each model folder, there is an additional file, meta.json.

Meta.json is a dictionary that contains - two levels of hash_keys, p* and m* and (nm* for neuromodulation). The * is calculated from the contents of the parameter set or morphology file (.swc) using hashlib.md5(contents_of_the_parameter_or_morphology).hexdigest(). This gives a hash specific to the contents of the parameter/morphology. The hash is prefixed with either "p" or "m" for parameter and morphology, respectively.

The advantage of hash keys:
  - They are calculated from the contents of the file, hence if the model changes, the hash keys will change. Good for testing
  - Each model becomes identifiable based on two keys, p* and m*, which can be used during the simulation
  - We do not use lists for model files, which are dependent on the order of the models. Hence, sensitive to changes to file structure. 

For further information and help with converting new models into the above-described format, email Johanna Frost Nylen, johanna.frost.nylen@ki.se.

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

This is the key, it tells Snudda where BasalGangliaData is. If you run from a folder outer than Snudda/examples, or if you put BasalGangliaData somewhere else then this path might need to be different. So you need to set ```SNUDDA_DATA``` in your shell script.


### Morphologies - new morphologies have to be centered

Before commiting new morphologies, please verify that they are centered at (0,0,0) using ```test_segmentid.py``` in ```Snudda/tests```.

```
export SNUDDA_DATA=/home/hjorth/HBP/BasalGangliaData/data/
python3 -m unittest test_segmentid.py
```
### Previous commits of the repository

When changes are made to the models, their hash names will changes and this affects the simulations. If you have to move to a previous commit, see below which commit could match when your network was created.

#### 2021-01-12

New hash to work with tests of models

if you have created a network prior to January 8, either regenerate the network and rerun (the models are the same, only keys have changed) or revert back to the old keys, by

git checkout 2768cd6

## Testing
BasalgangliaData uses unittest to test the code in tools/. To run tests:

```
python -m unittest discover tests/

```
Individual tests can be run by:

```
python -m unittest tests/name_of_test_file.py

```
Files with tests start with test_*, which is important when adding new tests.

To check if a piece of code has already been tested, generate a code coverage report:

```
python -m coverage run -m unittest discover tests/

```
and visualise it either in the terminal:

```
python -m coverage report
```
or html and open the htmlcov/index.html:

```
python -m coverage html

```

This will tell you which lines have been covered and if you have to write a new test or just modify a previous one. [Unittest](https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python) 


## Funding

Horizon 2020 Framework Programme (785907, HBP SGA2); Horizon 2020 Framework Programme (945539, HBP SGA3); Vetenskapsrådet (VR-M-2017-02806, VR-M-2020-01652); Swedish e-science Research Center (SeRC); KTH Digital Futures. The computations are enabled by resources provided by the Swedish National Infrastructure for Computing (SNIC) at PDC KTH partially funded by the Swedish Research Council through grant agreement no. 2018-05973. We acknowledge the use of Fenix Infrastructure resources, which are partially funded from the European Union's Horizon 2020 research and innovation programme through the ICEI project under the grant agreement No. 800858.

## Resources about Data versioning

### youtube 
https://www.youtube.com/watch?v=zimTrVwUsN0&ab_channel=FullStackDeepLearning


