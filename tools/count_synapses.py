import os
import numpy as np
import json
import h5py
from snudda import SnuddaLoad
import argparse
import matplotlib.pyplot as plt

class SynapseCount:

    def __init__(self, network_file, edges=None, input_file=None, core_diameter=300e-6):

        self.mod_lookup = {"GABA": "tmGabaA", "Glut": "tmGlut"}
        
        self.network_file = network_file
        self.input_file = input_file
        self.core_diameter = core_diameter

        self.snudda_load = SnuddaLoad(self.network_file)
        
        self.fig_path = os.path.join(os.path.dirname(network_file), "figures")
        os.makedirs(self.fig_path, exist_ok=True)

        
        if edges is not None:
            self.edges = edges
        else:
            self.edges = np.arange(0, 301, 10) * 1e-6 

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
        soma_synapses = 0
        
        for input_type in self.input_data["input"][str(neuron_id)]:
            inp = self.input_data["input"][str(neuron_id)][input_type]

            if mod == inp.attrs["mod_file"]:
                section_id = inp.attrs["section_id"]
                soma_mask = section_id == -1
                dist_to_soma = inp.attrs["distance_to_soma"][()]
                syn_per_bin, bin_edges = np.histogram(dist_to_soma[~soma_mask], bins=self.edges)

                assert all(dist_to_soma[soma_mask] == 0)  # Dist to soma on soma is 0
                soma_synapses += np.sum(soma_mask)
                
                synapses_per_bin += syn_per_bin

        return synapses_per_bin, soma_synapses

    def count_synapses_for_neuron_type(self, neuron_type, synapse_type="GABA"):

        neuron_id_list = self.snudda_load.get_neuron_id_of_type(neuron_type)
        neuron_id_list = self.get_core(neuron_id_list, core_diameter=self.core_diameter)
        
        synapses_per_bin = np.zeros((len(self.edges) - 1, ))
        neuron_count = 0
        soma_synapses = 0
        
        for n_id in neuron_id_list:
            syn_per_bin, soma_syn = self.count_synapses(n_id, synapse_type)
            synapses_per_bin += syn_per_bin
            soma_synapses += soma_syn
            neuron_count += 1

        return synapses_per_bin / neuron_count, soma_synapses / neuron_count

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

    def split_soma_dend_synapses(self, synapses):

        soma_mask = synapses[:,9] == -1
            
        soma_synapses = synapses[soma_mask,:]
        dend_synapses = synapses[~soma_mask,:]

        assert (soma_synapses[:,8] == 0).all()  # Soma dist for soma synapses should be 0
        
        return soma_synapses, dend_synapses

    def filter_synapses_on_pre_type(self, synapses, pre_type):

        if pre_type is None:
            return synapses
            
        pre_id = self.snudda_load.get_neuron_id_of_type(pre_type)
        mask = np.isin(synapses[:,0], pre_id)

        return synapses[mask, :]
        
        
    def count_internal_synapses(self, neuron_id, synapse_type="GABA", pre_type=None):

        
        synapses, coords = self.snudda_load.find_synapses(post_id=neuron_id)

        synapses = self.filter_synapses(synapses, synapse_type)

        synapses = self.filter_synapses_on_pre_type(synapses, pre_type)
        
        soma_synapses, dend_synapses = self.split_soma_dend_synapses(synapses)
        soma_syn = soma_synapses.shape[0]
        
        if len(dend_synapses) == 0:
            return np.zeros((len(self.edges) - 1, )), soma_syn
        
        dist_to_soma = dend_synapses[:, 8] * 1e-6

        syn_per_bin, bin_edges = np.histogram(dist_to_soma, bins=self.edges)


        
        return syn_per_bin, soma_syn

    def count_internal_synapses_for_neuron_type(self, neuron_type, synapse_type="GABA", pre_type=None):

        neuron_id_list = self.snudda_load.get_neuron_id_of_type(neuron_type)

        neuron_id_list = self.get_core(neuron_id_list, core_diameter=self.core_diameter)
        
        synapses_per_bin = np.zeros((len(self.edges) - 1, ))
        neuron_count = 0
        soma_synapses = 0
        
        for neuron_id in neuron_id_list:
            syn_per_bin, soma_s = self.count_internal_synapses(neuron_id, synapse_type, pre_type=pre_type)
            synapses_per_bin += syn_per_bin
            soma_synapses += soma_s
            neuron_count += 1

        return synapses_per_bin / neuron_count, soma_synapses / neuron_count
    

    def get_core(self, neuron_id_list, core_diameter):

        centre_point = np.mean(self.snudda_load.data["neuron_positions"], axis=0)
        dist_to_centre = np.linalg.norm(self.snudda_load.data["neuron_positions"] - centre_point, axis=1)

        centre_id = [x for x in neuron_id_list if dist_to_centre[x] < core_diameter/2]

        return centre_id
    
    
    def plot_synapse_counts(self, neuron_type, synapse_type="GABA", pre_type=None):

        edges_um = self.edges * 1e6
        
        if pre_type is None:
            # When pre_type is given we want only the synapses from internal neurons of this kind
            synapses_per_bin, soma_synapses = self.count_synapses_for_neuron_type(neuron_type=neuron_type,
                                                                                  synapse_type=synapse_type)
        internal_synapses_per_bin, internal_soma_synapses = \
            self.count_internal_synapses_for_neuron_type(neuron_type=neuron_type, synapse_type=synapse_type,
                                                         pre_type=pre_type)

        plt.figure()
        
        if pre_type is None:
            plt.stairs(synapses_per_bin, edges_um, linewidth=2, label="external")
            
        plt.stairs(internal_synapses_per_bin, edges_um, linewidth=2, label="internal")
        plt.xlabel("Distance from soma")
        plt.ylabel("Synapse count")

        if pre_type:
            pre_str = f" from {pre_type}"
            soma_syn_str = "{internal_soma_synapses:.1f} soma synapses)"
        else:
            pre_str = ""
            soma_syn_str = f"\n({soma_synapses:.1f} external soma synapses), {internal_soma_synapses:.1f} internal soma synapses)"
        
        title = f"Incoming {synapse_type} on {neuron_type}{pre_str} (average per neuron){soma_syn_str}"
        
        plt.title(title)
        plt.legend()
        plt.ion()
        if pre_type:
            fig_path = os.path.join(self.fig_path,f"incoming-{synapse_type}-on-{neuron_type}-from-{pre_type}.png")
        else:
            fig_path = os.path.join(self.fig_path,f"incoming-{synapse_type}-on-{neuron_type}.png")
        print(f"Saving to {fig_path}")
        plt.savefig(fig_path, bbox_inches="tight")
        plt.show()
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Count number of synapses")
    parser.add_argument("network_file")
    parser.add_argument("input_file")
    parser.add_argument("post_neuron_type")
    parser.add_argument("--pre_type", default=None, type=str)
    parser.add_argument("--synapse_type", help="'Glut' or 'GABA' input", default="GABA")
    parser.add_argument("--core_diameter", help="Diameter of core of neurons (default 300e-6)", default=300e-6, type=float)

    args = parser.parse_args()

    sc = SynapseCount(network_file=args.network_file, input_file=args.input_file, core_diameter=args.core_diameter)
    sc.plot_synapse_counts(neuron_type=args.post_neuron_type, synapse_type=args.synapse_type, pre_type=args.pre_type)
    # input("Press a key")
    
    # import pdb
    # pdb.set_trace()
