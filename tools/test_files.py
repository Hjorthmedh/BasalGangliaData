import unittest
from transfer import *
import os
import json

class TestSum(unittest.TestCase):

    def test_from_old_format(self):

        parameter_file = "test_data/parameters_test.json"
        test_dir_path = "test_data"
        change_parameter_format_to_hash_key(json_file=parameter_file, dir_path=test_dir_path)
        self.assertTrue(os.path.isfile("test_data/parameter_id_hash_keys.json"), msg="parameter file not created")

    def test_correct_models(self):

        test_dspn = "test_data/dspn_c1/hall_of_fame.json"

        with open(test_dspn, "r") as f:
            data = json.load(f)

        model = "../data/neurons/striatum/dspn/str-dspn-e150602_c1_D1-mWT-0728MSN01-v20211026/"

        parameter_has_key = "parameter_id_hash_keys.json"

    def test_morphology_hash_name(self):


        model = "../data/neurons/striatum/dspn/str-dspn-e150602_c1_D1-mWT-0728MSN01-v20211026/"

        morphology = "morphology"

        os.path.join(model, morphology)

        import glob

        for f in glob.glob(os.path.join(model, morphology, "*.swc")):
            with open(f, "r") as k:
                whole = k.read()
            hash_name = make_hash_name(whole)

            hash_id = hash_identifier(hash_name=hash_name, length=8, prefix="m")

            print(hash_id)


    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 3)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()