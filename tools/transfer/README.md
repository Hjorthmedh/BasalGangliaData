# Transferring files following Bluepyopt optimisation



Within this folder are the functions used to transfer **BluePyOpt format
to Snudda format**

<p><small> Questions or Corrections? Email johanna.frost.nylen@ki.se </small></p>


#### Interested in knowing more about BluePyOpt and Snudda format, continue reading below......


In BluePyOpt, there is a certain number of output files which contain
the parameters of the neuron models.
Following the optimisation, hall_of_fame.json contain the models which 
are the "best models" and these are complemented with parameters.json 
and mechanisms.json. 

Within, parameters.json are either the values or ranges (i.e. the optimisation
interval) for each parameter. Hence, parameters.json informs us about
which parameters are either fixed or optimised within the model.

Within mechanisms.json are the ion channels and other density mechanisms which 
are distributed onto the morphology (to clarify, the morphology is defined as
either soma, basal (dendritic), apical (cortex specific dendrite) or axon).

Lastly, each model has a morphology (which could be the same cell from which
the experimental data was collected) in the format of a swc-file.

In summary, the files are:

* hall_of_fame.json
* parameters.json
* mechanisms.json
* morphology files (SWC)

### Moving from BluePyOpt to Snudda format

In Snudda, a model is described by:

* mechanisms.json
* parameters.json
* morphology/morphologies
* (also modulation.json)

and **meta.json**.

Morphologies and mechanisms.json have the same structure as in BluePyOpt format.

Parameters.json is different. Within Snudda, parameters.json is a dictionary,
where the keys are hash keys and the values are parameter sets. 
The hash key is calculated from the contents of the parameter set. The calculation
uses Message-Digest algorithm 5 or **MD5** (see make_hash.py) to produce
a hash value. 

Modulation.json has the same structure as parameters.json, but the parameter
sets only involve parameters for neuromodulation.

Hash keys are also calculated for the morphologies based on the contents of the
swc-files.

## Meta.json 
The **meta.json** is a file which contains all the parameter set and morphology type
combinations for the model. There are two different reasons this could occur:

* The model has one morphology and 10 passing parameter sets within hall_of_fame.json.
  The meta.json would have 10 parameter hash_keys with a single morphology hash_key within.

* Another scenario is several morphologies for the hall_of_fame.json. The meta.json
  would then contain 10 parameter hash keys with several morphology hash keys
  within. 

In the parameter and morphology hash key pair, specific parameters for input,
neuromodulation are defined. Hence, the model simulated is defined by
parameter and morphology hash key pair. 

#### Why hash keys?

Simple reason, they are calculated from the data directly. If something changes in
the data, the hash key will change.

Setting up simple tests to check that the hash keys are correct will
assure you that your models have not changed.

Also, Snudda saves which parameter and morphology hash key is used for each
neuron instance within the network. If your models have changed and you try to 
simulate an old version of the network, Snudda will complain! 


## Example usage:

```
python simple_transfer.py -s source_data -d destination_folder -a
```


