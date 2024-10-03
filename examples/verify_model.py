
import json, os
import numpy as np
from collections import OrderedDict

'''
script for direct comparison between org and transfered model

needs path to the reference and transfered models.
The following arguments can be used to customize the command:
options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to original model
  -o OUT, --out OUT     path to output model
  -i MID, --mid MID     model id (0-9, default 0)
  -s PSPRINT, --psprint PSPRINT
                        print psection? (default False)
  -v PLOT, --plot PLOT  plot voltage of reference model by itself? (default False)
  -r RETURN_TV, --return_tv RETURN_TV
                        return time and voltage? Needed for comparison (default True)
  -u UPGRADE, --upgrade UPGRADE
                        upgrade params--must be done if not done before
                        (default False)


if run from the terminal, use e.g. the following command:
python simulate.py -p ../../Alex_model_repo/models/optim/HBP-2022Q2/str-dspn-e150602_c1_D1-mWT-0728MSN01-v20220620/ -o ../data/neurons/striatum/test/str-dspn-e150602_c1_D1-mWT-0728MSN01-v20220620/ -s 0 -i 0
'''

def simulate_org_model(model_path, pid, return_tv=True, plot=False, print_psection=False, current_amplitude=None):
    
    # change directory
    orgdir = os.getcwd()
    os.chdir(f'{model_path}checkpoints')
    
    # compile mechanisms 
    if return_tv or plot:
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
    
    
    print('1. simulating reference model...')
    
    # import config files
    with open('../config/parameters.json') as fp:
        parameters = json.load(fp)
    
    h.v_init = parameters[1]['value']
    h.celsius = parameters[0]['value']
    if current_amplitude:
        stim0 = current_amplitude # nA
        stim1 = 0
    else:
        with open('../config/protocols.json') as fp:
            protocols = json.load(fp, object_pairs_hook=OrderedDict)
        
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
    #os.system('rm -rf x86_64')
    os.chdir(orgdir)
    
    # plot/save/return voltage
    if plot:
        import matplotlib.pyplot as plt
        plt.plot(time, vm)
        plt.show()
        
        if not return_tv:
            return 0,0
    
    return np.array(time), np.array(vm)

def simulate_snudda(    transfered_model_path, 
                        ref_model_path=None,
                        hashkey=None, 
                        mkey=None,
                        pid=0, 
                        ref_tv=[],
                        sim_len=1.5,
                        print_psection=False,
                        current_amplitude=None):
    
    print('2.1 simulating transfered model in snudda...\n')
    if not hashkey:
        # get hash key corresponding to model index (pid)
        with open(f'{transfered_model_path}temp/parameters_hash_id.json', 'r') as h:
            hash2id = json.load(h)
        id2hash = {int(item):key for key,item in hash2id.items()} # reverse key:item 
        hashkey = id2hash[pid]
    if not mkey:
        morph_path = get_morphology_source_file(transfered_model_path)
        with open(f'{transfered_model_path}morphology/morphology_hash_filename.json', 'r') as h:
            mhash2name = json.load(h)
        name2mhash = {name:mkey for mkey,name in mhash2name.items()} # reverse key:item
        morph = os.path.splitext(os.path.basename(morph_path))[0]
        mkey = name2mhash[f'{morph}-var0.swc'] # var0 and the original morphology are identical
    
    # model setup ----------------
    from snudda import Snudda
    network_path = "snudda"
    ss = Snudda(network_path=network_path)
    ss.init_tiny(   neuron_paths=[transfered_model_path], 
                    neuron_names=["Cell"], 
                    number_of_neurons=[1],
                    morphology_key=[mkey],
                    parameter_key=[hashkey])
    
    ss.create_network()
    
    # current amplitude and delay from file
    if current_amplitude:
        stim1=0 * 1e-9
        stim0=current_amplitude * 1e-9 # nA to A 
    elif os.path.isfile(f'{ref_model_path}config/protocols.json'):
        with open(f'{ref_model_path}config/protocols.json') as fp:
            protocols = json.load(fp, object_pairs_hook=OrderedDict)
        proto = list(p for p in protocols if p.startswith('IDthresh_'))[0]
        stim0 = protocols[proto]['stimuli'][0]['amp'] * 1e-9
        stim1 = protocols[proto]['stimuli'][1]['amp'] * 1e-9
    else:
        print('NOT ABLE TO OPEN PROTOCOL FILE. Using a standard stimuli of 300 pA')
        import time
        time.sleep(5)
        stim1=0 * 1e-9
        stim0=0.3 * 1e-9 # using 300 pA
    
    simulation_config = {"current_injection_info" : {"0": {"time": [0, 0.7, 0.7, sim_len],
                                                       "current": [stim1, stim1, stim1+stim0, stim1+stim0]}}}
    # simulate
    sim = ss.simulate(simulation_config=simulation_config, verbose=False, time=sim_len)
    
    if print_psection:
        h = sim.sim.neuron.h
        for sec in h.allsec():
            print(h.psection(sec=sec))
    
    
    # plot
    from snudda.utils import SnuddaLoadSimulation
    sls = SnuddaLoadSimulation(network_path=network_path)
    time = sls.get_time()
    neuron_id = 0
    voltage = sls.get_data(neuron_id=neuron_id, data_type="voltage")[0][neuron_id]
    vm = voltage.T[0]*1000
    t = time*1000
    
    print('3. Comparing models...')
    if len(ref_tv):
        if all(vm == ref_tv[1]):
            print('\t-> models gives identical results')
        else:
            print('\t-> models differ')
            print(vm)
            print(ref_tv[1])
    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,8))
    plt.title('comparing reference and transfer models', fontsize=20)
    plt.plot(t, vm, label='transfered', lw=3)
    if len(ref_tv):
        plt.plot(ref_tv[0], ref_tv[1], ls='dotted', label='reference', lw=3)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig('org_and_snudda.png')
    plt.show()
    
    
