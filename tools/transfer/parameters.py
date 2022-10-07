import shutil
import os
import json
import sys
import pathlib
import copy
import hashlib
import collections
from hash_value.make_hash import *
from hash_value.parameters import *


def save_parameter_set(parameter_set, destination):

    """

    :param parameter_set:
    :param destination:
    :return:
    """
    if os.path.exists(os.path.join(destination, "parameters.json")):
        raise FileExistsError(f" File already exists in {destination}")
    else:
        with open(os.path.join(destination, "parameters.json"), "w") as f:
            json.dump(parameter_set, f, sort_keys=True, indent=4)


def combine_hall_of_fame_parameters(parameters_list, hall_of_fame):

    """

    :param parameters_list:
    :param hall_of_fame:
    :return:
    """
    combined_parameters_dict = dict()

    for i, models in enumerate(hall_of_fame):

        temporary_dict = copy.deepcopy(parameters_list)
        combined_parameters_dict.update({i: temporary_dict})

        for model_parameters in models.items():

            for params in combined_parameters_dict[i]:

                if model_parameters[0].split(".")[0] == params["param_name"]:

                    if model_parameters[0].split(".")[1] == params["sectionlist"]:
                        params.pop("bounds", None)

                        params.update({"value": model_parameters[1]})

    ordered = json.loads(json.dumps(combined_parameters_dict, indent=4, sort_keys=True))

    return ordered


def test_parameter_file(destination):

    """
    
    :param destination:
    :return:
    """
    return_value = True

    with open(os.path.join(destination, "temp", "parameters_temp.json")) as f:
        temp_para = json.load(f)

    for p_key, parameter_list in temp_para.items():

        hash_value = make_hash_name(parameter_list)

        hash_id = hash_identifier(hash_value=hash_value, length=8, prefix="p")

        if p_key == hash_id:
            pass
        else:
            raise ValueError(f" Hash was not the same as created")
            return_value = False

    return return_value


def combine_hall_of_fame_with_optimisation_parameters(source, destination, selected=False):
    """

    :param source: path to the model directory (BluePyOpt output), see examples for how
                    this directory should be structured
    :param destination: path to BasalGanglia/data/your_brain_area/neuron_type/model_name
    :param selected: for the case where several morphologies are available for the specific
           model, an additional file is needed, which contains the accepted parameter
           and morphology combinations. See examples/ on how this file should be
           structured.
    :return:
    """
    temp_dir = os.path.join(destination, "temp")

    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    if os.path.exists(os.path.join(source, "config")):
        hall_of_fame = os.path.join(source, "hall_of_fame.json")
        parameters = os.path.join(source, "config", "parameters.json")

        with open(parameters, "r") as f:
            parameter_set = json.load(f)

        with open(hall_of_fame, "r") as f:
            hall_of_fame_sets = json.load(f)

    else:
        raise NotADirectoryError(f" Directory : \n"
                                 f" {os.path.join(source, 'config')} does not exist. \n"
                                 f" See examples for a description of the BluePyOpt folder structure \n"
                                 f" we utilize. ")

    if selected and os.path.exists(os.path.join(destination, "temp", "selected_models.json")):
        with open(os.path.join(destination, "temp", "selected_models.json"), "r") as f:
            selected = json.load(f)

        # Filter the parameter sets which were parameter ids were finally selected
        hall_of_fame_sets = [hall_of_fame_sets[int(k)] for k in selected.keys()]

    '''
    Combination of parameter set and hall of fame parameters
    '''

    combined_parameters = combine_hall_of_fame_parameters(parameter_set, hall_of_fame_sets)

    save_parameter_set(parameter_set=combined_parameters,
                       destination=temp_dir)

    hashed_parameter_dict, translation = make_parameter_dict_hash_name(combined_parameters)

    with open(os.path.join(destination, "temp", "parameters_temp.json"), "w") as f:
        json.dump(hashed_parameter_dict, f, sort_keys=True, indent=4)

    if test_parameter_file(destination=destination):
        save_parameter_set(parameter_set=hashed_parameter_dict,
                           destination=destination)
        with open(os.path.join(destination, "temp", "parameters_hash_id.json"), "w") as f:
            json.dump(translation, f, sort_keys=True, indent=4)

    else:
        raise ValueError("parameters.json is wrong not passing")


def transfer_parameters(source, destination, selected):

    """

    Transitioning version for parameter transfer, this will replace the previous version
    i.e. combine_hall_of_fame_with_optimisation_parameters

    :param source:
    :param destination:
    :param selected:
    :return:
    """
    combine_hall_of_fame_with_optimisation_parameters(source=source,
                                                      destination=destination,
                                                      selected=selected)
