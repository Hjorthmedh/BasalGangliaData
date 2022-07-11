import os
import json

"""
    
    Meta.json is the core for each model. It contains the combination of morphologies and
    parameter sets.
    

"""


def write_meta(directory, selected=False):
    """

        meta.json contains the combinations of morphologies and parameter sets and
        additional parameters for the model, like neuromodulation parameter set
        and input specification (if needed)

    :param directory: path to the model directory in BasalGangliaData
    :param selected: if there are several morphology and parameter set combinations, see examples
    :return None, writes the meta.json file for the model.
    """
    parameters = os.path.join(directory, "parameters.json")

    with open(parameters, "r") as f:
        parameter_hash = json.load(f)

    morphologies = os.path.join(directory, "morphology", "morphology_hash_filename.json")

    with open(morphologies, "r") as f:
        morphologies_hash = json.load(f)

    meta = dict()

    if selected:
        with open(os.path.join(directory, "temp", "selected_models.json"), "r") as f:
            selected = json.load(f)

        with open(os.path.join(directory, "temp", "parameters_hash_id.json"), "r") as f:
            hash_id = json.load(f)

    for p_key in parameter_hash.keys():

        meta.update({p_key: dict()})
        for m_key, m_name in morphologies_hash.items():

            if selected:

                if hash_id[p_key] in selected and m_name in selected[hash_id[p_key]]:
                    meta[p_key].update({m_key: {"morphology": m_name}})
            else:
                meta[p_key].update({m_key: {"morphology": m_name}})

    with open(os.path.join(directory, "meta.json"), "w") as f:
        json.dump(meta, f, indent=4, sort_keys=True)
