import os
import json
from collections import OrderedDict
import glob

#
# python3 gather_if_info.py /home/hjorth/HBP/BasalGangliaData/data/neurons/striatum/dspn /home/hjorth/HBP/bgmod/models/optim/HBP-2021Q4
#
# python3 gather_if_info.py /home/hjorth/HBP/BasalGangliaData/data/neurons/striatum/ispn /home/hjorth/HBP/bgmod/models/optim/HBP-2021Q4
#
# python3 gather_if_info.py /home/hjorth/HBP/BasalGangliaData/data/neurons/striatum/fs /home/hjorth/HBP/bgmod/models/optim/HBP-2022Q2/


class GatherIFInfo:

    def __init__(self):
        
        pass


    def load_neuron(self, meta_file, val_model_file, mapping_file):

        print(f"Loading meta_meta: {meta_file}\nval_model_file: {val_model_file}\nmapping_file: {mapping_file}")
        
        self.meta_info = self.read_json(meta_file)
        self.val_model_info = self.read_json(val_model_file)
        self.mapping_info = self.read_json(mapping_file)

        self.if_file_out = os.path.join(os.path.dirname(meta_file), "if_info.json")

    def read_json(self, json_file):
        with open(json_file, "r") as f:
            return json.load(f)

    # val_model_file:
    # List of models.
    #  morph -- morphology
    #  par -- parameter_id, needs to map using mapping_info to parameter_key
    #  id_curve --> stim, freq
    #
    # mapping_file: dictionary parameter_key --> parameter_id
    #
    # meta_info:
    #   parameter_key, morphology_key --> data
        
    def get_info(self, parameter_key, morphology_key):

        morphology = self.meta_info[parameter_key][morphology_key]["morphology"]
        parameter_id = self.mapping_info[parameter_key]

        stim = None
        freq = None

        for models in self.val_model_info:
            if morphology == models["morph"] and \
               parameter_id == models["par"]:
                
                stim = models["id_curve"]["stim"]
                freq = models["id_curve"]["freq"]

                break

        if stim is None or freq is None:
            import pdb
            pdb.set_trace()
            
        return stim, freq


    def iter_meta(self):
        for par_key in self.meta_info.keys():
            for morph_key in self.meta_info[par_key].keys():
                yield par_key, morph_key

    def write_if_file(self):

        data_out = OrderedDict()
        
        for par_key, morph_key in self.iter_meta():
            
            stim, freq = self.get_info(par_key, morph_key)

            if par_key not in data_out:
                data_out[par_key] = OrderedDict()


            try:
                data_out[par_key][morph_key] = OrderedDict()
                data_out[par_key][morph_key]["current"] = [s*1e-12 for s in stim]
                data_out[par_key][morph_key]["frequency"] = freq
            except:
                import traceback
                print(traceback.format_exc())
                import pdb
                pdb.set_trace()
                
                
        print(f"--> Writing current-frequency info to {self.if_file_out}\n")

        # assert not os.path.exists(self.if_file_out), f"Abort: {self.if_file_out} already exists"
        
        with open(self.if_file_out, "w") as f:
            json.dump(data_out, f, indent=2)
        

    def iter_neurons(self, neuron_type_dir, val_model_dir):
        meta_files = glob.glob(os.path.join(neuron_type_dir, "*", "meta.json"))
        for meta_file in meta_files:
            neuron_dir = os.path.dirname(meta_file)
            mapping_file = os.path.join(neuron_dir, "temp", "parameters_hash_id.json")
            
            neuron_dir_name = os.path.basename(neuron_dir)
            neuron_dir_name = self.val_model_dir_remapping(neuron_dir_name)
            val_model_file = os.path.join(val_model_dir, neuron_dir_name, "val_models.json")

            yield meta_file, val_model_file, mapping_file

    def write_all_if_files(self, neuron_type_dir, val_model_dir):
        for meta_file, val_model_file, mapping_file in self.iter_neurons(neuron_type_dir=neuron_type_dir,
                                                                         val_model_dir=val_model_dir):
            
            self.load_neuron(meta_file=meta_file, val_model_file=val_model_file, mapping_file=mapping_file)
            self.write_if_file()

    def val_model_dir_remapping(self, dir_name):
        
        with open("val_model_name_remapping.json", "r") as f:
            mapping_data = json.load(f)

        if dir_name in mapping_data:
            print(f"Remapping {dir_name} to {mapping_data[dir_name]}") 
            return mapping_data[dir_name]
        else:
            return dir_name
    
            
if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser("Create if_info.json file with information about frequency response to current injections")
    parser.add_argument("neuron_type_dir", help="Neuron type dir, e.g.'BasalGangliaData/data/neurons/striatum/dspn/'", type=str)
    parser.add_argument("val_model_dir", help="Val model dir, e.g. 'bgmod/models/optim/HBP-2021Q4/'", type=str)

    args = parser.parse_args()

    gifi = GatherIFInfo()
    gifi.write_all_if_files(neuron_type_dir=args.neuron_type_dir, val_model_dir=args.val_model_dir)
    
