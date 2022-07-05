import copy
import unittest
import os
import json
import glob
import deepdiff
import copy


class TestSum(unittest.TestCase):

    def test_lts(self):

        pass

    def test_chin(self):

        pass

    def test_fs(self):

        model_dir = os.path.join("..", "data", "neurons", "striatum", "fs")
        models = [m.split("/")[-1] for m in glob.glob(os.path.join(model_dir, "*"))]

        source_dir = os.path.join("../tools/test_data", "HBP-2021Q1")

        for m in models:

            with open(os.path.join(source_dir, m, "val_models.json"), "r") as f:
                val_models = json.load(f)

            with open(os.path.join(model_dir, m, "temp", "parameter_hash_to_id.json"), "r") as f:
                phash_to_id = json.load(f)

            with open(os.path.join(model_dir, m, "parameters.json"), "r") as f:
                created_parameters = json.load(f)

            inv_phash_to_id = {v: k for k, v in phash_to_id.items()}

            with open(os.path.join(source_dir, m, "hall_of_fame.json"), "r") as f:
                hall_of_fame = json.load(f)

            with open(os.path.join(model_dir, m, "meta.json"), "r") as f:
                meta = json.load(f)

            with open(os.path.join(source_dir, m, "config", "parameters.json"), "r") as f:
                parameters = json.load(f)

            with open(os.path.join(model_dir, m, "morphology", "morphology_hash_filename.json"), "r") as f:
                morphology = json.load(f)

            inv_morphology = {v: k for k, v in morphology.items()}

            for data_set in val_models:

                original = parameters
                created = created_parameters[inv_phash_to_id[data_set["par"]]]

                original_frozen = [o for o in original if "value" in o]
                frozen_parameters = list()

                # Check frozen parameters

                for subset in original_frozen:

                    for c in created:

                        if subset["param_name"] in c["param_name"] and subset["type"] == c["type"] \
                                and subset["type"] == c["type"]:
                            if "sectionlist" in subset.keys() and subset["sectionlist"] == c["sectionlist"] \
                                    and subset["dist_type"] == c["dist_type"] and "value" in c and "value" in subset:

                                frozen_parameters.append(c)

                                if "gbar" in subset["param_name"] or "pbar" in subset["param_name"]:

                                    if "fs" not in subset["param_name"]:

                                        subset["param_name"] = subset["param_name"] + "_fs"
                                        subset["mech"] = subset["mech"] + "_fs"

                            elif c["type"] == "global" and "value" in c and "value" in subset:
                                frozen_parameters.append(c)


                res = deepdiff.DeepDiff(original_frozen, frozen_parameters, ignore_order=True)
                temp = copy.deepcopy(res)
                for values_changed, data in res.items():
                    for k in data.keys():
                        if "dist" in k:
                            del temp[values_changed][k]
                if "values_changed" in temp.keys():
                    temp = temp["values_changed"]

                self.assertEqual(len(temp), 0)



                created = created_parameters[inv_phash_to_id[data_set["par"]]]
                h = hall_of_fame[data_set["par"]]

                optimized_parameters = dict()
                chosen_parameters = list()

                for name in h.keys():

                    for c in created:

                        name_section = name.split(".")

                        if name_section[0] == c["param_name"].replace("_fs", "") and name_section[1].replace("_fs", "") == c["sectionlist"]:
                            optimized_parameters.update({name: c["value"]})
                            chosen_parameters.append(c)

                res = deepdiff.DeepDiff(h, optimized_parameters, ignore_order=True)

                self.assertEqual(len(res), 0)

                self.assertTrue([inv_morphology[data_set["morph"]] in meta[inv_phash_to_id[data_set["par"]]].keys()])
                self.assertEqual(len(deepdiff.DeepDiff(chosen_parameters + frozen_parameters,
                                                       created, ignore_order=True)), 0)

            morphologies = dict()
            for data_set in val_models:

                if data_set["par"] not in morphologies.keys():
                    morphologies.update({data_set["par"]: 1})
                else:
                    morphologies[data_set["par"]] += 1

            for id_num, length in morphologies.items():
                self.assertEqual(len([*meta[inv_phash_to_id[id_num]].keys()]), length)

    def test_ispn(self):

        model_dir = os.path.join("..", "data", "neurons", "striatum", "ispn")
        models = [m.split("/")[-1] for m in glob.glob(os.path.join(model_dir, "*"))]

        source_dir = os.path.join("../tools/test_data", "HBP-2021Q4")

        for m in models:

            with open(os.path.join(source_dir, m, "val_models.json"), "r") as f:
                val_models = json.load(f)

            with open(os.path.join(model_dir, m, "temp", "parameter_hash_to_id.json"), "r") as f:
                phash_to_id = json.load(f)

            with open(os.path.join(model_dir, m, "parameters.json"), "r") as f:
                created_parameters = json.load(f)

            inv_phash_to_id = {v: k for k, v in phash_to_id.items()}

            with open(os.path.join(source_dir, m, "hall_of_fame.json"), "r") as f:
                hall_of_fame = json.load(f)

            with open(os.path.join(model_dir, m, "meta.json"), "r") as f:
                meta = json.load(f)

            with open(os.path.join(source_dir, m, "config", "parameters.json"), "r") as f:
                parameters = json.load(f)

            with open(os.path.join(model_dir, m, "morphology", "morph_key_hash_name.json"), "r") as f:
                morphology = json.load(f)

            inv_morphology = {v: k for k, v in morphology.items()}

            for data_set in val_models:

                original = parameters
                created = created_parameters[inv_phash_to_id[data_set["par"]]]

                original_frozen = [o for o in original if "value" in o]
                frozen_parameters = list()

                # Check frozen parameters

                for subset in original_frozen:

                    for c in created:

                        if subset["param_name"] == c["param_name"] and subset["type"] == c["type"] \
                                and subset["type"] == c["type"]:
                            if "sectionlist" in subset.keys() and subset["sectionlist"] == c["sectionlist"] \
                                    and subset["dist_type"] == c["dist_type"] and "value" in c and "value" in subset:
                                frozen_parameters.append(c)
                            elif c["type"] == "global" and "value" in c and "value" in subset:
                                frozen_parameters.append(c)
                res = deepdiff.DeepDiff(original_frozen, frozen_parameters, ignore_order=True)
                temp = copy.deepcopy(res)
                for values_changed, data in res.items():
                    for k in data.keys():
                        if "dist" in k:
                            del temp[values_changed][k]
                if "values_changed" in temp.keys():
                    temp = temp["values_changed"]

                self.assertEqual(len(temp), 0)



                created = created_parameters[inv_phash_to_id[data_set["par"]]]
                h = hall_of_fame[data_set["par"]]

                optimized_parameters = dict()
                chosen_parameters = list()

                for name in h.keys():

                    for c in created:

                        name_section = name.split(".")

                        if name_section[0] == c["param_name"] and name_section[1] == c["sectionlist"]:
                            optimized_parameters.update({name: c["value"]})
                            chosen_parameters.append(c)

                res = deepdiff.DeepDiff(h, optimized_parameters, ignore_order=True)

                self.assertEqual(len(res), 0)

                self.assertTrue([inv_morphology[data_set["morph"]] in meta[inv_phash_to_id[data_set["par"]]].keys()])
                self.assertEqual(len(deepdiff.DeepDiff(chosen_parameters + frozen_parameters,
                                                       created, ignore_order=True)), 0)

            morphologies = dict()
            for data_set in val_models:

                if data_set["par"] not in morphologies.keys():
                    morphologies.update({data_set["par"]: 1})
                else:
                    morphologies[data_set["par"]] += 1

            for id_num, length in morphologies.items():
                self.assertEqual(len([*meta[inv_phash_to_id[id_num]].keys()]), length)

    def test_dspn(self):
        model_dir = os.path.join("..", "data", "neurons", "striatum", "dspn")
        models = [m.split("/")[-1] for m in glob.glob(os.path.join(model_dir, "*"))]

        source_dir = os.path.join("../tools/test_data", "HBP-2021Q4")

        for m in models:

            with open(os.path.join(source_dir, m, "val_models.json"), "r") as f:
                val_models = json.load(f)

            with open(os.path.join(model_dir, m, "temp", "parameter_hash_to_id.json"), "r") as f:
                phash_to_id = json.load(f)

            with open(os.path.join(model_dir, m, "parameters.json"), "r") as f:
                created_parameters = json.load(f)

            inv_phash_to_id = {v: k for k, v in phash_to_id.items()}

            with open(os.path.join(source_dir, m, "hall_of_fame.json"), "r") as f:
                hall_of_fame = json.load(f)

            with open(os.path.join(model_dir, m, "meta.json"), "r") as f:
                meta = json.load(f)

            with open(os.path.join(source_dir, m, "config", "parameters.json"), "r") as f:
                parameters = json.load(f)

            with open(os.path.join(model_dir, m, "morphology", "morphology_hash_filename.json"), "r") as f:
                morphology = json.load(f)

            inv_morphology = {v: k for k, v in morphology.items()}

            for data_set in val_models:

                original = parameters
                created = created_parameters[inv_phash_to_id[data_set["par"]]]

                original_frozen = [o for o in original if "value" in o]
                frozen_parameters = list()

                # Check frozen parameters

                for subset in original_frozen:

                    for c in created:

                        if subset["param_name"] == c["param_name"] and subset["type"] == c["type"] \
                                and subset["type"] == c["type"]:
                            if "sectionlist" in subset.keys() and subset["sectionlist"] == c["sectionlist"] \
                                    and subset["dist_type"] == c["dist_type"] and "value" in c and "value" in subset:
                                frozen_parameters.append(c)
                            elif c["type"] == "global" and "value" in c and "value" in subset:
                                frozen_parameters.append(c)
                res = deepdiff.DeepDiff(original_frozen, frozen_parameters, ignore_order=True)
                temp = copy.deepcopy(res)
                for values_changed, data in res.items():
                    for k in data.keys():
                        if "dist" in k:
                            del temp[values_changed][k]
                if "values_changed" in temp.keys():
                    temp = temp["values_changed"]

                self.assertEqual(len(temp), 0)

                created = created_parameters[inv_phash_to_id[data_set["par"]]]
                h = hall_of_fame[data_set["par"]]

                optimized_parameters = dict()
                chosen_parameters = list()

                for name in h.keys():

                    for c in created:

                        name_section = name.split(".")

                        if name_section[0] == c["param_name"] and name_section[1] == c["sectionlist"]:
                            optimized_parameters.update({name: c["value"]})
                            chosen_parameters.append(c)

                res = deepdiff.DeepDiff(h, optimized_parameters, ignore_order=True)

                self.assertEqual(len(res), 0)

                self.assertTrue([inv_morphology[data_set["morph"]] in meta[inv_phash_to_id[data_set["par"]]].keys()])
                self.assertEqual(len(deepdiff.DeepDiff(chosen_parameters + frozen_parameters,
                                                       created, ignore_order=True)), 0)

            morphologies = dict()
            for data_set in val_models:

                if data_set["par"] not in morphologies.keys():
                    morphologies.update({data_set["par"]: 1})
                else:
                    morphologies[data_set["par"]] += 1

            for id_num, length in morphologies.items():
                self.assertEqual(len([*meta[inv_phash_to_id[id_num]].keys()]), length)



if __name__ == '__main__':
    unittest.main()
