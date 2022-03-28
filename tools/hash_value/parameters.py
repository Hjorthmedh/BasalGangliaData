import os

from tools.hash_value.make_hash import *

"""
    Hash keys for parameter sets
"""


def make_parameter_hash_key(parameter_list):
    hash_value = make_hash_name(parameter_list)

    hash_key = hash_identifier(hash_value=hash_value, length=8, prefix="p")

    return hash_key


def make_parameter_dict_hash_name(parameter_dict):
    """

    :param parameter_dict:
    :return:
    """
    translation = dict()
    hashed_parameter_dict = dict()

    for p_id, parameter_list in parameter_dict.items():
        hash_key = make_parameter_hash_key(parameter_list=parameter_list)
        hashed_parameter_dict.update({hash_key: parameter_list})
        translation.update({hash_key: p_id})

    if len(parameter_dict) != len(translation):
        raise ValueError(
            f"All parameter sets are not individual - there is replication as there are {len(parameter_dict)} parameter sets"
            f"while only {len(translation)} unique hash_keys")

    return hashed_parameter_dict, translation
