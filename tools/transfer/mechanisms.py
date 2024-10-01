import shutil
import os


def transfer_mechanisms(source=None, destination=None, direct_path=None):

    """
    :param source: path to the model directory (BluePyOpt output), see examples for how
                    this directory should be structured
    :param destination: path to BasalGanglia/data/your_brain_area/neuron_type/model_name
    :param direct_path: folder path to where mechanisms.json is
    :return:
    """

    if direct_path:
        mechanisms_path = os.path.join(direct_path, "mechanisms.json")
    else:
        mechanisms_path = os.path.join(source, "config", "mechanisms.json")

    #check if dir exists , if not, create
    if not os.path.exists(destination):
        os.mkdir(destination)
    shutil.copy(mechanisms_path, os.path.join(destination, "mechanisms.json"))
    
    print("mechanims file transfer complete")
