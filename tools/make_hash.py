import json
import hashlib


def hash_identifier(hash_name, length, prefix):
    hash_key = "".join([prefix, hash_name[:length]])

    return hash_key


def make_hash_name(data):
    a = json.dumps(data).encode("utf-8")
    hash_name = hashlib.md5(a).hexdigest()

    return hash_name
