import os
import numpy as np
import json
import h5py
from snudda import SnuddaLoad
import argparse
import matplotlib.pyplot as plt

class SynapseCount:

    def __init__(self, network_file, edges=None, input_file=None):

        self.mod_lookup = {"GABA": "tmGabaA", "Glut": "tmGlut"}
        
        self.network_file = network_file
        self.edges = edges
        self.input_file = input_file

        self.snudda_load = SnuddaLoad(self.network_file)
        
        self.fig_path = os.path.join(os.path.dirname(network_file), "figures")
        os.makedirs(self.fig_path, exist_ok=True)

        
        if edges is not None:
            self.edges = edges
        else:
            self.edges = np.arange(0, 300e-6, 10e-6)

        if input_file is not None:
            self.input_data = h5py.File(input_file, "r")
            self.input_config = json.loads(self.input_data["config"][()])
        else:
            self.input_data = None
            self.input_config = None

        self.build_channel_model_lookup()


    def count_synapses(self, neuron_id, synapse_type="GABA"):

        mod = self.mod_lookup[synapse_type]

        synapses_per_bin = np.zeros((len(self.edges) - 1, ))
        
        for input_type in self.input_data["input"][str(neuron_id)]:
            inp = self.input_data["input"][str(neuron_id)][input_type]

            if mod == inp.attrs["mod_file"]:
                dist_to_soma = inp.attrs["distance_to_soma"][()]
                syn_per_bin, bin_edges = np.histogram(dist_to_soma, bins=self.edges)

                synapses_per_bin += syn_per_bin

        return synapses_per_bin

    def count_synapses_for_neuron_type(self, neuron_type, synapse_type="GABA"):

        neuron_id = self.snudda_load.get_neuron_id_of_type(neuron_type)
        synapses_per_bin = np.zeros((len(self.edges) - 1, ))
        neuron_count = 0
        
        for n_id in neuron_id:
            synapses_per_bin += self.count_synapses(n_id, synapse_type)
            neuron_count += 1

        return synapses_per_bin / neuron_count

    def build_channel_model_lookup(self):
        self.channel_model_lookup = dict()
        con_dist = self.snudda_load.data["connectivity_distributions"]
        
        for con in con_dist.values():
            for con2 in con.values():
                try:
                    if con2["channel_model_id"] == 3:
                        # Skip gap junctions
                        continue

                    self.channel_model_lookup[con2["channel_model_id"]] = con2["channel_parameters"]["mod_file"]
                except:
                    import traceback
                    print(traceback.format_exc())
                    import pdb
                    pdb.set_trace()
                    
    def filter_synapses(self, synapses, synapse_type):

        mod_file = self.mod_lookup[synapse_type]
        channel_id = synapses[:,6]

        index = [idx for idx, c_id in enumerate(channel_id) if self.channel_model_lookup[c_id] == mod_file]

        return synapses[index, :]
                
    def count_internal_synapses(self, neuron_id, synapse_type="GABA"):

        synapses, coords = self.snudda_load.find_synapses(post_id=neuron_id)

        synapses = self.filter_synapses(synapses, synapse_type)
        dist_to_soma = synapses[8, :] * 1e-6
        
        syn_per_bin, bin_edges = np.histogram(dist_to_soma, bins=self.edges)

        return syn_per_bin

    def count_internal_synapses_for_neuron_type(self, neuron_type, synapse_type="GABA"):

        neuron_id = self.snudda_load.get_neuron_id_of_type(neuron_type)
        synapses_per_bin = np.zeros((len(self.edges) - 1, ))
        neuron_count = 0
        
        for n_id in neuron_id:
            synapses_per_bin += self.count_internal_synapses(n_id, synapse_type)
            neuron_count += 1

        return synapses_per_bin / neuron_count
    
        
    def plot_synapse_counts(self, neuron_type, synapse_type="GABA"):

        edges_um = self.edges * 1e6
        synapses_per_bin = self.count_synapses_for_neuron_type(neuron_type, synapse_type)
        internal_synapses_per_bin = self.count_internal_synapses_for_neuron_type(neuron_type, synapse_type)
        plt.figure()
        plt.stairs(synapses_per_bin, edges_um, linewidth=2, label="external")
        plt.stairs(internal_synapses_per_bin, edges_um, linewidth=2, label="internal")
        plt.xlabel("Distance from soma")
        plt.ylabel("Synapse count")
        plt.title(f"Incoming {synapse_type} on {neuron_type} (average per neuron)")
        plt.legend()
        plt.ion()
        fig_path = os.path.join(self.fig_path,f"incoming-{synapse_type}-on-{neuron_type}.png")
        print(f"Saving to {fig_path}")
        plt.savefig(fig_path, bbox_inches="tight")
        plt.show()
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Count number of synapses")
    parser.add_argument("network_file")
    parser.add_argument("input_file")
    parser.add_argument("post_neuron_type")
    parser.add_argument("--input_type", help="'Glut' or 'GABA' input", default="GABA")

    args = parser.parse_args()

    sc = SynapseCount(network_file=args.network_file, input_file=args.input_file)
    sc.plot_synapse_counts(neuron_type=args.post_neuron_type, synapse_type=args.input_type)
    input("Press a key")
    
    import pdb
    pdb.set_trace()
