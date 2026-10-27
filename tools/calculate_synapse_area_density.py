# This code calculates the density of synapses along the dendrite, as a function of the soma

# TODO: Remove edge effects by only considering centre neurons!!

import os
import numpy as np
import json
import h5py
from snudda import SnuddaLoad
from snudda.utils.snudda_path import snudda_parse_path
from snudda.neurons.morphology_data import MorphologyData
import argparse
import matplotlib.pyplot as plt

class SynapseAreaDensity:

    def __init__(self, network_file, edges=None, input_file=None):
        self.network_file = network_file
        self.snudda_load = SnuddaLoad(self.network_file)
        self.fig_path = os.path.join(os.path.dirname(network_file), "figures")
        os.makedirs(self.fig_path, exist_ok=True)

        self.dend_density_cache = dict()

        if edges is not None:
            self.edges = edges
        else:
            self.edges = np.arange(0, 301, 10) * 1e-6 

        if input_file is not None:
            self.input_data = h5py.File(input_file, "r")
        else:
            self.input_data = None

    def calculate_dendrite_area_density(self, neuron_morphology):
        # Dendritic area found at each distance from soma

        if neuron_morphology not in self.dend_density_cache:
            md = MorphologyData(neuron_morphology)

            all_len = []
            all_area = []
            all_mid = []

            for s in md.section_iterator(section_type=3):
                r0, r1 = md.geometry[s.point_idx[:-1], 3], md.geometry[s.point_idx[1:], 3]
                d0, d1 = md.geometry[s.point_idx[:-1], 4], md.geometry[s.point_idx[1:], 4]
                xyz0, xyz1 = md.geometry[s.point_idx[:-1], :3], md.geometry[s.point_idx[1:], :3]
                slant = np.linalg.norm(xyz1 - xyz0, axis=1)
                seg_area = np.pi * (r0 + r1) * slant
                seg_mid = (d0 + d1) / 2
                
                # seg_len = md.geometry[s.point_idx[1:], 4] - md.geometry[s.point_idx[:-1], 4]
                # seg_mid = (md.geometry[s.point_idx[1:], 4] + md.geometry[s.point_idx[:-1], 4])/2
                # seg_r = (md.geometry[s.point_idx[1:], 3] + md.geometry[s.point_idx[:-1], 3])/2
                # seg_area = 2*np.pi*seg_r*seg_len
                # all_len.append(seg_len)
                all_mid.append(seg_mid)
                all_area.append(seg_area)

            # all_lengths = np.concatenate(all_len)
            all_mids = np.concatenate(all_mid)
            all_areas = np.concatenate(all_area)

            total_area_per_bin, bin_edges = np.histogram(all_mids, bins=self.edges, weights=all_areas)

            self.dend_density_cache[neuron_morphology] = total_area_per_bin

        return self.dend_density_cache[neuron_morphology]

    def get_all_morphologies_of_neuron_type(self, neuron_type):
        neuron_id = self.snudda_load.get_neuron_id_of_type(neuron_type)

        return set([self.snudda_load.get_morphology(nid) for nid in neuron_id])

    def get_all_neuron_id_with_morphology(self, morphology):

        return [x["neuron_id"] for x in self.snudda_load.data["neurons"]
                if snudda_parse_path(x["morphology"], self.snudda_load.snudda_data) == morphology]

    def split_soma_dend_synapses(self, synapses):

        soma_mask = synapses[:,9] == -1
            
        soma_synapses = synapses[soma_mask,:]
        dend_synapses = synapses[~soma_mask,:]

        assert (soma_synapses[:,8] == 0).all()  # Soma dist for soma synapses should be 0
        
        return soma_synapses, dend_synapses

    
    def calculate_synapse_density(self, neuron_id, pre_type=None):

        morph_file = self.snudda_load.get_morphology(neuron_id)
        dend_density = self.calculate_dendrite_area_density(morph_file)
        
        synapses, _ = self.snudda_load.find_synapses(pre_id=None, post_id=neuron_id)

        if synapses is None:
            return None, 0, 0
        
        if pre_type is not None:
            pre_id_list = self.snudda_load.get_neuron_id_of_type(neuron_type=pre_type)

            mask = np.isin(synapses[:, 0], pre_id_list)
            synapses = synapses[mask, :]

        soma_synapses, dend_synapses = self.split_soma_dend_synapses(synapses)
        num_soma_synapses = soma_synapses.shape[0]
        num_dend_synapses = dend_synapses.shape[0]
            
        synapse_soma_dist = dend_synapses[:, 8] * 1e-6
        synapses_per_bin, bin_edges = np.histogram(synapse_soma_dist, bins=self.edges)

        density = np.divide(synapses_per_bin, dend_density,
                            out=np.zeros_like(synapses_per_bin, dtype=float),
                            where=dend_density > 0)

        return density, num_soma_synapses, num_dend_synapses


    def calculate_synapse_density_for_morphology(self, morphology, pre_type=None, core_diameter=300e-6):

        neuron_id_list = [x["neuron_id"]
                          for x in self.snudda_load.data["neurons"]
                          if snudda_parse_path(x["morphology"], self.snudda_load.snudda_data) == morphology \
                          and x["virtual_neuron"] == False]

        neuron_id_list = self.get_core(neuron_id_list, core_diameter=core_diameter)
        
        density = np.zeros(len(self.edges) - 1)
        num_soma_synapses = 0
        num_dend_synapses = 0

        if len(neuron_id_list) == 0:
            return density, num_soma_synapses, num_dend_synapses
        
        for neuron_id in neuron_id_list:
            d, n_soma_syn, n_dend_syn = self.calculate_synapse_density(neuron_id, pre_type=pre_type)
            if d is not None:
                density += d
            num_soma_synapses += n_soma_syn
            num_dend_synapses += n_dend_syn

        density /= len(neuron_id_list)
        num_soma_synapses /= len(neuron_id_list)
        num_dend_synapses / len(neuron_id_list)
            
        return density, num_soma_synapses, num_dend_synapses

    def split_soma_dend_input_synapses(self, input_soma_dist, section_id):
        soma_mask = section_id == -1
        input_soma_dist_soma = input_soma_dist[soma_mask]
        input_soma_dist_dend = input_soma_dist[~soma_mask]

        assert (input_soma_dist_soma == 0).all()
        
        return input_soma_dist_soma, input_soma_dist_dend
    
    def calculate_input_density(self, neuron_id, input_type=None):

        morph_file = self.snudda_load.get_morphology(neuron_id)
        dend_density = self.calculate_dendrite_area_density(morph_file)

        synapses_per_bin = np.zeros((len(self.edges) - 1, ))
        num_soma_inputs = 0
        num_dend_inputs = 0

        for it in self.input_data["input"][str(neuron_id)].keys():

            if input_type is not None and it != input_type:
                # Only looking at specific input this time
                continue

            section_id = self.input_data["input"][str(neuron_id)][it].attrs["section_id"][()]
            input_soma_dist = self.input_data["input"][str(neuron_id)][it].attrs["distance_to_soma"][()]

            input_soma_dist_soma, input_soma_dist_dend = self.split_soma_dend_input_synapses(input_soma_dist,
                                                                                             section_id)
            
            syn_per_bin, bin_edges = np.histogram(input_soma_dist_dend, bins=self.edges)
            synapses_per_bin += syn_per_bin
            num_soma_inputs += len(input_soma_dist_soma)
            num_dend_inputs += len(input_soma_dist_dend)

        density = np.divide(synapses_per_bin, dend_density,
                            out=np.zeros_like(synapses_per_bin, dtype=float),
                            where=dend_density > 0)

        return density, num_soma_inputs, num_dend_inputs

    def calculate_input_density_for_morphology(self, morphology, input_type=None, core_diameter=300e-6):

        neuron_id_list = [x["neuron_id"]
                          for x in self.snudda_load.data["neurons"]
                          if snudda_parse_path(x["morphology"], self.snudda_load.snudda_data) == morphology \
                          and x["virtual_neuron"] == False]

        neuron_id_list = self.get_core(neuron_id_list, core_diameter=core_diameter)

        density = np.zeros(len(self.edges) - 1)
        num_soma_inputs = 0
        num_dend_inputs = 0

        if len(neuron_id_list) == 0:
            return density, num_soma_inputs, num_dend_inputs
        
        for neuron_id in neuron_id_list:
            d, n_soma_inputs, n_dend_inputs = self.calculate_input_density(neuron_id, input_type=input_type)
            if d is not None:
                density += d

            num_soma_inputs += n_soma_inputs
            num_dend_inputs += n_dend_inputs

        density /= len(neuron_id_list)
        num_soma_inputs /= len(neuron_id_list)
        num_dend_inputs /= len(neuron_id_list)

        return density, num_soma_inputs, num_dend_inputs


    def get_core(self, neuron_id_list, core_diameter=300e-6):

        centre_point = np.mean(self.snudda_load.data["neuron_positions"], axis=0)
        dist_to_centre = np.linalg.norm(self.snudda_load.data["neuron_positions"] - centre_point, axis=1)

        centre_id = [x for x in neuron_id_list if dist_to_centre[x] < core_diameter/2]

        return centre_id
        
    def plot_density(self, density, num_soma_synapses, num_dend_synapses, label="Synapse density", ax=None, color=None, title=None, y_label="Synapse density", fig_path=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        edges_um = self.edges * 1e6

        # Plot binned staircase outline and filled area onto the axis
        # We want synapses per micrometer, not per meter (hence * 1e-6)
        # ax.stairs(density * 1e-6, edges_um, fill=True, alpha=0.3, label=label, color=color)
        if color is not None:
            ax.stairs(density * 1e-12, edges_um, linewidth=2, color=color, label=label)
        else:
            ax.stairs(density * 1e-12, edges_um, linewidth=2, label=label)

        ax.set_xlabel("Distance to Soma (µm)")
        ax.set_ylabel(f"{y_label} (1/µm2)")
        # ax.legend(fontsize=8, loc='upper right')

        if title:
            ax.set_title(title + f"\n(average {num_soma_synapses:.1f} synapses on soma, {num_dend_synapses:.1f} synapses on dend)")

        ax.grid(True, linestyle="--", alpha=0.5)

        if fig_path is not None:
            print(f"Writing figure to {fig_path}")
            ax.get_figure().savefig(fig_path, bbox_inches='tight')

        return ax

    def plot_all_density(self, neuron_type, pre_type=None, core_diameter=300e-6):
        all_morph = self.get_all_morphologies_of_neuron_type(neuron_type=neuron_type)

        num_soma_synapses_all = 0
        num_dend_synapses_all = 0
        
        ax = None
        for morph in all_morph:
            print(f"Processing {morph}")
            density, num_soma_synapses, num_dend_synapses = self.calculate_synapse_density_for_morphology(morphology=morph, pre_type=pre_type, core_diameter=core_diameter)
            plot_label = f"Synaptic density on {neuron_type}"
            if pre_type is not None:
                plot_label += f" for {pre_type}"
            plot_label += f" ({morph})"
            ax = self.plot_density(density=density,
                                   num_soma_synapses=num_soma_synapses,
                                   num_dend_synapses=num_dend_synapses,
                                   label=plot_label, ax=ax)
            num_soma_synapses_all += num_soma_synapses
            num_dend_synapses_all += num_dend_synapses

        num_soma_synapses = num_soma_synapses_all / len(all_morph)
        num_dend_synapses = num_dend_synapses_all / len(all_morph)

        ax.set_title(f"Synapse density on {neuron_type}" + ("" if pre_type is None else f" from {pre_type}")
                     + f"\n{num_soma_synapses:.1f} synapses on soma, {num_dend_synapses:.1f} on dendrites")

        pre_text = "" if pre_type is None else f"-from-{pre_type}"
        fig_path = os.path.join(self.fig_path, f"synaptic-area-density-on-{neuron_type}{pre_text}.png")
        print(f"Saving figure {fig_path}")
        ax.get_figure().savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.ion()
        plt.show()

    def plot_all_input_density(self, neuron_type, input_type=None, core_diameter=300e-6):
        all_morph = self.get_all_morphologies_of_neuron_type(neuron_type=neuron_type)
        num_soma_inputs_all = 0
        num_dend_inputs_all = 0
        
        ax = None
        for morph in all_morph:
            print(f"Processing {morph}")
            density, num_soma_synapses, num_dend_synapses= self.calculate_input_density_for_morphology(morphology=morph, input_type=input_type, core_diameter=core_diameter)
            plot_label = f"Input density on {neuron_type}"
            if input_type is not None:
                plot_label += f" ({input_type})"
            plot_label += f" ({morph})"
            ax = self.plot_density(density=density,
                                   num_soma_synapses=num_soma_synapses,
                                   num_dend_synapses=num_dend_synapses,
                                   label=plot_label, ax=ax)
            num_soma_inputs_all += num_soma_synapses
            num_dend_inputs_all += num_dend_synapses

        num_soma_inputs = num_soma_inputs_all / len(all_morph)
        num_dend_inputs = num_dend_inputs_all / len(all_morph)
            
        ax.set_title(f"Input density on {neuron_type}" + ("" if input_type is None else f"({input_type})")
                     + f"\n{num_soma_synapses:.1f} synapses on soma, {num_dend_inputs:.1f} synapses on dend")

        input_text = "" if input_type is None else f"-{input_type}"
        fig_path = os.path.join(self.fig_path, f"input-area-density-on-{neuron_type}{input_text}.png")
        print(f"Saving figure {fig_path}")
        ax.get_figure().savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.ion()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate synapse density distribution")
    parser.add_argument("network_path", help="Path to network file")
    parser.add_argument("neuron_type", help="Post synaptic neuron type")
    parser.add_argument("--pre_type", help="Pre-synaptic neuron type", default=None)
    parser.add_argument("--core_diameter", help="Diameter of core of neurons (default 200e-6)", default=200e-6, type=float)
    parser.add_argument("--input_file", help="Input file (hdf5)", default=None)
    parser.add_argument("--input_type", help="Input type", default=None)

    args = parser.parse_args()

    sd = SynapseAreaDensity(network_file=args.network_path, input_file=args.input_file)

    sd.plot_all_density(neuron_type=args.neuron_type, pre_type=args.pre_type, core_diameter=args.core_diameter)

    if args.input_file:
        sd.plot_all_input_density(neuron_type=args.neuron_type, input_type=args.input_type, core_diameter=args.core_diameter)

    # input("Press a key to exit.")
