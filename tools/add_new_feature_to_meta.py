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

    hashed = make_hash_name(meta)
    hash_id = hash_identifier(hashed, length=5, prefix="updated_")

    file_path_old = pathlib.Path(dir_path) / "temp" / f"meta_{hash_id}.json"

    shutil.copy(meta_json, file_path_old)

    file_name = "meta.json"

    file_path = pathlib.Path(dir_path) / file_name

    with open(file_path, "w") as f:
        json.dump(meta, f, indent=4, sort_keys=True)