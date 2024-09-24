"""
The cell definitions
"""

import neuron as nrn
from neuron import h
import numpy as np
import json

h.load_file('import3d.hoc')

#nrn.load_mechanisms('mechanisms')



FLOAT_FORMAT = '%.17g'





class Cell:
    def __init__(self, gid, name):
        self.name = name
        self.gid = gid
    def _set_spike_detection(self):
        # spike detection
        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)

    def __repr__(self):
        return "{}[{}]".format(self.name, self.gid)

    def _set_morphology_from_swc(self):
        """Load morphology"""
        morphology_loader = h.Import3d_SWC_read()
        morphology_loader.quiet = 2
        morphology_loader.input(str(self.morphology_path))
        morph_imp = h.Import3d_GUI(morphology_loader, 0)
        morph_imp.instantiate(self)

    def _create_sectionlists(self, replace_axon=True):

        # soma
        self.somalist = h.SectionList()
        for sec in h.allsec():
            if sec.name().find('soma') >= 0 and sec.name().find('{}[{}]'.format(self.name, self.gid)) >= 0:
                self.somalist.append(sec=sec)
        self.soma = list(self.somalist)[0]

        # dendrite
        self.dendlist = h.SectionList()
        for sec in self.soma.wholetree(): # why wholetree here???
            if sec.name().find('dend') >= 0 and sec.name().find('{}[{}]'.format(self.name, self.gid)) >= 0:
                self.dendlist.append(sec=sec)
        # axon
        if replace_axon:
            # self.axonlist will be created by the below method
            self._create_AIS()
        else:
            self.axonlist = h.SectionList()
            for sec in self.soma.wholetree():
                if sec.name().find('axon') >= 0 and sec.name().find('{}[{}]'.format(self.name, self.gid)) >= 0:
                    self.axonlist.append(sec=sec)
        # all
        self.allsecnames = []
        self.allseclist  = h.SectionList()
        for sec in self.soma.wholetree():
            if sec.name().find('{}[{}]'.format(self.name, self.gid)) >= 0:
                self.allsecnames.append(sec.name())
                self.allseclist.append(sec=sec)

        self.name2seclist = {'soma': self.somalist, 'basal': self.dendlist, 'axon': self.axonlist, 'all':self.allseclist}

    def _create_AIS(self):
        """Replica of "Replace axon" in:
            https://bluepyopt.readthedocs.io/en/latest/_modules/bluepyopt/ephys/morphologies.html#Morphology
        """

        temp = []
        #c = 0
        for sec in h.allsec():
            if sec.name().find('axon') >= 0 and sec.name().find('{}[{}]'.format(self.name, self.gid)) >= 0:
                #print(sec.name(), sec.diam,  sec.n3d())
                #h.psection(sec=sec)
                #for i in range(sec.n3d()):
                #    print('{:.6f}, {:.6f}, {:.6f}, {:.6f}'.format(sec.x3d(i), sec.y3d(i), sec.z3d(i), sec.diam3d(i)))
                temp.append(sec)
                #c += 1
                #if c > 0:break
                sec.nseg = 1 + 2*int(sec.L/40)  # set nseg of the axon. this is needed to get the same diameter as BPO versions of this script 

        # specify diameter based on BPO
        if len(temp) == 0:
            ais_diams = [1, 1]
        elif len(temp) == 1:
            ais_diams = [temp[0].diam, temp[0].diam]
        else:
            ais_diams = [temp[0].diam, temp[0].diam]
            # Define origin of distance function
            h.distance(0, 0.5, sec=self.soma)

            for sec in h.allsec():
                if sec.name().find('axon') >= 0 and sec.name().find(f'{self.name}[{self.gid}]') >= 0:
                    # If distance to soma is larger than 60, store diameter
                    d = h.distance(1, 0.5, sec=sec)
                    if d > 60:
                        ais_diams[1] = sec.diam
                        break

        # delete old axon
        for section in temp:
            h.delete_section(sec=section)

        # Create new axon sections
        a0 = h.Section(name='{}[{}].axon[0]'.format(self.name, self.gid))
        a1 = h.Section(name='{}[{}].axon[1]'.format(self.name, self.gid))

        # connect axon sections to soma and each-other
        a0.connect(self.soma)
        a1.connect(a0)

        # populate axon list
        self.axonlist = h.SectionList()
        for sec in self.soma.wholetree():
            if sec.name().find('axon') >= 0 and sec.name().find('{}[{}]'.format(self.name, self.gid)) >= 0:
                #print('adding sec: {} to axon!'.format(sec.name()))
                self.axonlist.append(sec=sec)

        # set axon params
        for index, section in enumerate([a0, a1]):
            section.nseg = 1
            section.L = 30
            section.diam = ais_diams[index]

        # this line is needed to prevent garbage collection of axon
        self.axon = [a0, a1]

    def _set_nsegs(self, nseg_axon=1):
        """ def seg/sec.  use default nseg for soma (1?)"""
        for sec in self.dendlist:
            sec.nseg = 2 * int(sec.L / 40.0) + 1
        for sec in self.axonlist:
            if nseg_axon > 0:
                sec.nseg = nseg_axon  # two segments in axon initial segment for spn's in Lindroos 2020 1 for bpo_models with replaced axon
            else:
                # use default number of segments/section
                sec.nseg = 2 * int(sec.L / 40.0) + 1

