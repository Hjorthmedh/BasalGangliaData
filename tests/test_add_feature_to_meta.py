import os
import sys
# Dirty fix, :TODO rewrite tools as a package - joined directly to Snudda or the lab
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "tools")))
import unittest
import json
import shutil
from meta.create_meta import write_meta
from transfer.morphology import transfer_morphologies
from transfer.selected_models import transfer_selected_models
from transfer.parameters import transfer_parameters
from transfer.mechanisms import transfer_mechanisms
from modify.add_feature import add_feature_to_meta


class TestCreate(unittest.TestCase):

    def test_add_feature_to_meta(self):
        test_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))

        source = os.path.join(test_root, "example_variation_source")

        destination = os.path.join(test_root, "example_variation_destination")
        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.mkdir(destination)
        os.mkdir(os.path.join(destination, "temp"))

        transfer_mechanisms(source=source, destination=destination)

        transfer_parameters(source=source,
                            destination=destination,
                            selected=True)

        transfer_selected_models(source=source, destination=destination)

        transfer_morphologies(source=source,
                              destination=destination,
                              selected=True)

        write_meta(directory=destination, selected=True)

        add_dict = dict()
        feature = ["fake"]

        copy_this_structure = os.path.join(destination, "meta.json")

        with open(copy_this_structure, "r") as f:
            d = json.load(f)
        for p in d:
            add_dict[p] = dict()
            for m in d[p]:
                add_dict[p].update({m: {"fake_feature": feature}})

        add_json = os.path.join(os.path.dirname(__file__), "test_data", "example_additional", "add.json")
        with open(add_json, "w") as f:
            json.dump(add_dict, f)

        add_feature_to_meta(directory=destination, additional_feature_json=add_json)

        with open(os.path.join(destination, "meta.json")) as f:
            d = json.load(f)

        for p in d:
            for m in d[p]:
                assert "fake_feature" in d[p][m].keys()
                assert "morphology" in d[p][m].keys()
                assert len(d[p][m].keys()) == 2
if __name__ == '__main__':
    unittest.main()
