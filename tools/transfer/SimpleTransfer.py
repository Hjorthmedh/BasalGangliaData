from transfer.mechanisms import transfer_mechanisms
from transfer.parameters import transfer_parameters
from transfer.morphology import transfer_morphologies
from meta.create_meta import write_meta
from transfer.selected_models import transfer_selected_models
import os

class SimpleTransfer:

    """
    Class to Transfer all the files from Bluepyopt format to Snudda
    
    By default assumes that the files
        -mechanisms.json
        -parameters.json
    are located in the config folder of the source, and that 
        -best_model.json 
    are in the base of source (else file path can be added manually, see below)
    
    if you are using hall_of_fame.json instead of best_models.json,
        please set the optimization_result_file directly
    
    Also assumes that the morphology file is in source/morphology
        if not, specify as argument
        
    If model selection is enabled (selected=True), the list of models is filled from selected_models file.
    """

    def __init__(self,  source, 
                        destination, 
                        optimisation_result_file=None,
                        mechanisms_path_folder=None, 
                        parameters_path_folder=None, 
                        morphology_path_folder=None, 
                        selected_models=None, 
                        selected=False):
        
        self.source = source
        self.destination = destination
        
        if not optimisation_result_file:
            self.optimisation_result_file = f'{source}/best_models.json'
        else:
            self.optimisation_result_file = optimisation_result_file
        
        if not mechanisms_path_folder:
            self.mechanisms_path_folder = f'{source}/config'
        else:
            self.mechanisms_path_folder = mechanisms_path_folder
        
        if not parameters_path_folder:
            self.parameters_path_folder = f'{source}/config/parameters.json'
        else:
            self.parameters_path_folder = parameters_path_folder
        
        if not morphology_path_folder:
            self.morphology_path_folder = f'{source}/morphology'
        else:
            self.morphology_path_folder = morphology_path_folder
        
        self.selected = selected
        self.selected_models = selected_models
        
        self.transfer()
        
        print('\n---transfer complete---')

    def transfer(self):


        transfer_mechanisms(source=self.source, direct_path=self.mechanisms_path_folder,
                            destination=self.destination)
        transfer_parameters(direct_path_param=self.parameters_path_folder,
                            direct_path_best_models=self.optimisation_result_file, destination=self.destination)

        if self.selected:
            transfer_selected_models(source=self.source, destination=self.destination, direc_path_selected=self.selected_models)

        transfer_morphologies(direct_path_morph=self.morphology_path_folder,
                              destination=self.destination, selected=self.selected)
        write_meta(directory=self.destination, selected=self.selected)








