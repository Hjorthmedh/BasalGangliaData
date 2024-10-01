
import json, argparse, os
from collections import OrderedDict


def read_data(par):
    # read in data from param file
    newp = {}
    for p in par:
        if p['type'] == 'global':
            sl = 'global'
            if sl not in newp: newp[sl] = {}
            if 'value' in p:    
                newp[sl][p['param_name']] = p['value']
            elif 'bounds' in p: 
                newp[sl][p['param_name']] = p['bounds']
            else:
                raise Exception('global parameter % does not have neither "value" nor "bounds"' % p['param_name'])
            continue
        
        sl = p['sectionlist']
        del p['sectionlist']
        
        if sl not in newp: newp[sl] = {}
        
        if p['param_name'] == 'g_pas':
            p['mech'] = 'pas'
            p['mech_param'] = 'g'  
        
        if 'mech' in p:
            m = p['mech']
            param = p['mech_param']
            del p['mech']
        else:
            m = 'neuron_specific'
            param = p['param_name']
        
        if not m in newp[sl]: newp[sl][m] = {}
        #if not m in newp[sl][m]: newp[sl][m][param] = []
        
        del p['param_name']
        
        if 'mech_param' in p: 
            del p['mech_param']
        
        if not p['dist_type'] == 'uniform':
            p['dist_type'] = p['dist'] 
            del p['dist']
        
        newp[sl][m][param] = p
    
    return newp

def write2file(newp, pid, namebase, wuj=False, print_string=True):

    # PART 2: WRITE TO FILE ---------------------------------------------------------

    # write using json?
    if wuj:
        with open(f'{namebase}{pid}_v2.json', 'w') as h:
            json.dump(newp, h, indent=3)
        exit()

    # else: write using custom format
    n = 3
    t = ' '*n
    ss = '{\n'
    for i0, k1 in enumerate(['all', 'axon', 'basal', 'soma', 'global']):
        if k1 == 'soma' and k1 not in newp:
            if 'somatic' in newp:
                newp['soma'] = newp['somatic']
            else:
                print('Warning, no somatic parameters added')
                continue
        elif k1 == 'axon' and k1 not in newp:
            if 'axonal' in newp:
                newp['axon'] = newp['axonal']
            else:
                print('Warning, no axonal parameters added')
                continue
        elif k1 == 'basal' and k1 not in newp:
            if 'dend' in newp:
                newp['axon'] = newp['dend']
            elif 'dendritic' in newp:
                newp['axon'] = newp['dendritic']
            else:
                print('Warning, no basal parameters added')
                continue 
        i1 = newp[k1]
        ss += '%s"%s": {' % (t,k1)
        # global
        if k1 == 'global':
            for i, (k2,val) in enumerate(i1.items()):
                ss += '"{}": {} '.format(k2, val)
                if i+1 == len(i1):
                    if i0+1==len(newp):
                        ss += '%s' %  ('}\n')
                    else:
                        ss += '%s' %  ('}\n')  # if not last item: add ','
                else:
                    ss += ','
            continue
        # else
        for i, (k2,i2) in enumerate(i1.items()):
            ss += '\n%s"%s": {\n' % (t*2,k2)
            for j, (k3,i3) in enumerate(i2.items()):
                #if 'bar' in k3:
                #    k3 = 'gbar'
                if j+1 == len(i2):
                    ss += '%s"%s": %s\n' %  (t*3, k3, i3) 
                else:
                    ss += '{}"{}": {},\n'.format(t*3, k3, i3) 
            if i+1 == len(i1):
                ss += '%s %s' %  (t*3, '}\n')
            else:
                ss += '%s %s' %  (t*3, '},')
        ss += '%s%s,\n' % (t*2,'}')
                    
    ss += '}'
    ss = ss.replace("'", "#")
    ss = ss.replace('#', '"')
    
    with open(f'{namebase}{pid}_v2.json', 'w') as text_file:
        text_file.write(ss) #"Purchase Amount: %s" % TotalAmount)
    
    if print_string:
        print(ss)
    else:
        print(f'-param set {namebase}{pid} done!')
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Script converting model parameter(v1) in to v2')
    parser.add_argument('-f','--infile', help='parameter file (.json)', required=True)
    parser.add_argument('-s','--save', help='save new format to file?', default=0)
    parser.add_argument('-p','--print', help='print new format to shell', default=0)
    args = vars(parser.parse_args())
    
    namebase = os.path.splitext(args['infile'])[0]
    print(namebase)
    with open(args['infile'], 'r') as h:
        all_param_sets = json.load(h) #, object_pairs_hook=OrderedDict)  # ['pee2d330a'] 
    
    # how to check if the parameter file has more than one set of parameters?
    for i, k in enumerate(all_param_sets.keys()):
        parameters = read_data(all_param_sets[k])
        write2file(parameters, i, namebase, wuj=False, print_string=int(args['print']))
        
        
    
    
    
