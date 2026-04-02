2026-03-26: (RL) ---------------
Removing duplicate models with same electrophysiology but different axons
- chin.json:
 original folder removed ($SNUDDA_DATA/neurons/striatum/chin/str-chin-e170614_cell6-m17JUL301751_170614_no6_MD_cell_1_x63-v20190710")
    and cell index shift by one for remaining models:
        "ChIN_0": "$SNUDDA_DATA/neurons/striatum/chin/str-chin-Opt0"
	    "ChIN_1": "$SNUDDA_DATA/neurons/striatum/chin/str-chin-Opt1"
	    "ChIN_2": "$SNUDDA_DATA/neurons/striatum/chin/str-chin-Opt2"

- str-chin-Opt0/meta.json:
    1 morphology from original model (deleted above) moved to the Opt0/meta.json, param set: "p06791b5b", 
    as the param set in that folder were identical to the Opt0 version (except for v_init: -80 vs -60 mV and e_pas: -55 vs -50). 
    In the paper by Johanna and Ilaria, DOI: 10.1111/ejn.14854 they say: 
        "To reproduce an intrinsically generated spontaneous activity,
        the reversal potential of the passive current was increased
        by a maximum of 5 mV for the ChIN models"
    This creates a setup in Opt0:
        "p06791b5b": {
            "morph1": {...},
            "morph2": {...}
            }
        "p62677738": {
            "m92fb243d": {...}
    
- an AIS was also added to all Opt[0,1,2]/meta.json:
    "axon_stump": {
                "axon_length":   [30e-6, 30e-6],
                "axon_diameter": [1e-6,  1e-6]
            }

- str-chin-Opt0/parameters.json
    e_pas updated to -50 in order to match fig 5 in Hjorth et al., 2020 microcircuit of striatum in silico (stim protocol also extracted from that paper)
    (this is also in accordance with the paper by Johanna and Ilaria)

2025-04-02 (RL) ------------
ChIN models opt 0-2 transferred from this repo:
https://github.com/jofrony/ChIN-LTS-Network-simulation/tree/master/config/CholinergicOptimisation

The model catalogues were manually updated:
- with a config folder (holding mechanisms.json and parameters.json)
- with a morphology folder (holding the swc-file)
- a hall_of_fame.json file (holding selected parameter sets from best_models.json

Only parameter sets with a specific param file in the base of the model folder (e.g. v0 or v9) were added
