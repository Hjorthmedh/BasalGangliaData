import os
import json
import shutil
import glob
from hash_value.morphology import make_morphology_hash_key_dict

'''

    Code for transferring morphology files from BluePyOpt output to BasalGangliaData 
    and Snudda format
'''


def transfer_morphologies(source=None, destination=None, selected=False, direct_path_morph=None):

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

    if direct_path_morph:
        morphology_directory = os.path.join(direct_path_morph)
    else:
        morphology_directory = os.path.join(source, "morphology")

    morphology_destination = os.path.join(destination, "morphology")

    if os.path.exists(morphology_directory):
        pass
    else:
        print(f"All morphologies should be placed in a directory called 'morphology' \n"
              f" i.e the complete path would be {os.path.abspath(os.path.join(source, 'morphology'))} ")

    if selected and os.path.exists(os.path.join(destination, "temp", "selected_models.json")):
        with open(os.path.join(destination, "temp", "selected_models.json"), "r") as f:
            selected = json.load(f)
        morphology_total = list()

        for mvs in selected.values():
            for m in mvs:
                if m not in morphology_total:
                    morphology_total.append(os.path.join(morphology_directory, m))
    elif selected:
        raise FileNotFoundError("Prior to moving the morphologies, you have to create the 'selected_models.json' \n"
                                "via tools.transfer.selected_models.select_validated_models ")

    else:
        morphology_total = glob.glob(os.path.join(morphology_directory, "*.swc"))

    hash_name_dict = make_morphology_hash_key_dict(morphology_total)

    if os.path.exists(morphology_destination):
        print(f"{morphology_destination} already exists cannot copy the files from {source}")
    else:
        shutil.copytree(morphology_directory, morphology_destination)

        with open(os.path.join(morphology_destination, "morphology_hash_filename.json"), "w") as f:
            json.dump(hash_name_dict, f, indent=4, sort_keys=True)

        print(f"Morphology file transfer complete \n"
              f" \n"
              f"from : {source} \n"
              f"to : {destination} \n")


