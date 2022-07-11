import os

from tools.hash_value.make_hash import *

"""
    Hash keys for morphologies
"""

def swc_file_to_hash_key(swc_filename):

    with open(swc_filename, "r") as k:
        whole = k.read()

    hash_value = make_hash_name(whole)

    hash_key = hash_identifier(hash_value=hash_value, length=8, prefix="m")

    return hash_key


def make_morphology_hash_key_dict(morphology_total):
    hash_name_dict = dict()

    for swc_filepath in morphology_total:
        morphology_name = os.path.basename(swc_filepath)

        hash_key = swc_file_to_hash_key(swc_filename=swc_filepath)

        hash_name_dict.update({hash_key: morphology_name})

    return hash_name_dict
