
import json, os
from collections import OrderedDict

def read_data(fname):
    v1 = [] # for parameter file
    m1 = {} # for mechanisms file
    
    with open(fname, 'r') as f:
        params_v2 = json.load(f)
    
    if 'global' in params_v2:
        for key,value in params_v2['global'].items():
            v1.append({ "param_name": key,
                        "type": "global",
                        "value": value})
    
    for key in params_v2.keys():
        if key == 'global': continue
        
        # should this be implemented some other way? (e.g. by importing mechanims.json)
        if key == 'axon':
            region = 'axonal'
        elif key == 'soma':
            region = 'somatic'
        else:
            region = key
        
        m1[region] = []
        
        for mech, item in params_v2[key].items():
            
            if not mech == 'neuron_specific':
                m1[region].append(mech)
            
            for p, i2 in item.items():
                
                param = i2
                param["sectionlist"] = region
                if mech == 'neuron_specific':
                    param["param_name"] = p
                else:
                    param["param_name"] = f'{p}_{mech}'
                    #param["mech"] = mech
                    #param["mech_param"] = p
                
                # fix dist_type
                if not param["dist_type"] == "uniform":
                    param["dist"] = param["dist_type"]
                    param["dist_type"] = "distance"               
                
                v1.append(param)
    
    return v1, m1
            

       


if __name__ == '__main__':
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Script converting model parameter(v1) in to v2')
    parser.add_argument('-f','--infile', help='parameter file (.json)', default=False)
    parser.add_argument('-s','--save', help='save new format to file?', action="store_true", default=False)
    dargs, ip = parser.parse_known_args()
    args = vars(dargs)
    
    if not args['infile']:
        if ip:
            # assume that the first argument is the infile
            args['infile'] = ip[0]
        else:
            raise Exception('Argument error - missing parameter file.\n' 
                           'Please add a parameter file.\n\n'
                           'Either use the -f flag or add it as the first argument:\n'
                           'python transform_parameters_to_v2.py -f path/to/parameters.json\n'
                           'python transform_parameters_to_v2.py path/to/parameters.json')
    
    v1, m1 = read_data(args['infile'])
    if args['save']:
        with open('param_v1.json', 'w') as f:
            json.dump(v1, f, indent=3)
        with open('mechanisms_v1.json', 'w') as f:
            json.dump(m1, f, indent=3)
    else:
        print(json.dumps(v1, indent=3))
        print()
        print(json.dumps(m1, indent=3))
    
        
        
    
    
    
