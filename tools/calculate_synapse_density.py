import os
import numpy as np
from snudda import SnuddaLoad

def process_file(path):
    sl = SnuddaLoad(path)

    print(f"Creating connection matrix")
    connection_matrix = sl.create_connection_matrix()

    incoming_synapses_name = {}
    incoming_synapses_morph = {}

    for neuron_name in np.unique([x["name"] for x in sl.data["neurons"]]):
        print(f"Processing {neuron_name}")
    
        for neuron_id in sl.get_centre_neurons_iterator(neuron_name=neuron_name,
                                                        return_distance=False):

            # post_id = neuron_id
            n_incoming = np.sum(connection_matrix[:, neuron_id])

            name = sl.data["neurons"][neuron_id]["name"]
            morph = sl.data["neurons"][neuron_id]["morphology"]

            if name not in incoming_synapses_name:
                incoming_synapses_name[name] = []

            incoming_synapses_name[name].append(n_incoming)

            if morph not in incoming_synapses_morph:
                incoming_synapses_morph[morph] = []

            incoming_synapses_morph[morph].append(n_incoming)


    for name, data in incoming_synapses_name.items():
        print(f"{name}: {np.mean(data)} +/ {np.std(data)}")

    for morph, data in incoming_synapses_morph.items():
        print(f"{os.path.basename(morph)}: {np.mean(data)} +/ {np.std(data)}")

        

            
    
    import pdb
    pdb.set_trace()


if __name__ == "__main__":

    process_file("/home/hjorth/HBP/Snudda/examples/networks/test-10k/network-synapses.hdf5")
