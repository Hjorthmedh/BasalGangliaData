import os
import json

"""

    To transfer val_models.json from BluePyOpt to Snudda format 
    
"""


def transfer_selected_models(source, destination):

    """

    :param source: path to the model directory (BluePyOpt output), see examples for how
                    this directory should be structured
    :param destination: path to BasalGanglia/data/your_brain_area/neuron_type/model_name
    :return:
    """
    validated_models = os.path.join(source, "val_models.json")

    with open(validated_models, "r") as f:
        validated = json.load(f)

    selected_models = dict()

    for model in validated:

        if model["par"] not in selected_models.keys():
            selected_models.update({model["par"]: [model["morph"]]})
        else:
            selected_models[model["par"]].append(model["morph"])

    temp_dir = os.path.join(destination, "temp")
    if os.path.exists(temp_dir):
        with open(os.path.join(temp_dir, "selected_models.json"), "w") as f:
            json.dump(selected_models, f)

        print(f"Transfer of the selected combinations of parameters and morphologies \n"
              f" \n"
              f"from : {source} \n"
              f"to : {temp_dir} \n")

    else:
        raise NotADirectoryError(f" The directory {temp_dir} does not exists \n "
                                 f" Create it to continue with the transfer")
