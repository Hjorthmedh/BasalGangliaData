import unittest
from make_hash import *
import os
import json
import glob
import collections


class TestSum(unittest.TestCase):

    def test_meta_hash_name(self):

        model_dir = os.path.join("..", "data", "neurons", "striatum")

        for neuron_dir in glob.glob(os.path.join(model_dir, "*/*")):
            neuron_type = neuron_dir.split("/")[-2]
            model_name = neuron_dir.split("/")[-1]
            hash_meta = os.path.join(neuron_dir, "meta.json")

            with open(hash_meta, "r") as f:
                meta_hashed = json.load(f)

            hash_parameters = os.path.join(neuron_dir, "parameters.json")

            with open(hash_parameters, "r") as f:
                parameters_hashed = json.load(f)

            hash_morphology = os.path.join(neuron_dir, "morphology", "morph_key_hash_name.json")

            with open(hash_morphology, "r") as f:
                morphology_hashed = json.load(f)

            hash_neuromodulation = os.path.join(neuron_dir, "modulation.json")

            with open(hash_neuromodulation, "r") as f:
                neuromodulation_hashed = json.load(f)

            with open(hash_meta, "r") as f:
                meta_hashed = json.load(f)

            for hash_p, variations in meta_hashed.items():

                self.assertTrue((hash_p in parameters_hashed.keys()), msg=f"The parameter hash {hash_p} is not in "
                                                                          f"neuron type {neuron_type} and "
                                                                          f"model {model_name} meta.json")

                for hash_m, specific_combo in variations.items():

                    self.assertTrue((hash_m in morphology_hashed.keys()))
                    self.assertEqual(morphology_hashed[hash_m], specific_combo["morphology"])

                    if "neuromodulation" in specific_combo.keys():

                        for nm in specific_combo["neuromodulation"]:
                            self.assertTrue((nm in neuromodulation_hashed.keys()))

    def test_neuromodulation_hash_name(self):

        model_dir = os.path.join("..", "data", "neurons", "striatum")

        for neuron_dir in glob.glob(os.path.join(model_dir, "*/*")):

            neuron_type = neuron_dir.split("/")[-2]
            model_name = neuron_dir.split("/")[-1]
            hash_neuromodulation = os.path.join(neuron_dir, "modulation.json")

            with open(hash_neuromodulation, "r") as f:
                neuromodulation_hashed = json.load(f)

            for hash_key, neuromodulation_list in neuromodulation_hashed.items():
                hash_name = make_hash_name(neuromodulation_list)

                hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="nm")

                self.assertEqual(hash_id, hash_key, msg=f"Hash keys are not correct, check neuron type {neuron_type} "
                                                        f"and model {model_name} for updated neuromodulation sets")

    def test_parameter_hash_name(self):

        model_dir = os.path.join("..", "data", "neurons", "striatum")

        for neuron_dir in glob.glob(os.path.join(model_dir, "*/*")):

            neuron_type = neuron_dir.split("/")[-2]
            model_name = neuron_dir.split("/")[-1]
            hash_parameters = os.path.join(neuron_dir, "parameters.json")

            with open(hash_parameters, "r") as f:
                parameters_hashed = json.load(f)

            for hash_key, parameter_list in parameters_hashed.items():
                hash_name = make_hash_name(parameter_list)

                hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="p")

                self.assertEqual(hash_id, hash_key, msg=f"Hash keys are not correct, check neuron type {neuron_type} "
                                                        f"and model {model_name} for updated parameter sets")

    def test_morphology_hash_name(self):

        model_dir = os.path.join("..", "data", "neurons", "striatum")

        morphology = "morphology"

        for neuron_dir in glob.glob(os.path.join(model_dir, "*/*")):

            neuron_type = neuron_dir.split("/")[-2]
            model_name = neuron_dir.split("/")[-1]
            hash_morphology = os.path.join(neuron_dir, "morphology", "morph_key_hash_name.json")

            with open(hash_morphology, "r") as f:
                trial_hash = json.load(f)
            morphologies = glob.glob(os.path.join(neuron_dir, "morphology", "*.swc"))
            excluded = list()

            for m in morphologies:
                m_name = m.split("/")[-1]
                if m_name in trial_hash.values():
                    with open(m, "r") as k:
                        whole = k.read()

                    hash_name = make_hash_name(whole)

                    hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="m")

                    self.assertTrue((hash_id in trial_hash.keys()), msg=f"Model {neuron_type} , {model_name} \n"
                                                                        f"Model directory {model_dir} \n"
                                                                        f"Morphology {m_name} \n")

                    self.assertEqual(trial_hash[hash_id], m_name)
                else:
                    excluded.append(m_name)

            print(f"These morphologies are excluded/not used in the model of {neuron_type}, {model_name}:")
            print(*excluded, sep="\n")
            print("\n")


if __name__ == '__main__':
    unittest.main()
