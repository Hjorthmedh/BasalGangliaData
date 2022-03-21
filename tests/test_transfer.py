import os
import shutil
import sys

# Dirty fix, :TODO rewrite tools as a package - joined directly to Snudda or the lab
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "tools")))

import unittest
from transfer.morphology import transfer_morphologies
from transfer.selected_models import transfer_selected_models
from transfer.parameters import transfer_parameters
from transfer.mechanisms import transfer_mechanisms

"""
    Testing the functionality of transferring files from BluePyOpt format
    to Snudda format within the BasalGangliaData
    
"""


class TestSum(unittest.TestCase):

    def test_transfer_mechanisms(self):

        test_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))

        source = os.path.join(test_root, "example_variation_source")

        destination = os.path.join(test_root, "example_variation_destination")

        transfer_mechanisms(source=source, destination=destination)

        self.assertTrue(os.path.exists(os.path.join(destination, "mechanisms.json")))

    def test_transfer_parameters(self):

        test_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))

        source = os.path.join(test_root, "example_variation_source")

        destination = os.path.join(test_root, "example_variation_destination")

        transfer_parameters(source=source,
                            destination=destination,
                            selected=True)

        self.assertTrue(os.path.exists(os.path.join(destination, "parameters.json")))

    def test_transfer_morphologies(self):
        test_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))

        source = os.path.join(test_root, "example_variation_source")

        destination = os.path.join(test_root, "example_variation_destination")

        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.mkdir(destination)

        self.assertRaises(FileNotFoundError,
                          transfer_morphologies,
                          source=source,
                          destination=destination,
                          selected=True)

        os.mkdir(os.path.join(destination, "temp"))

        transfer_selected_models(source=source, destination=destination)

        transfer_morphologies(source=source,
                              destination=destination,
                              selected=True)

        self.assertTrue(os.path.exists(os.path.join(destination, "morphology", "morphology_hash_filename.json")))
        self.assertTrue(os.path.exists(os.path.join(destination, "temp", "selected_models.json")))

    def test_transfer_selected_models(self):

        test_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))

        source = os.path.join(test_root, "example_variation_source")

        destination = os.path.join(test_root, "example_variation_destination")

        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.mkdir(destination)

        self.assertRaises(NotADirectoryError,
                          transfer_selected_models,
                          source=source,
                          destination=destination)

        os.mkdir(os.path.join(destination, "temp"))

        transfer_selected_models(source=source, destination=destination)

        self.assertTrue(os.path.exists(os.path.join(destination, "temp", "selected_models.json")))


if __name__ == '__main__':
    unittest.main()
