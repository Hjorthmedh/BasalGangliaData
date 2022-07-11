import json
import hashlib

'''
NOTE!!!!!!!!

    Creating hash keys are sensitive to how the data is read and
    it calculates the hash key based on the current order of the contents.

    For dictionaries, it is therefore important to always used the same
    way of opening and saving the contents to keep the order.
    
    !!!!! SEE examples on how this is currently solved !!!!!!
    
'''

"""

    The functions which are used to calculate the hash keys
    for the contents of parameters.json, *.swc and modulation.json
    
    All used length = 8
    parameters.json has prefix 'p'
    *.swc has prefix 'm'
    modulation.json prefix 'nm'
    
    
    To calculate a hash key:
    
    Firstly, open file and extract content of the parameter set,
    morphology (i.e content of *.swc) or the modulation parameter set
    
    For example, for parameters.json
    
    with open("parameters.json") as f:
        param_set = json.load(f)
        
    Next step,
    
    select parameter set, for example a parameter set which is 
    currently at index 3 in the list (if parameters.json is a list
    of parameter sets)
    
    data = param_set[3] # parameter set
    
    Last step
    
    long_hash = make_hash_name(data=data) # calculate the long hash name
    hash_key = hash_identified(hash_name=long_hash, length=8, prefix='p')
    
    We are finished and have a hash_key for our parameter set
    
    

"""


def hash_identifier(hash_value, length, prefix):
    hash_key = "".join([prefix, hash_value[:length]])

    return hash_key


def make_hash_name(data):
    a = json.dumps(data).encode("utf-8")
    hash_key = hashlib.md5(a).hexdigest()

    return hash_key
