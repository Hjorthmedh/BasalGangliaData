import os
import numpy as np
import json
from snudda import SnuddaLoad
import argparse
import matplotlib.pyplot as plt
    
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
                                                        return_distance=False,
                                                        n_neurons=500):

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
            else:
                print(f"Missing {morph_stub} in morph_info")
                import pdb
                pdb.set_trace()

        

    for name, data in incoming_synapses_name.items():
        print(f"{name}: {np.mean(data):.2f} +/- {np.std(data):.2f}")

    for morph, data in incoming_synapses_morph.items():
        print(f"{os.path.basename(morph)}: {np.mean(data):.2f} +/- {np.std(data):.2f}")

    len_list = []
    den_list = []
    
        
    for morph, data in incoming_synapse_density.items():
        morph_stub = os.path.splitext(morph)[0]
        print(f"Density of {morph} (with dend length {morph_info[morph_stub]['dend']['length']:.2f} micrometer): {np.mean(data):.4f} +/- {np.std(data):.4f} synapses/micrometer")
        len_list.append(morph_info[morph_stub]['dend']['length'])
        den_list.append(np.mean(data))



    plt.figure()
    fig, ax = plt.subplots(figsize=(4, 4), dpi=300)
    ax.plot(len_list, den_list, 'k.', markersize=6)

    plt.plot(len_list,den_list,'k.')
    plt.xlabel("Dendritic length (micrometer)")
    plt.ylabel("Synapse density (1/micrometer)")

    # Turn spines on and style them
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_linewidth(1.2)

    # Ticks outward, on all sides
    ax.tick_params(direction="out",
                   length=4,
                   width=1.2,
                   top=True,
                   right=True)

    ax.set_xlabel("Dendritic length (µm)", fontsize=11)
    ax.set_ylabel("Synapse density (µm⁻¹)", fontsize=11)
    plt.tight_layout()
    fig.subplots_adjust(left=0.18, bottom=0.18, right=0.95, top=0.95)
    plt.savefig("spn_synapse_density_summary.pdf", bbox_inches="tight")
    plt.savefig("spn_synapse_density_summary.png")
    plt.ion()
    plt.show()


    # import pdb
    # pdb.set_trace()
        
    input("Press a key")     





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check density of synapses in network synapse file')
    parser.add_argument('path', type=str, help='Path to the network-synapses.hdf5 file')
    
    args = parser.parse_args()
    
    process_file(args.path)    
