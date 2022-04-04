import os
import sys
# Dirty fix, :TODO rewrite tools as a package - joined directly to Snudda or the lab
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "tools")))
import unittest
from hash_value.make_hash import *
import json
import glob
import collections




class TestSynapses(unittest.TestCase):


    def test_synapses(self):

        """
            Testing the synapse parameters

        """

        root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        synapse_dir = os.path.join(root, "data", "synapses", "striatum")

        correct_hashes = os.path.join(synapse_dir, "temp", "synapse_hash_key.json")

        with open(correct_hashes, "r") as f:
            correct_hash_dict = json.load(f)

        for f in glob.glob(os.path.join(synapse_dir, "*.json")):

            with open(f, "r") as sf:
                d = json.load(sf)

            hash_value = make_hash_name(d)

            hash_key = hash_identifier(hash_value=hash_value, length=8, prefix="syn")

            basename = os.path.basename(f)

            assert hash_key == correct_hash_dict[basename]



