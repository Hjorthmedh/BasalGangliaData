import os
from snudda.input.input_tuning import InputTuning

network_path = os.path.join("networks", "input_tuning_dspn")
input_tuning = InputTuning(network_path)

input_tuning.find_background_activity()
