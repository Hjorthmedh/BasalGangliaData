import os
import glob
from .make_hash import *
import shutil


def make_morphology_hash_key_dict(morphology_total):
    hash_name_dict = dict()

    for m in morphology_total:
        m_name = m.split("/")[-1]

        with open(m, "r") as k:
            whole = k.read()

        hash_name = make_hash_name(whole)

        hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="m")

        hash_name_dict.update({hash_id: m_name})

    return hash_name_dict


def transfer_morphologies(source, destination, selected=False):
    morphology_directory = os.path.join(source, "morphology")

    morphology_destination = os.path.join(destination, "morphology")

    if os.path.exists(morphology_directory):
        pass
    else:
        print(f"All morphologies should be placed in a directory called 'morphology' \n"
              f" i.e the complete path would be {os.path.abspath(os.path.join(source, 'morphology'))} ")

    if selected:
        with open(os.path.join(destination, "temp", "selected_models.json"), "r") as f:
            selected = json.load(f)
        morphology_total = list()

        for mvs in selected.values():
            for m in mvs:
                if m not in morphology_total:
                    morphology_total.append(os.path.join(morphology_directory, m))

    else:
        morphology_total = glob.glob(os.path.join(morphology_directory, "*.swc"))

    hash_name_dict = make_morphology_hash_key_dict(morphology_total)

    if os.path.exists(morphology_destination):
        print(f"{morphology_destination} already exists cannot copy the files from {source}")
    else:
        shutil.copytree(morphology_directory, morphology_destination)

    with open(os.path.join(morphology_destination, "morphology_hash_filename.json"), "w") as f:
        json.dump(hash_name_dict, f, indent=4, sort_keys=True)

