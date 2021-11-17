import json
import sys
import pathlib
import copy
import hashlib
import shutil

def from_old_format(json_file, dir_path):

    parameter_list = json.load(open(json_file))
    parameter_hashed, internal_key = hashable_keys(parameter_list, return_internal=True)

    file_name = "parameters.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as model_f:
        json.dump(parameter_hashed, model_f, indent=4, sort_keys=True)

        print(f"parameters.json saved in folder : {dir_path} \n")

    if bool(internal_key):
        file_name = "parameter_id_hash_keys.json"

        file_path = pathlib.Path(dir_path) / file_name

        with open(file_path, "w") as f:
            json.dump(internal_key, f, indent=4, sort_keys=True)

def add_feature_to_meta(meta_json, additional_feature_json, dir_path):

    meta = json.load(open(meta_json))
    additional_feature = json.load(open(additional_feature_json))


    for param_hash, morpholgies in additional_feature.items():

        for m, data in morpholgies.items():

            for new_features, feature_set in data.items():

                if new_features in meta[param_hash][m].keys():
                    raise ValueError(f" Feature already exists and has value : {meta[param_hash][m][new_features]}")

                else:
                    meta[param_hash][m].update({new_features: feature_set})

    file_name_old = "meta_old.json"

    file_path_old = pathlib.Path(dir_path) / file_name_old

    shutil.copy(meta_json, file_path_old)

    file_name = "meta.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as f:
        json.dump(meta, f, indent=4, sort_keys=True)

def write_meta(parameters_json, dir_path, morphology_json=None, internal_key_json=None, val_models_json=None):
    meta = dict()

    param = json.load(open(parameters_json))

    if val_models_json:

        internal_key = json.load(open(internal_key_json))
        inverted = dict((v, k) for k, v in internal_key.items())
        temp = dict()
        val_models = json.load(open(val_models_json))
        for v in val_models:
            p_id = inverted[v["par"]]
            
            if p_id not in temp.keys():
                temp.update({p_id : [v["morph"]]})
            else:
                temp[p_id].append(v["morph"])

    
    else:
        morph = json.load(open(morphology_json))
        temp = dict.fromkeys([*param.keys()], morph)

    morphology_hash_filename = dict()

    for parameter_hash, morphology_list in temp.items():

        meta.update({parameter_hash: dict()})

        for m in morphology_list:
            a = json.dumps(m, sort_keys=True).encode("utf-8")
            hash_name = hashlib.md5(a).hexdigest()
            hash_key = "".join(["m", hash_name[:8]])
            morphology_hash_filename.update({hash_key: m})
            meta[parameter_hash].update({hash_key: {"morphology": m}})

    file_name = "meta.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as f:
        json.dump(meta, f, indent=4, sort_keys=True)

    file_name = "morphology_hash_name.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as f:
        json.dump(morphology_hash_filename, f, indent=4, sort_keys=True)


def combine_optimised_models(parameter_json, selected_parameters_json, dir_path, val_ids=None):
    """

    :parameter_json : json file which specifies parameter list used in optimization
    :best_models_json : json file which specifies the result for best models

    :rtype: object
    """
    selected_parameters_dict = json.load(open(selected_parameters_json))
    parameters_dict = json.load(open(parameter_json))

    parameter_list = list()

    if val_ids is None:
        val_ids = range(len(selected_parameters_dict))

        print(f"Number of models : {len(selected_parameters_dict)} \n")

    for i, models in enumerate(selected_parameters_dict):

        if i in val_ids:

            temporary_dict = copy.deepcopy(parameters_dict)

            for model_parameters in models.items():

                for params in temporary_dict:

                    if model_parameters[0].split(".")[0] == params["param_name"]:

                        if model_parameters[0].split(".")[1] == params["sectionlist"]:
                            params.pop("bounds", None)

                            params.update({"value": model_parameters[1]})

            parameter_list.append(temporary_dict)

    parameter_hashed, internal_key = hashable_keys(parameter_list, return_internal=True)

    file_name = "parameters.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as model_f:

        json.dump(parameter_hashed, model_f, indent=4, sort_keys=True)

        print(f"parameters.json saved in folder : {dir_path} \n")

    if bool(internal_key):
        file_name = "parameter_id_hash_keys.json"

        file_path = pathlib.Path(dir_path) / file_name

        with open(file_path, "w") as f:
            json.dump(internal_key, f, indent=4, sort_keys=True)


def hashable_keys(parameter_list, return_internal=False):
    output_dictionary = dict()
    internal_key = dict()
    for i, data_instances in enumerate(parameter_list):
        a = json.dumps(data_instances, sort_keys=True).encode("utf-8")
        hash_name = hashlib.md5(a).hexdigest()
        hash_key = "".join(["p", hash_name[:8]])

        output_dictionary.update({hash_key: data_instances})
        internal_key.update({hash_key: i})

    if return_internal:
        return output_dictionary, internal_key

    else:
        return output_dictionary
