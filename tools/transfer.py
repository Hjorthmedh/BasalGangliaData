import shutil
from distutils.dir_util import copy_tree
from post_optimisation import combine_optimised_models, write_meta, from_old_format
import os
import json


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
