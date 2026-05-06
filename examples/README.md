# Example on how to transfer models from BPO to snudda
The easiest way to transfer models is to use the script:  
**simple_transfer.py** 

The transfer script will look for and use either val_models.json, hall_of_fame.json or best_models.json with that priority.

**v2 / THIN format is handled automatically.** If `config/parameters.json` is in the newer nested-dict format (v2), it is converted to the expected list format (v1) before transfer. Similarly, if the models file is a THIN-format dict with a `"models"` key, the list is extracted and section names are normalised (`axon`→`axonal`, `soma`→`somatic`) automatically. No extra flags are needed — the script detects the format and converts on the fly.

If simple_transfer.py fails, use the below basic options at the bottom of the notebook.

run commands in terminal or use the code below

### Examples
Transfer one model from *source* (-s) and store in *destination* (-d):  

>python simple_transfer.py **-s** example_models/str-fs-model1/
>                          **-d** Transfered_models/fs/str-fs-model1/

To transfer all the models in a directory, use the below command:  

>python simple_transfer.py **-s** example_models/ **-d** Transfered_models/  **-a**

which will try to transfer all the example models and sort them into respective celltype directory (i.g. dspn and fs).  
The sorting assumes that the model name is of the format /region-type-additional_info/, e.g. str-dspn-...  
If this is not the case, the model will be skipped (see output for example_models/fs/model1).  

Models that already exist in the output folder will also be skipped (as is the case below for the model transfered as a single model).

In order to se all the options, run below command in a terminal:  

>python simple_transfer.py -h

The transfer is an automated version of the 3 options described below.

Example scripts of actual transfers can be found in the **example_transfers** folder.

The models can be vierified used using the functions in **verify_models.py** 

## Verify transfer by simulation
Below simulations will only work if the original model has hoc versions of the models stored in a subfolder named checkpoints.  

Use command:

> python verify_model.py -p example_models/str-dspn-model2/ -o Transfered_models/dspn/str-dspn-model2/ 

where  
-p is path to the reference model (BPO)  
-o is the flag for the output model (transfered)  

for all options use:

> python verify_model.py -h

Here direct comparison of simulations in the two setups is used to verify the transfer. Another way to verify models would be to compare the output of  

>for sec in h.allsec():  
>>    h.psection(sec=sec)  

if the output of this command is identical for transfered and reference models, and the mechanisms are identical -> the models are idential


## Below follows a detailed description of the underlying functions that simple_transfer are using

## BluePyOpt 

To create single multi-compartmental models, the lab utilizes [BluePyOpt](https://github.com/BlueBrain/BluePyOpt). The optimization is started using a collection of code* with the "set up" of the 
optimization is done with the following code:

```
    optimiser = bpopt.optimisations.DEAPOptimisation(
        evaluator=evaluator,
        offspring_size=offspring_size,
        map_function=lview.map_sync,
        seed=1)
    pop, hof, log, hist = optimiser.run(max_ngen=ngenerations)
```

see the method "run" in BluePyOpt [here](https://github.com/BlueBrain/BluePyOpt/blob/dfd202904c4f497c54574c7f321a95bb5183438b/bluepyopt/deapext/optimisations.py#L253)

The "pop","hof","log" and "hist" are returned from "run". The "hof" contains the "best" parameter sets of the optimization. The "hof" is saved into a json-file by the following code:

```
    import json
    best_models = []
    for record in hof:
        params = evaluator.param_dict(record)
        best_models.append(params)

    with open('best_models.json', 'w') as fp:
        json.dump(best_models, fp, indent=4)
    
```
The file can be further filtered by different validation scripts* but the structure should be the same as in 'best_models.json' (a list of dictionaries). See examples/ for examples of each file required in the conversion from BluePyOpt to Snudda.

Some people in the lab use 'best_models.json', but further validation following the optimization should filter this list and these models are saved in 'hall_of_fame.json'. This file has the same structure but might contain fewer models, as other features are measured during validation compared to optimization.

If the optimization is also tested on several different morphologies, a third file called 'val_models.json' is required (See examples/ for an example of 'val_model.json').


*for more information on the optimization contact Alex Kozlov or Ilaria Carannante. 

### Option 1: Give the path to specific files

#### Required files
    Mandatory
    * parameters.json  (v1 list format or v2 nested-dict format — both accepted)
    * mechanisms.json  (not required when using v2 parameters — generated automatically)
    VERSION - either 1 or 2 or 2 + 3
        1. best_models.json (if you are using the direct output of the optimizer)
        2. hall_of_fame.json (if you have filtered the parameter sets against more validations)
        3. val_models.json (if you have varied the morphology used within the original optimization and hence have more morph-parameter combinations)
        
The model optimisation could be a folder, containing the follow files and subdirectories:

    model/
        config/
                parameters.json
                mechanisms.json
        morphology/
                contain one or several morphologies (.swc)
                used for the model
        hall_of_fame.json ( contain the parameter sets - the results of the optimisation)
        val_models.json ( optional file, if several morphologies are used, the parameter sets which match each morphology)
        
For an example of the structure and contents of the files, see **BasalGangliaData/tests/test_data/example_variation_source**

*Contact Alex Kozlov for more information   

## The steps

#### Create your own notebook and copy-paste the code to perform each step individually or utilize the class TransferBluePyOptToSnudda. 

The transfer has been divided into several steps.

Create directory for the model.
```
    Within BasalGangliaData, the models used in Snudda are saved under
    BasalGangliaData/data/neurons/name_of_nucleus

    **If the nucleus does not exist, add a folder for the new nucleus**

    Next create (if it does not already exist), a folder for each cell type within the nucleus

    Lastly, create the folder for each model of the cell type 
    (this folder will be the **destination** used in the code below)

     For example,

     BasalGanglia/data/neurons/newnucleus/new_celltype/new_model
```        

#### Add tools to your path

```
import sys
sys.path.append("../tools")
source = "where the Bluepyopt optimisation, with the structure described above"
destination = "BasalGanglia/data/neurons/newnucleus/new_celltype/new_model"
```

#### Transfer mechanisms

```
from transfer.mechanisms import transfer_mechanisms
transfer_mechanisms(source=source, destination=destination)
```

#### Transfer parameters

```
from transfer.parameters import transfer_parameters
transfer_parameters(source=source,
                            destination=destination,
                            selected=True)
```

#### Transfer selected models from val_models.json


```
from transfer.selected_models import transfer_selected_models
transfer_selected_models(source=source, destination=destination)
```

#### Transfer morphologies

```
from transfer.morphology import transfer_morphologies
transfer_morphologies(source=source,
                              destination=destination,
                              selected=True)
```

#### Create the meta.json which combines all information on the model

```
from meta.create_meta import write_meta
write_meta(directory=destination, selected=True)
```