def upgrade_parameters_to_v2(model_path, hashkey, kid=0):
    # open transfered parameter file. This file contains many families of models
    with open(f'{model_path}parameters.json', 'r') as h:
        all_param_sets = json.load(h)
    
    import transform_parameters_to_v2 as trans
    parameters = trans.read_data(all_param_sets[hashkey])
    trans.write2file(parameters, kid, model_path, print_string=False)


def get_morphology_source_file(ref_model_path):
    # get morphology
    from glob import glob
    morphologies = glob(f'{ref_model_path}morphology/*.swc')
    for morph in morphologies:
        if 'var' not in morph:
            print(morph)
            return morph
    return None
    

def simulate_transfered_model(ref_model_path, transfered_model_path, pid, upgrade_params=True, ref_tv=[], print_psection=False):
        
    # import ion channels from the org source (the reference model)
    import neuron as nrn
    import sys
    sys.path.append('Local_simulation_setup')
    #nrn.load_mechanisms(f'{ref_model_path}mechanisms')
    
    # get hash key corresponding to model index (pid)
    with open(f'{transfered_model_path}temp/parameters_hash_id.json', 'r') as h:
        hash2id = json.load(h)
    id2hash = {int(item):key for key,item in hash2id.items()} # reverse key:item 
    hashkey = id2hash[pid]
    
    morph = get_morphology_source_file(ref_model_path)
    
    # create param_v2
    if upgrade_params:
        print('2.0 upgrading parameters...')
        upgrade_parameters_to_v2(transfered_model_path, hashkey, kid=pid) # Cell0 from original setup
    
    # model setup ----------------------------------
    from neuron import h
    h.load_file("stdrun.hoc")
    
    import matplotlib.pyplot as plt
    import cell_builder as create
    
    # cadyn mechanisms are for now hardcoded. TODO: how to generalize--is it needed or is below standard?
    # the region must for now be either soma, basal or axon. 
    # The dyn mechanism itself have to be part of the compiled mechanisms under ./mechanisms
    region_cadyn_dict = {   'soma':  ['cadyn_ms', 'caldyn_ms'],
                            'basal': ['cadyn_ms', 'caldyn_ms']}
    
    cell = create.Bpo_cell(f'{transfered_model_path}{pid}_v2.json',
                          morph,
                          cell_type='transFerdinand',
                          region_cadyn_dict=region_cadyn_dict,
                          allow_non_uniform=False)
    
    if print_psection:
        for sec in h.allsec():
            h.psection(sec=sec)
    
    print('2.1 simulating transfered model...')
        
    with open(f'{ref_model_path}config/protocols.json') as fp:
        protocols = json.load(fp, object_pairs_hook=OrderedDict)

    proto = list(p for p in protocols if p.startswith('IDthresh_'))[0]
    stim0 = protocols[proto]['stimuli'][0]['amp']
    stim1 = protocols[proto]['stimuli'][1]['amp']

    simtot = 1500 # hardcoding simlen

    hold = h.IClamp(cell.soma(0.5))
    hold.amp = stim1 
    hold.delay = 0
    hold.dur = simtot

    stimuli = h.IClamp(cell.soma(0.5))
    stimuli.amp = stim0 
    stimuli.delay = 700
    stimuli.dur = simtot

    # save voltage
    time = h.Vector()
    time.record(h._ref_t)
    vm = h.Vector()
    vm.record(cell.soma(0.5)._ref_v)

    # run
    h.tstop = simtot  
    cvode = h.CVode()
    cvode.active(0)
    h.dt = 0.025
    h.run()
    
    
    print('3. Comparing models...')
    if len(ref_tv):
        if all(np.array(vm) == ref_tv[1]):
            print('\t-> models gives identical results')
        else:
            print('\t-> models differ')
            print(np.array(vm))
            print(ref_tv[1])
    
    plt.figure(figsize=(12,8))
    plt.title('comparing reference and transfer models', fontsize=20)
    plt.plot(time, vm, label='transfered', lw=3)
    if len(ref_tv):
        plt.plot(ref_tv[0], ref_tv[1], ls='dotted', label='reference', lw=3)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig('org_and_my.png')
    plt.show()
     
