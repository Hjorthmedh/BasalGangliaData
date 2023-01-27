Clone BasalGangliaData
Clone bgmod next to the BasalGangliaData folder

(You can run switch_folder_structure.py at this stage but it will not contain 
other neurons apart from dspn and ispn and will not have synapses folder etc. 
So instead follow the steps below.)

Copy the folders 20220930_1 and 20220930_2 from the backup folder and put them anywhere next to each other (as they are in the backup folder).
These folders contain everything except dspn and ispn. If you run the script with these as basis then you will get synapses folders etc included.

The code in switch_folder_structure.py will generate 20220930_1 (morphologies only, in correct folder structure)
and 20220930_2 (final output folder including parameters etc).
