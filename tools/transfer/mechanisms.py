import shutil
import os


def transfer_mechanisms(source, destination):

    """
    :param source: path to the model directory (BluePyOpt output), see examples for how
                    this directory should be structured
    :param destination: path to BasalGanglia/data/your_brain_area/neuron_type/model_name
    :return:
    """
    shutil.copy(os.path.join(source, "config", "mechanisms.json"), os.path.join(destination, "mechanisms.json"))
