from transfer.mechanisms import transfer_mechanisms
from transfer.parameters import transfer_parameters
from transfer.morphology import transfer_morphologies
from meta.create_meta import write_meta
from transfer.selected_models import transfer_selected_models
import os

class TransferBluePyOptToSnudda:

    """

    Class to Transfer all the files from Bluepyopt format to Snudda

    """

    def __init__(self, source=None, destination=None, mechanisms_path_folder=None, parameters_path_folder=None,
                 morphology_path_folder=None, optimisation_result_path=None, selected_models=None, selected=False):

        self.option = None
        self.source = source
        self.destination = destination
        self.selected = selected
        self.selected_models = selected_models
        self.mechanisms_path_folder = mechanisms_path_folder
        self.parameters_path_folder = parameters_path_folder
        self.morphology_path_folder = morphology_path_folder
        self.optimisation_result_path = optimisation_result_path

    def transfer(self):


        transfer_mechanisms(source=self.source,direct_path=self.mechanisms_path_folder,
                            destination=self.destination, selected=self.selected)
        transfer_parameters(direct_path_param=self.parameters_path_folder,
                            direct_path_best_models=self.optimisation_result_path, destination=self.destination)

        transfer_morphologies(direct_path_morph=self.morphology_path_folder,
                              destination=self.destination, selected=self.selected)
        write_meta(directory=destination, selected=self.selected)

        if self.selected:
            transfer_selected_models(source=self.source, destination=self.destination, direc_path_selected=self.selected_models)








