# How to transfer your model from BluePyOpt to BasalGangliaData (using Snudda format)

# BluePyOpt 

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

## Option 1: Give the path to specific files

### Required files
    Mandatory
    * parameters.json
    * mechanisms.json
    VERSION - either 1 or 2 or 2 + 3
        1. best_models.json (if you are using the direct output of the optimizer)
        2. hall_of_fame.json (if you have filtered the parameter sets against more validations)
        3. val_models.json (if you  have varied the morphology used within the original optimization and hence have more morph-parameter combinations)
        
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

# The steps

### Create your own notebook and copy-paste the code to perform each step individually or utilize the class TransferBluePyOptToSnudda. 

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

### Add tools to your path

```
import sys
sys.path.append("../tools")
source = "where the Bluepyopt optimisation, with the structure described above"
destination = "BasalGanglia/data/neurons/newnucleus/new_celltype/new_model"
```

### Transfer mechanisms

```
from transfer.mechanisms import transfer_mechanisms
transfer_mechanisms(source=source, destination=destination)
```

### Transfer parameters

```
from transfer.parameters import transfer_parameters
transfer_parameters(source=source,
                            destination=destination,
                            selected=True)
```

### Transfer selected models from val_models.json


```
from transfer.selected_models import transfer_selected_models
transfer_selected_models(source=source, destination=destination)
```

### Transfer morphologies

```
from transfer.morphology import transfer_morphologies
transfer_morphologies(source=source,
                              destination=destination,
                              selected=True)
```

### Create the meta.json which combines all information on the model

```
from meta.create_meta import write_meta
write_meta(directory=destination, selected=True)
```