import shutil
import os
import json
import sys
import pathlib
import copy
import hashlib
import collections
from make_hash import *

def make_parameter_dict_hash_name(parameter_dict):
    translation = dict()
    hashed_parameter_dict = dict()
    print(parameter_dict.keys())
    for p_id, parameter_list in parameter_dict.items():
        hash_name = make_hash_name(parameter_list)

        hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="p")
        hashed_parameter_dict.update({hash_id: parameter_list})
        translation.update({hash_id: p_id})

    if len(parameter_dict) != len(translation):
        raise ValueError(
            f"All parameter sets are not individual - there is replication as there are {len(parameter_dict)} parameter sets"
            f"while only {len(translation)} unique hash_keys")

    return hashed_parameter_dict, translation


def combine_hall_of_fame_parameters(parameters_list, hall_of_fame):
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
    return_value = True

    with open(os.path.join(destination, "temp", "parameters_temp.json")) as f:
        temp_para = json.load(f)

    for p_key, parameter_list in temp_para.items():

        hash_name = make_hash_name(parameter_list)

        hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="p")

        if p_key == hash_id:
            pass
        else:
            raise ValueError(f" Hash was not the same as created")
            return_value = False

    return return_value


def combine_hall_of_fame_with_optimisation_parameters(source, destination, selected=False):
    hall_of_fame = os.path.join(source, "hall_of_fame.json")

    parameters = os.path.join(source, "config", "parameters.json")

    with open(hall_of_fame, "r") as f:
        hall = json.load(f)
        
    if os.path.exists(parameters):
        with open(parameters, 'r+') as f:
            content = f.read()
            f.seek(0)
            content=content.replace('math.exp', 'exp')#This way it can be run multiple time wihtout creating math.math.exp
            content=content.replace('exp', 'math.exp')#In long term, change "from math import *" in Alex code to "import math"
            f.write(content)
        with open(parameters, "r") as f:
            para = json.load(f)
    else:
        print(f"parameters.json for the bluepyopt optimisation should be in a subdir called config, i.e \n"
              f"create {os.path.abspath(os.path.join(source, 'config'))} ")

    temp_dir = os.path.join(destination, "temp")

    if os.path.exists(temp_dir):
        pass
    else:
        print(f"a temporary directory for intermediate files does not exist in {destination}, \n"
              f"create a 'temp' directory i.e. {os.path.abspath(os.path.join(destination, 'temp'))}")

    if selected:
        with open(os.path.join(destination, "temp", "selected_models.json"), "r") as f:
            selected = json.load(f)
        hall = [hall[int(k)] for k in selected.keys()]

    combined_parameters = combine_hall_of_fame_parameters(para, hall)

    hashed_parameter_dict, translation = make_parameter_dict_hash_name(combined_parameters)
    if not os.path.isdir(os.path.join(destination, "temp")):
        os.mkdir(os.path.join(destination, "temp"))
    with open(os.path.join(destination, "temp", "parameters_temp.json"), "w") as f:
        json.dump(hashed_parameter_dict, f, sort_keys=True, indent=4)

    if test_parameter_file(destination=destination):
        shutil.copy(os.path.join(destination, "temp", "parameters_temp.json"),
                    os.path.join(destination, "parameters.json"))
        with open(os.path.join(destination, "temp", "parameters_hash_id.json"), "w") as f:
            json.dump(translation, f, sort_keys=True, indent=4)
    else:
        raise ValueError("parameters.json is wrong not passing")

