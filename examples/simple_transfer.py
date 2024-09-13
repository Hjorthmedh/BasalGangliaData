
import shutil, os, sys
sys.path.append('../tools')

from transfer import SimpleTransfer as strans

'''
if mechnisms.json, 
   parameters.json and 
   best_models.json 
all in base of source 
and morphology is in
    source/morphology 
specifying source and destination is all that should be needed
'''

# Please specify/update these paths, below
# ---------------------------------------------------------------
source_path         = '../examples/example-option-2' # extra path added for illustration
new_celltype_path   = '../data/neurons/striatum/test'
# ---------------------------------------------------------------


# create new folder for storing the new cell (using the same name as the source)
source_name = os.path.split(source_path)[-1]
new_cell_path = '{}/{}'.format(new_celltype_path, source_name) # past the name of the source model to the celltype path
os.makedirs(new_cell_path, exist_ok=True)


# do the transfer
strans.SimpleTransfer(source_path, new_cell_path)
