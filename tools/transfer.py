import shutil
from distutils.dir_util import copy_tree
import os
import json
import sys
import pathlib
import copy
import hashlib
import collections


def hash_identifier(hash_name, length, prefix):
    hash_key = "".join([prefix, hash_name[:length]])

    return hash_key


def hashable_keys(parameter_list, return_internal=False):
    output_dictionary = dict()
    internal_key = dict()

    for i, data_instances in enumerate(parameter_list):
        hash_name = make_hash_name(data=data_instances)
        hash_key = hash_identifier(hash_name=hash_name, length=8, prefix="p")

        output_dictionary.update({hash_key: data_instances})
        internal_key.update({hash_key: i})

    if return_internal:
        return output_dictionary, internal_key

    else:
        return output_dictionary


def make_hash_name(data):
    a = json.dumps(data, sort_keys=True).encode("utf-8")
    hash_name = hashlib.md5(a).hexdigest()

    return hash_name


def change_parameter_format_to_hash_key(json_file, dir_path):
    with open(json_file, "r") as f:
        parameter_list = json.load(f)

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

    """

    :param meta_json: meta file, structure with dictionary with two levels, firstly parameter keys and secondly
                        morphology keys
    :param additional_feature_json: structure, two level dictionary as meta with third level being the specific
                        which is to be added to the meta json block.
    :param dir_path: directory of where the new meta json, and the old will be saved.
    :return:
    """


    with open(meta_json, "r") as f:
        meta = json.load(f)

    with open(additional_feature_json, "r") as f:
        additional_feature = json.load(f)

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
                temp.update({p_id: [v["morph"]]})
            else:
                temp[p_id].append(v["morph"])


    else:
        morph = json.load(open(morphology_json))
        temp = dict.fromkeys([*param.keys()], morph)

    morphology_hash_filename = dict()

    for parameter_hash, morphology_list in temp.items():

        meta.update({parameter_hash: dict()})

        for m in morphology_list:
            with open(m) as f:
                m_read = f.read()
            a = json.dumps(m_read, sort_keys=True).encode("utf-8")
            hash_name = hashlib.md5(a).hexdigest()
            hash_key = "".join(["m", hash_name[:8]])
            morphology_hash_filename.update({hash_key: m})
            meta[parameter_hash].update({hash_key: {"morphology": m}})

    new_param = dict()

    for params in meta.keys():
        new_param.update({params: param[params]})

    file_name = "parameters.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as f:
        json.dump(new_param, f, indent=4, sort_keys=True)

    shutil.copy(pathlib.Path(dir_path) / "parameters.json", os.path.join(dir_path, "parameters_old.json"))

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


def for_models_from_previous_old_format(dir_path, out_put_dir):
    if not os.path.exists(out_put_dir):
        os.makedirs(out_put_dir)

    import glob
    morphology_file = glob.glob(os.path.join(dir_path, "*.swc"))[0]
    morphology_dir_output = os.path.join(out_put_dir, "morphology/")

    if not os.path.exists(morphology_dir_output):
        os.makedirs(morphology_dir_output)

    name_m = morphology_file.split("/")[-1]
    shutil.copy(morphology_file, os.path.join(morphology_dir_output, name_m))

    with open(os.path.join(morphology_dir_output, "morphology.json"), "w") as f:
        json.dump([name_m], f)

    mechanism_json = os.path.join(dir_path, "mechanisms.json")
    mechanism_json_new = os.path.join(out_put_dir, "mechanisms.json")
    shutil.copy(mechanism_json, mechanism_json_new)

    from_old_format(os.path.join(dir_path, "parameters.json"), out_put_dir)

    write_meta(parameters_json=os.path.join(out_put_dir, "parameters.json"), dir_path=out_put_dir,
               internal_key_json=os.path.join(out_put_dir, "parameter_id_hash_keys.json"),
               morphology_json=os.path.join(out_put_dir, "morphology", "morphology.json"))


def for_models_with_variation_in_morphology(dir_path, out_put_dir):
    if not os.path.exists(out_put_dir):
        os.makedirs(out_put_dir)

    # copy morphology folder

    morphology_dir = os.path.join(dir_path, "morphology/")
    morphology_dir_output = os.path.join(out_put_dir, "morphology/")

    copy_tree(morphology_dir, morphology_dir_output)

    # copy mechanism file

    mechanism_json = os.path.join(dir_path, "config", "mechanisms.json")
    mechanism_json_new = os.path.join(out_put_dir, "mechanisms.json")

    shutil.copy(mechanism_json, mechanism_json_new)

    # create parameter.json
    hall_of_fame = os.path.join(dir_path, "hall_of_fame.json")
    parameters = os.path.join(dir_path, "config", "parameters.json")

    combine_optimised_models(parameters, hall_of_fame, out_put_dir)

    # Write meta data
    final_parameter = os.path.join(out_put_dir, "parameters.json")
    internal = os.path.join(out_put_dir, "parameter_id_hash_keys.json")
    val_models = os.path.join(dir_path, "val_models.json")

    write_meta(parameters_json=final_parameter, dir_path=out_put_dir, internal_key_json=internal,
               val_models_json=val_models)
