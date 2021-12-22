import shutil
import os


def transfer_mechanisms(source, destination):
    shutil.copy(os.path.join(source, "config", "mechanisms.json"), os.path.join(destination, "mechanisms.json"))
