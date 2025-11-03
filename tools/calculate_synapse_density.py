import os
import numpy as np
import json
from snudda import SnuddaLoad

def process_file(path):
    sl = SnuddaLoad(path)

    print(f"Creating connection matrix")
    connection_matrix = sl.create_connection_matrix()

    incoming_synapses_name = {}
    incoming_synapses_morph = {}
    incoming_synapse_density = {}

    with open("/home/hjorth/HBP/szmod/analysis/metadata/dspn_d2oe_0.00.json", "r") as f:
        morph_info = json.load(f)

    with open("/home/hjorth/HBP/szmod/analysis/metadata/ispn_d2oe_0.00.json", "r") as f:
        morph_info |= json.load(f)

    
    for neuron_name in np.unique([x["name"] for x in sl.data["neurons"]]):
        print(f"Processing {neuron_name}")
    
        for neuron_id in sl.get_centre_neurons_iterator(neuron_name=neuron_name,
                                                        return_distance=False):

            # post_id = neuron_id
            n_incoming = np.sum(connection_matrix[:, neuron_id])

            name = sl.data["neurons"][neuron_id]["name"]
            morph = sl.data["neurons"][neuron_id]["morphology"]

            morph_stub = os.path.splitext(os.path.basename(morph))[0]
            
            if name not in incoming_synapses_name:
                incoming_synapses_name[name] = []

            incoming_synapses_name[name].append(n_incoming)

            if morph not in incoming_synapses_morph:
                incoming_synapses_morph[morph] = []

            incoming_synapses_morph[morph].append(n_incoming)


            if morph_stub in morph_info:
                if morph_stub not in incoming_synapse_density:
                    incoming_synapse_density[morph_stub] = []

                dend_len = morph_info[morph_stub]["dend"]["length"]
                
                incoming_synapse_density[morph_stub].append(n_incoming/dend_len)

        

    for name, data in incoming_synapses_name.items():
        print(f"{name}: {np.mean(data):.2f} +/ {np.std(data):.2f}")

    for morph, data in incoming_synapses_morph.items():
        print(f"{os.path.basename(morph)}: {np.mean(data):.2f} +/ {np.std(data):.2f}")

    len_list = []
    den_list = []
    
        
    for morph, data in incoming_synapse_density.items():
        morph_stub = os.path.splitext(morph)[0]
        print(f"Density of {morph} (with dend length {morph_info[morph_stub]['dend']['length']:.2f} micrometer): {np.mean(data):.4f} +/- {np.std(data):.4f} synapses/micrometer")
        len_list.append(morph_info[morph_stub]['dend']['length'])
        den_list.append(np.mean(data))


    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(len_list,den_list,'k.')
    plt.xlabel("Dendritic length (micrometer)")
    plt.ylabel("Synapse density (1/micrometer)")
    plt.savefig("spn_synapse_density_summary.png")
    plt.ion()
    plt.show()
        
            
    
    import pdb
    pdb.set_trace()


if __name__ == "__main__":

    # process_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k/network-synapses.hdf5")

    # process_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k-mu2_zero/network-synapses.hdf5")

    # process_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k-mu2_one/network-synapses.hdf5")

    # rocess_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k-mu2_one_sm3/network-synapses.hdf5")

    # process_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k-mu2_1.5/network-synapses.hdf5")

    process_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k-mu2_2/network-synapses.hdf5")        
