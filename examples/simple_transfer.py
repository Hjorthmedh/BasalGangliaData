
import shutil, os, sys, argparse, glob
import recenter_morph as rcm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools")))

from transfer import SimpleTransfer as strans

'''
if no arguments are given an example model will be transfered

-use arguments -s and -d to specify input and output location

    $ python simple_transfer.py -s <source> -d <destination>

-use -a or --all to batch transfer all models in one directory

    $ python simple_transfer.py -s <source> -d <destination> -a 1
'''

def center_morphology(source_path):
    # loop over all swc files in the morphology folder of the source and checks that the morphology is centered
    allm = glob.glob(os.path.join(f'{source_path}/morphology/', "*.swc"))
    for mfile in allm:
        rcm.recenter(mfile)
        

def do_transfer(source_path, new_cell_path):
    # The morphology must be centered - check and center if not centered.
    center_morphology(source_path)
    
    # create output dir (check for existence is done in prev stage)
    os.makedirs(new_cell_path)
    
    files_in_folder = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
    if not len(files_in_folder):
        raise Exception('\n\nInput Error - the source directory is empty\n'
                        f'{source_path}\n'
                        'Possibly the files are in a subdirectory of the source?')
    elif os.path.isfile(f'{source_path}/val_models.json'):
        opt_res = f'{source_path}/hall_of_fame.json'
        select  = f'{source_path}/val_models.json'
        f = 'val_models.json'
    elif os.path.isfile(f'{source_path}/hall_of_fame.json'):
        opt_res = f'{source_path}/hall_of_fame.json'
        select  = None
        f = 'hall_of_fame.json'
    elif os.path.isfile(f'{source_path}/best_models.json'):
        opt_res = None
        select  = None
        f = 'best_models.json'
    else:
        raise Exception(f'Neither of: val_models, hall_of_fame nor best_models exist in source: \n{source_path}')
    
    print(f'\ntranfering source: \n\t{source_path} \nto destination \n\t{new_cell_path}')
    print(f'\nusing opt_file: {f}\n')
    strans.SimpleTransfer(  source_path, 
                            new_cell_path, 
                            optimisation_result_file=opt_res,
                            selected_models=select)


def transfer_all(source_path, new_celltype_path, clean=False):
    print(f"Reading from source_path={source_path}")
    subdir = [ f.name for f in os.scandir(source_path) if f.is_dir() ]
    print(subdir)
    for d in subdir:
        # celltype is hardcoded and assumes that the type is in the first location of the filename "str-dspn-..."
        try:
            celltype = d.split('-')[1] 
        except:
            print(f'\nmodel: {d}')
            print('\tcelltype can not be extracted from the model name')
            print('\tin order to work with batch transfer, model names have to be in the format:')
            print('\n\tregion-type-additional_info\n\te.g. str-dspn-...')
            print('--> skipping')
            continue
        destination = os.path.join(new_celltype_path, celltype, d)
        sub_source_path = os.path.join(source_path, d)
        if os.path.isdir(destination):
            print()
            print(f'Destination: {destination} \nalready exists')
            print('--> skipping')
            continue    
        
        do_transfer(sub_source_path, destination)
        
        if clean:
            import shutil
            shutil.rmtree(f"{destination}/temp")

def transfer_single(source_path, new_celltype_path, clean=False):    
    # create a new folder for storing the new cell (using the same name as the source)
    if os.path.normpath(source_path).count(os.sep): # this check if there are more than one level in the path - if so use last
        source_name = os.path.split(source_path)[-1]
    else:
        source_name = source_path
    
    new_cell_path = os.path.join(new_celltype_path, source_name) # paste the name of the source model to the celltype path
    
    if os.path.isdir(new_cell_path):
        print()
        raise Exception(f'the output path folder already exists: \n{new_cell_path}')
    
    do_transfer(source_path, new_cell_path)
    
    if clean:
        import shutil
        shutil.rmtree(f"{new_cell_path}/temp")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple program for transfer (conversion) of BPO models into snudda')
    parser.add_argument('--source', '-s', help='source directory')
    parser.add_argument('--destination', '-d', help='destination argument')
    parser.add_argument('--all', '-a', help='transfer all models in directory (sub directories)', action="store_true", default=False)
    parser.add_argument('--clean', '-c', help='clean dest by deleting temp files', action="store_true", default=False)
    #parser.add_argument('-hof','--hall_off_fame', help='list of best models (best_models/hall_off_fame)', default=None)
    #parser.add_argument('-rm','--delete', help='delete destination -- can not be used with the -a/--all option', default=0)
    args = parser.parse_args()

    
    if args.source:
        source_path = args.source.rstrip('/')
    else:
        # update here
        source_path = '../examples/example-option-2' # extra "../examples/" added for testing/illustration
        
    if args.destination:
        new_celltype_path = args.destination
    else:
        # update here
        new_celltype_path = '../data/neurons/striatum/test'
    
    # do the transfer
    if args.all:
        transfer_all(source_path, new_celltype_path, clean=args.clean)
    else:
        transfer_single(source_path, new_celltype_path, clean=args.clean)
    