def print_hashkey2id(model_path):
    import sys
    with open(f'{model_path}/temp/parameters_hash_id.json') as fp:
        h2id = json.load(fp)
    print(h2id)
    sys.exit()

def get_amplitude(current_amplitude):
    if len(current_amplitude.split()) > 1:
        raise ValueError(f'current_amplitude must either be given as a number (in nA)\nor a string with units (A/nA/pA), without space. E.g: 100pA\n\tnot {current_amplitude}')    
    elif 'nA' in current_amplitude:
        print(f"nano ampere... {current_amplitude.split('nA')[0]}")
        return float(current_amplitude.split('nA')[0])
    elif 'pA' in current_amplitude:
        return float(current_amplitude.split('pA')[0]) * 1e-3
    elif 'A' in current_amplitude:
        return float(current_amplitude.split('A')[0]) * 1e9
    else:
        raise ValueError(f'current_amplitude must either be given as a number (in nA)\nor a string with units (A/nA/pA), without space. E.g: 100pA\n\tnot {current_amplitude}')
        

def main_compare(ref_model, trans_model, mid=0, print_psection=False, current_amplitude=False):
    # can be used to compare models with a single command
    amp = current_amplitude
    if current_amplitude:
        if type(current_amplitude)==str:
            # try to extract value from string
            amp = get_amplitude(current_amplitude)
            
    ref_tv = simulate_org_model(   ref_model,
                                   mid,
                                   print_psection=print_psection,
                                   return_tv=True,
                                   current_amplitude=amp)

    simulate_snudda(trans_model, ref_model_path=ref_model, pid=mid, ref_tv=ref_tv, print_psection=print_psection, current_amplitude=amp)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='script for direct comparison between org and transfered model')
    parser.add_argument('-p','--path', help='path to original model', required=True)
    parser.add_argument('-o','--out', help='path to output model', required=True)
    parser.add_argument('-i','--mid', help='model id (0-9, default 0)', default=0)
    parser.add_argument('-s','--psprint', help='print psection? (default False)', default=0)
    parser.add_argument('-v','--plot', help='plot voltage of reference model by itself? (default False)', default=0)
    parser.add_argument('-r','--return_tv', help='return time and voltage? Needed for comparison (default True)', default=1)
    parser.add_argument('-u','--upgrade', help='upgrade params--must be done if not done before (default False)', default=0)
    parser.add_argument(      '--print_hashkeys', help='print all hashkeys:id combinations in the transfered param file and exit', action="store_true", default=False)

    args = vars(parser.parse_args())
    
    if args['print_hashkey']:
        print_hashkey2id(args['out'])
        
    if not args['psprint']:
        pps = False
    else:
        pps = True
    
    t,v = simulate_org_model(   args['path'], 
                                int(args['mid']), 
                                plot=args['plot'], 
                                print_psection=int(args['psprint']),
                                return_tv=int(args['return_tv']))
    
    simulate_snudda(args['path'], args['out'], ref_tv=ref_tv)
    
    '''
    simulate_transfered_model(  args['path'], 
                                args['out'], 
                                int(args['mid']),  
                                upgrade_params=args['upgrade'],
                                print_psection=int(args['psprint']),
                                ref_tv=ref_tv)'''
    
    
    
    
    
    
    
