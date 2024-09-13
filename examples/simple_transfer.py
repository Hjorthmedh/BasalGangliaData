
import shutil, os, sys, argparse
sys.path.append('../tools')

from transfer import SimpleTransfer as strans

'''
run this file with arguments or change the paths to source and destination
below (source and new_celltype_path, respectively)

    $ python simple_transfer.py -s <source> -d <destination>

In order to use hall_of_fame instead of best_models (default)  
use the -h argument and send the path to the file

    $ python simple_transfer.py -hof path/hall_off_fame.json

use the -rm/--delete argument to delete the destination folder before transfer (if exists)
    
    $ python simple_transfer.py -rm 1

TODO: 
-verify transfer
'''

parser = argparse.ArgumentParser(description='Simple program for transfer (conversion) of BPO models into snudda')
parser.add_argument('-s','--sours', help='source directory')
parser.add_argument('-a','--all', help='transfer all models in directory (sub directories)', default=0)
parser.add_argument('-d','--destination', help='destination argument')
parser.add_argument('-hof','--hall_off_fame', help='list of best models (best_models/hall_off_fame)', default=None)
parser.add_argument('-rm','--delete', help='delete destination', default=0)
args = vars(parser.parse_args())    

def do_transfer(source_path, new_cell_path, hof):
    print('\n--------------------')
    print(f'tranfering source: \n\t{source_path} \nto destination \n\t{new_cell_path}\n')
    strans.SimpleTransfer(source_path, new_cell_path, optimisation_result_file=hof)

# Please specify/update these paths, below (if not added as argument(s))
# -------------------------------------------------------------------
if args['sours']:
    source_path = args['sours'].strip('/')
else:
    # update here
    source_path = '../examples/example-option-2' # extra path added for illustration
    
if args['destination']:
    new_celltype_path = args['destination']
else:
    # update here
    new_celltype_path = '../data/neurons/striatum/test'
# -------------------------------------------------------------------

# do the transfer
if args['all']:
    subdir = [ f.name for f in os.scandir(source_path) if f.is_dir() ]
    print(subdir)
    for d in subdir:
        celltype = d.split('-')[1] # this is hardcoded and assumes that the type is in the first location of the filename
        destination = os.path.join(new_celltype_path, celltype, d)
        sub_source_path = os.path.join(source_path, d)
        if int(args['delete']) and os.path.isdir(destination):
            shutil.rmtree(destination)
        os.makedirs(destination, exist_ok=True)
        do_transfer(sub_source_path, destination, args['hall_off_fame'])
else:
    if int(args['delete']):
        shutil.rmtree(new_celltype_path)
    
    # create a new folder for storing the new cell (using the same name as the source)
    if os.path.normpath(source_path).count(os.sep): # this check if there are more than one level in the path
        source_name = os.path.split(source_path)[-1]
    else:
        source_name = source_path

    new_cell_path = '{}/{}'.format(new_celltype_path, source_name) # past the name of the source model to the celltype path
    os.makedirs(new_cell_path, exist_ok=True)
    
    do_transfer(source_path, new_cell_path, args['hall_off_fame'])
    

