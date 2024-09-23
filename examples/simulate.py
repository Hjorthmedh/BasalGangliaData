
import json, os
import numpy as np
from collections import OrderedDict

'''
script for direct comparison between org and transfered model
'''

def simulate_org_model(model_path, pid, return_tv=True, plot=False, print_psection=False):
    
    # change directory
    orgdir = os.getcwd()
    os.chdir(f'{model_path}checkpoints')
    
    # compile mechanisms 
    if return_tv or plot:
        print(return_tv, plot)
        ggg
        os.system('rm -rf x86_64')
        os.system("nrnivmodl ../mechanisms")
    
    # model setup ----------------------------------
    from neuron import h
    h.load_file("stdrun.hoc");
    
    name = f'Cell_{pid}'
    h.load_file(f'{name}.hoc')
    cmd = f'h.{name}("../morphology/")'
    cell = eval(cmd)
    
    if print_psection:
        for sec in h.allsec():
            print(h.psection(sec=sec))
        if not return_tv:
            return 0,0
    
    # import config files
    with open('../config/parameters.json') as fp:
        parameters = json.load(fp)
    with open('../config/protocols.json') as fp:
        protocols = json.load(fp, object_pairs_hook=OrderedDict)
    
    h.v_init = parameters[1]['value']
    h.celsius = parameters[0]['value']
    
    proto = list(p for p in protocols if p.startswith('IDthresh_'))[0]
    stim0 = protocols[proto]['stimuli'][0]['amp']
    stim1 = protocols[proto]['stimuli'][1]['amp']
    
    simtot = 1500 # hardcoding simlen
    
    hold = h.IClamp(cell.soma[0](0.5))
    hold.amp = stim1 
    hold.delay = 0
    hold.dur = simtot
    
    stimuli = h.IClamp(cell.soma[0](0.5))
    stimuli.amp = stim0 
    stimuli.delay = 700
    stimuli.dur = simtot
    
    # save voltage
    time = h.Vector()
    time.record(h._ref_t)
    vm = h.Vector()
    vm.record(cell.soma[0](0.5)._ref_v)
    
    # run
    h.tstop = simtot  
    cvode = h.CVode()
    cvode.active(0)
    h.dt = 0.025
    h.run();
    
    # cleanup
    os.system('rm -rf x86_64')
    os.chdir(orgdir)
    
    # plot/save/return voltage
    if plot:
        import matplotlib.pyplot as plt
        plt.plot(time, vm)
        plt.xlim([0,3000]) # remove this lim? (added for comparison with original model)
        plt.show()
        
        if not return_tv:
            return 0,0
    
    return np.array(time), np.array(vm)

def upgrade_parameters_to_v2(model_path):
    with open(f'{model_path}parameters.json', 'r') as h:
        all_param_sets = json.load(h)
    keys = all_param_sets.keys()
    kid = 9
    k = keys[kid]
    #param_file_str = f'{model_path}/parameters.json'
    #cmd = 'python Local_simulation_setup/transform_parameters_to_v2.py'
    
    sys.path.append('Local_simulation_setup')
    import transform_parameters_to_v2
    parameters = read_data(all_param_sets[k])
    write2file(parameters, kid, model_path, wuj=False, print_string=True)
    

def simulate_transfered_model(model_path, pid, plot=False):
    # TODO!
    
    # move all scripts needed here.
    
    # import ion channels from the org source
    
    # map org to transfered
    
    # create param_v2
    upgrade_parameters_to_v2(model_path)
    
    ggg
    
    
    # change directory
    orgdir = os.getcwd()
    os.chdir(model_path)
    
    # compile mechanisms 
    os.system('rm -rf x86_64')
    os.system("nrnivmodl ../mechanisms")
    
    # model setup ----------------------------------
    from neuron import h
     
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='script for direct comparison between org and transfered model')
    parser.add_argument('-p','--path', help='path to original model', required=True)
    parser.add_argument('-i','--mid', help='model id (0-9, default 0)', default=0)
    parser.add_argument('-s','--psprint', help='print psection? (default False)', default=0)
    parser.add_argument('-f','--plot', help='plot voltage? (default False)', default=0)
    parser.add_argument('-r','--return_tv', help='return time and voltage? (default True)', default=1)
    args = vars(parser.parse_args())
    
    if not args['psprint']:
        pps = False
    else:
        pps = True
    
    #if not args['return_tv']:
    
    simulate_transfered_model(args['path'], args['mid'], plot=int(args['mid']))
    
    t,v = simulate_org_model(   args['path'], 
                                args['mid'], 
                                plot=int(args['mid']), 
                                print_psection=int(args['psprint']),
                                return_tv=int(args['return_tv']))
    
    
    
    