# ======================= the ball and stick class ==================================================
class BallAndStick(Cell):
    def __init__(self, gid):
        super().__init__(gid, "NGF_BallAndStick")
        self._setup_morphology()
        self.all = self.soma.wholetree()
        self._setup_biophysics()

        self._set_spike_detection()

    def _setup_morphology(self):
        self.soma = h.Section(name="soma", cell=self)
        self.dend = h.Section(name="dend", cell=self)
        self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 12.6157
        self.dend.L = 200
        self.dend.diam = 1

    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
        self.soma.insert("hh")
        for seg in self.soma:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003  # Leak conductance in S/cm2
            seg.hh.el = -54.3  # Reversal potential in mV
        # Insert passive current in the dendrite
        self.dend.insert("pas")
        for seg in self.dend:
            seg.pas.g = 0.001  # Passive conductance in S/cm2
            seg.pas.e = -65  # Leak reversal potential mV



        
    


# ======================= the BPO cell class ==================================================

class Bpo_cell(Cell):
    def __init__(self, params,
                 morphology=None,
                 best_models=None,
                 cell_type='cell',
                 bmi=0,
                 gid=0,
                 param_key=None,
                 replace_axon=True,
                 region_cadyn_dict={},
                 allow_non_uniform=True):
        super().__init__(gid, cell_type)
        self.morphology_path = morphology
        self._set_morphology_from_swc()

        self.bmi = bmi

        self._create_sectionlists(replace_axon=replace_axon)
        if replace_axon:
            nseg = 1
        else:
            nseg = 0
        self._set_nsegs(nseg_axon=nseg)

        self._set_spike_detection()

        # insert mechanisms and set values
        with open(params) as file:
            if param_key:
                param_list = json.load(file)[param_key]
            else:
                param_list = json.load(file)
                
        if best_models:
            with open(best_models) as file:
                best_model = json.load(file)[self.bmi]
        else:
            best_model = []

        if 'global' in param_list:
            for par in param_list['global'].keys():
                cmd = f'h.{par} = param_list["global"]["{par}"]'
                exec(cmd)
        
        for region, dynamics in region_cadyn_dict.items():
            for sec in self.name2seclist[region]:
                for dyn in dynamics:
                    sec.insert(dyn)
        
        for sec_list in ['soma', 'axon', 'basal', 'all']:
            item = param_list[sec_list]
            
            ns = []
            for mech, params in item.items():
                # insert channel
                if mech == 'neuron_specific':
                    ns = params
                else:
                    for sec in self.name2seclist[sec_list]:
                        sec.insert(mech)

                        # set value
                        for var, val in params.items(): 
                            
                            if 'bounds' in val:
                                # get from best_models
                                if not len(best_model):
                                    raise Exception('Error: best model is empty (or not added). Needed for parameter: {}'.format(var))
                                elif not '{}_{}.{}'.format(var, mech, sec_list) in best_model:
                                    raise Exception('Error: key ({}_{}.{}) not in best_model'.format(var, mech, sec_list))
                                value = best_model['{}_{}.{}'.format(var, mech, sec_list)]
                            else:
                                value = val['value']

                            for seg in sec:
                                if val['dist_type'] == 'uniform':
                                    cmd = 'seg.{}.{} = {}'.format(mech, var, value)
                                    exec(cmd)
                                else:
                                    if allow_non_uniform:
                                        # set soma(0) as reference section (as default BPO)
                                        h.distance(0, 0, sec=self.soma) # the second arg is the location in the soma
                                        # calc distance
                                        distance = h.distance(1, seg.x, sec=sec)
                                        import math
                                        from math import exp
                                        v = eval(val['dist_type'].format(distance=distance, value=value))
                                        cmd = 'seg.{}.{} = {}'.format(mech, var, v)
                                    else:
                                        cmd = 'seg.{}.{} = {}'.format(mech, var, value) # this string gives uniform values (in accordance with Alex model
                                    exec(cmd)
                if len(ns):
                    for sec in self.name2seclist[sec_list]:

                        # set value
                        # assuming uniform distribution for now
                        for var, val in ns.items():
                            if 'bounds' in val:
                                # get from best_models
                                if not len(best_model):
                                    raise Exception('Error: best model is not added. Needed for parameter: {}'.format(var))
                                elif not '{}.{}'.format(var, sec_list) in best_model:
                                    raise Exception('Error: key ({}.{}) not in best_model'.format(var, sec_list))
                                value = best_model['{}.{}'.format(var, sec_list)]
                            else:
                                value = val['value']

                            cmd = 'sec.{} = {}'.format(var, value)
                            exec(cmd)
