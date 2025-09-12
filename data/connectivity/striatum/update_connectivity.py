import json
from argparse import ArgumentParser

def update_config(original_config, new_config):

    with open(original_config, "r") as f:
        original = json.load(f)

    with open(new_config, "r") as f:
        new_data = json.load(f)

    if "connectivity" not in new_data:
        raise KeyError(f"'connectivity' tag missing in {new_config}")


    for pair, data in new_data["connectivity"].items():
        if pair not in original:
            raise KeyError(f"Connectivity between {pair} not in {original_config}, please add first")

        for type, data2 in data.items():
            print(f"Updating {pair} {type}")
            original[pair][type]["pruning"] = data2["pruning"]

    with open(f"{original_config}-updated", "wt") as f:
        json.dump(original, f, indent=4)
        

if __name__ == "__main__":
    parser = ArgumentParser("Update network config")
    parser.add_argument("main_config", help="Config file to update")
    parser.add_argument("new_config_data", help="Config file with new data")

    args = parser.parse_args()

    update_config(args.main_config, args.new_config_data)
    
