import os
import json

def select_validated_models(source,destination):

    validated_models = os.path.join(source, "val_models.json")

    with open(validated_models, "r") as f:
        validated = json.load(f)

    selected_models = dict()

    for model in validated:

        if model["par"] not in selected_models.keys():
            selected_models.update({model["par"]: [model["morph"]]})
        else:
            selected_models[model["par"]].append(model["morph"])

    with open(os.path.join(destination, "temp", "selected_models.json"), "w") as f:
        json.dump(selected_models, f)
