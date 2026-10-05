# This code calculates the density of synapses along the dendrite, as a function of the soma

import os
import numpy as np
import json
from snudda import SnuddaLoad
from snudda.utils.snudda_path import snudda_parse_path
from snudda.neurons.morphology_data import MorphologyData
import argparse
import matplotlib.pyplot as plt

class SynapseDensity:

    def __init__(self, network_file, edges=None):
        self.network_file = network_file
        self.snudda_load = SnuddaLoad(self.network_file)
        self.fig_path = os.path.join(os.path.dirname(network_file), "figures")
        os.makedirs(self.fig_path, exist_ok=True)

        self.dend_density_cache = dict()

        if edges is not None:
            self.edges = edges
        else:
            self.edges = np.arange(0, 300e-6, 10e-6)


    def calculate_dendrite_density(self, neuron_morphology):
        # Dendritic length found at each distance from soma

        if neuron_morphology not in self.dend_density_cache:
            md = MorphologyData(neuron_morphology)

            all_len = []
            all_mid = []

            for s in md.section_iterator(section_type=3):
                seg_len = md.geometry[s.point_idx[1:], 4] - md.geometry[s.point_idx[:-1], 4]
                seg_mid = (md.geometry[s.point_idx[1:], 4] + md.geometry[s.point_idx[:-1], 4])/2
                all_len.append(seg_len)
                all_mid.append(seg_mid)

            all_lengths = np.concatenate(all_len)
            all_mids = np.concatenate(all_mid)

            total_length_per_bin, bin_edges = np.histogram(all_mids, bins=self.edges, weights=all_lengths)

            self.dend_density_cache[neuron_morphology] = total_length_per_bin

        return self.dend_density_cache[neuron_morphology]

    def get_all_morphologies_of_neuron_type(self, neuron_type):
        neuron_id = self.snudda_load.get_neuron_id_of_type(neuron_type)

        return set([self.snudda_load.get_morphology(nid) for nid in neuron_id])

    def get_all_neuron_id_with_morphology(self, morphology):

        return [x["neuron_id"] for x in self.snudda_load.data["neurons"]
                if snudda_parse_path(x["morphology"], self.snudda_load.snudda_data) == morphology]

    def calculate_synapse_density(self, neuron_id, pre_type=None):

        morph_file = self.snudda_load.get_morphology(neuron_id)
        dend_density = self.calculate_dendrite_density(morph_file)

        synapses, _ = self.snudda_load.find_synapses(pre_id=None, post_id=neuron_id)

        if pre_type is not None:
            pre_id_list = self.snudda_load.get_neuron_id_of_type(neuron_type=pre_type)

            mask = np.isin(synapses[:, 0], pre_id_list)
            synapses = synapses[mask, :]

        synapse_soma_dist = synapses[:, 8] * 1e-6
        synapses_per_bin, bin_edges = np.histogram(synapse_soma_dist, bins=self.edges)

        density = np.divide(synapses_per_bin, dend_density,
                            out=np.zeros_like(synapses_per_bin, dtype=float),
                            where=dend_density > 0)

        return density


    def calculate_synapse_density_for_morphology(self, morphology, pre_type=None):

        neuron_id_list = [x["neuron_id"]
                          for x in self.snudda_load.data["neurons"]
                          if snudda_parse_path(x["morphology"], self.snudda_load.snudda_data) == morphology \
                          and x["virtual_neuron"] == False]

        density = np.zeros(len(self.edges) - 1)

        for neuron_id in neuron_id_list:
            density += self.calculate_synapse_density(neuron_id, pre_type=pre_type)

        density /= len(neuron_id_list)

        return density

    def plot_density(self, density, label="Synapse density", ax=None, color=None, title=None, y_label="Synapse density", fig_path=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        edges_um = self.edges * 1e6

        # Plot binned staircase outline and filled area onto the axis
        # We want synapses per micrometer, not per meter (hence * 1e-6)
        # ax.stairs(density * 1e-6, edges_um, fill=True, alpha=0.3, label=label, color=color)
        if color is not None:
            ax.stairs(density * 1e-6, edges_um, linewidth=2, color=color, label=label)
        else:
            ax.stairs(density * 1e-6, edges_um, linewidth=2, label=label)

        ax.set_xlabel("Distance to Soma (µm)")
        ax.set_ylabel(f"{y_label} (1/µm)")
        # ax.legend(fontsize=8, loc='upper right')

        if title:
            ax.set_title(title)

        ax.grid(True, linestyle="--", alpha=0.5)

        if fig_path is not None:
            print(f"Writing figure to {fig_path}")
            ax.get_figure().savefig(fig_path, bbox_inches='tight')

        return ax

    def plot_all_density(self, neuron_type, pre_type=None):
        all_morph = self.get_all_morphologies_of_neuron_type(neuron_type=neuron_type)

        ax = None
        for morph in all_morph:
            print(f"Processing {morph}")
            density = self.calculate_synapse_density_for_morphology(morphology=morph, pre_type=pre_type)
            plot_label = f"Synaptic density on {neuron_type}"
            if pre_type is not None:
                plot_label += f" for {pre_type}"
            plot_label += f" ({morph})"
            ax = self.plot_density(density=density, label=plot_label, ax=ax)

        ax.set_title(f"Synapse density on {neuron_type}" + ("" if pre_type is None else f" from {pre_type}"))

        pre_text = "" if pre_type is None else f"-from-{pre_type}"
        fig_path = os.path.join(self.fig_path, f"synaptic-density-on-{neuron_type}{pre_text}.png")
        print(f"Saving figure {fig_path}")
        ax.get_figure().savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.ion()
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate synapse density distribution")
    parser.add_argument("network_path", help="Path to network file")
    parser.add_argument("neuron_type", help="Post synaptic neuron type")
    parser.add_argument("--pre_type", help="Pre-synaptic neuron type", default=None)

    args = parser.parse_args()

    sd = SynapseDensity(network_file=args.network_path)

    sd.plot_all_density(neuron_type=args.neuron_type, pre_type=args.pre_type)

    input("Press a key to exit.")