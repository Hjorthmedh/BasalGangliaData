import os
import shutil
import numpy as np
import json
import copy
from tools.hash_value.make_hash import *
"""

    Meta.json is the core of each model within Snudda. 
    
    See README.md for an example.
    
    
"""

def add_feature_to_meta(directory, additional_feature_json):
    """

    :param directory: the model directory
    :param additional_feature_json: structure, two level dictionary as meta with third level being the specific
                        which is to be added to the meta json block.
    :return:
    """
    meta_json = os.path.join(directory, "meta.json")

    with open(meta_json, "r") as f:
        meta = json.load(f)

    with open(additional_feature_json, "r") as f:
        additional_feature = json.load(f)

    for param_hash, morph_hashes in additional_feature.items():

        for m, data in morph_hashes.items():

            for new_features, feature_set in data.items():

                if new_features in meta[param_hash][m].keys():
                    raise ValueError(f" Feature already exists and has value : {meta[param_hash][m][new_features]}")

                else:
                    meta[param_hash][m].update({new_features: feature_set})

    hashed = make_hash_name(meta)
    hash_id = hash_identifier(hashed, length=5, prefix="updated_")

    file_path_old = os.path.join(directory, "temp", f"meta_{hash_id}.json")

    shutil.copy(meta_json, file_path_old)

    file_path = os.path.join(directory, "meta.json")

    with open(file_path, "w") as f:
        json.dump(meta, f, indent=4, sort_keys=True)

