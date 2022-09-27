# Temp commented out init line, since I had to manually remove FS since there
# where no tuned parameters.json for them.
# Also removed LTS and ChIN while testing.

# snudda init --size 100 TEST1-PD0 --snudda_data /home/hjorth/HBP/BasalGangliaData/Parkinson/Bo2022/PD0 --overwrite --seed 12345
snudda place TEST1-PD0
snudda detect TEST1-PD0
snudda prune TEST1-PD0
snudda input TEST1-PD0 --input /home/hjorth/HBP/Snudda/snudda/data/input_config/external-input-dSTR-scaled-v4.json

# snudda init --size 100 TEST1-PD2 --snudda_data /home/hjorth/HBP/BasalGangliaData/Parkinson/Bo2022/PD2 --connectionFile /home/hjorth/HBP/BasalGangliaData/Parkinson/Bo2022/PD2/connectivity/network-config-PD.json --overwrite --seed 12345
snudda place TEST1-PD2
snudda detect TEST1-PD2
snudda prune TEST1-PD2
snudda input TEST1-PD2 --input /home/hjorth/HBP/Snudda/snudda/data/input_config/external-input-dSTR-scaled-v4.json

