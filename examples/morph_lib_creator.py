
'''
morphological helper functions for app.py

import to app.py and use 

morph_with_none, sec_coordinates, stem2plot, sec2stem = morph_lib_creator.create() 

to create needed libraries of default morphology.
'''

import numpy as np
import pickle
import json


def map_sec2stem(morphology):
    '''create sec->stem dict'''
    
    sec2stem = {}
    for stem in morphology['stem']:
        
        for sec in morphology['stem'][stem]:
            sec2stem[str(sec)] = stem
    return sec2stem
    
    
    

def get_midpoint(sec, morphology, return_half_len=False):
    
    # start point
    point       = morphology['sec'][sec][0]
    parent      = morphology['points'][point]['parent']
    line        = morphology['points'][parent]
    start_point = [ float(line['x']),
                    float(line['y']), 
                    float(line['z']) ]
    
    # calc total section length
    L = []
    l = 0
    for point in morphology['sec'][sec]:
        end_point_line  = morphology['points'][point]
        end_point       = [ float(end_point_line['x']), 
                            float(end_point_line['y']), 
                            float(end_point_line['z']) ]
        
        diff    = np.subtract(start_point, end_point)
        l      += np.sqrt(diff.dot(diff)) 
        L.append(l)
        
        start_point = end_point
    
    # half lenght
    lh          = l/2.0
    
    if return_half_len:
        return lh
    
    # find two closest points 
    for d,dist in enumerate(L):
        if dist > lh:
            
            # choose closet point
            if d == 0:
                line    = morphology['points'][ morphology['sec'][sec][d] ]
            elif np.abs(lh-L[d]) < np.abs(lh-L[d-1]):
                line    = morphology['points'][ morphology['sec'][sec][d] ]
            else:
                line    = morphology['points'][ morphology['sec'][sec][d-1] ]
            return [    float(line['x']),
                        float(line['y']), 
                        float(line['z']) ]
                        
 

def get_branching_points(swc_file):
    ''' check if branching points (parent to more than one point) '''
    
    bp  = {'all':{}, 'branching':{}}
    
    with open(swc_file) as f:
        
        for line in f.readlines(): # for line in file...  
            if line[0] in ['#', ' ', '\n', '\t']: continue
            l = line.split() 
            if l[6] in bp['all']:
                bp['branching'][l[6]] = True
            else:
                bp['all'][l[6]] = True
    
    return bp
    


def read_morph_swc(swc_file, bp, ntypes=[]):
    ''' extract morphological data from swc file.
        
        Aug 8 -24 update (before axon was ignored):
        by default, both axon and all dendrite types are extracted.
            In order to only extract one type, use the ntype argument, 
            e.g. ntype=[2] for axon, and ntype=[3,4] for basal and apical dendrites'''
    
    morphology      = {'stem':{}, 'sec':{}, 'points':{}, 'sortlist':[]}
    morph_with_none = {'x':[], 'y':[], 'z':[], 'r':[] }
    stem2plot       = {}
    sec_coordinates = {}
    
    prev_point      = '0'
    
    with open(swc_file) as f:    
        for line in f.readlines(): 
            
            if line[0] in ['#']: continue   # , ' ' removed dec -24 (RL) 
                
            l = line.split()
            
            if not len(l) == 7:
                continue # dec -24
            
            # commented Aug 8 -24 (RL)
            # not sure if this is needed for some reason? to get the midpoint of the last section? What is the midpoint used for?
            #   added this command to the end of the function
            '''
            if l[1] == '2': 
                sec_coordinates[sec] = get_midpoint(sec, morphology)
                break
            '''
            # added Aug 8 -24 (RL)
            if l[1] == '1':
                # always store the soma
                pass
            elif len(ntypes):
                # only save specific neurite type(s)
                if int(l[1]) not in ntypes:
                    continue
            
            morphology['points'][ l[0] ] = {  
                                    'type'      :   l[1],
                                    'x'         :   l[2],
                                    'y'         :   l[3],
                                    'z'         :   l[4],
                                    'r'         :   l[5],
                                    'parent'    :   l[6]   
                                            }
                                            
            morphology['sortlist'].append(l[0])
            
            if l[6] == '-1':
                sec =0
                stem=0
                morphology['sec'][ sec ] = []
                morphology['stem'][ stem ] = [sec]
                stem2plot[stem]  = {'x':[], 'y':[], 'z':[], 'r':[], 'sec':[]}
            elif l[6] != prev_point:
                # get midpoint coordinates of previous section
                sec_coordinates[sec] = get_midpoint(sec, morphology)
                # update sec
                sec += 1
                if l[6] == '1':
                    stem += 1
                    morphology['stem'][ stem ] = [sec]
                    stem2plot[stem]  = {'x':[], 'y':[], 'z':[], 'r':[], 'sec':[]}
                else:
                    morphology['stem'][ stem ].append( sec )
                morphology['sec'][ sec ] = [ l[0] ]
                # add None to not connect end point with next start point 
                # and add parent as start of next
                for xx in ['x', 'y', 'z', 'r']:
                    morph_with_none[xx].append( None )
                    morph_with_none[xx].append( morphology['points'][l[6]][xx] )
                    stem2plot[stem][xx].append( None )
                    stem2plot[stem][xx].append( morphology['points'][l[6]][xx] )
                stem2plot[stem]['sec'].append( 'none' )
                stem2plot[stem]['sec'].append( 'branching' )
                
                # added Nov -24 (since sections were missing from tree)
                if l[0] in bp['branching']:
                    
                    # first and last point of section!
                    
                    # interpolate midpoint from parent sec and current. 
                    sec_coordinates[sec] = [(float(morphology['points'][l[6]]['x'])+float(l[2]))/2,
                                            (float(morphology['points'][l[6]]['y'])+float(l[3]))/2,
                                            (float(morphology['points'][l[6]]['z'])+float(l[4]))/2]
                    # increase sec count and add to stem
                    sec += 1
                    morphology['stem'][ stem ].append( sec )
                    # start new sec list and add id
                    morphology['sec'][ sec ] = [ l[0] ]
                    # add None to not connect end point with next start point 
                    #   and add parent (l[6]) as start of next (copy from line ~168-174)
                    #   TODO: move to function so not repeating same code
                    for xx in ['x', 'y', 'z', 'r']:
                        morph_with_none[xx].append( None )
                        morph_with_none[xx].append( morphology['points'][l[6]][xx] )
                        stem2plot[stem][xx].append( None )
                        stem2plot[stem][xx].append( morphology['points'][l[6]][xx] )
                    stem2plot[stem]['sec'].append( 'none' )
                    stem2plot[stem]['sec'].append( 'branching' )
                    
            else:
                morphology['sec'][ sec ].append( l[0] )
                if l[0] in bp['branching']:
                    # get midpoint coordinates of previous section
                    sec_coordinates[sec] = get_midpoint(sec, morphology)
                    # update sec
                    sec += 1
                    morphology['sec'][ sec ] = []
                    morphology['stem'][ stem ].append( sec )
            
            # add point
            for i,xx in enumerate(['x', 'y', 'z', 'r']):
                morph_with_none[xx].append( l[i+2] )
                stem2plot[stem][xx].append( l[i+2] )
            stem2plot[stem]['sec'].append(  'sec:'+str(sec) )    
            prev_point = l[0] 
    
    if len(sec_coordinates):
        # Aug. 8 -24 (RL)
        sec_coordinates[sec] = get_midpoint(sec, morphology)
    else:
        print('NO POINT OF TYPE:', ntypes)
    
    return [morphology, morph_with_none, sec_coordinates, stem2plot]






def create(swc_file='../Neuron/morphologies/WT-dMSN_P270-20_1.02_SGA1-m24.swc', ntypes=[]):
    '''
    master function for reading morphological data (in swc format) into dicts
    '''
    
    #check_n_somapoints(swc_file)
    
    bp = get_branching_points(swc_file)
    morphology, morph_with_none, sec_coordinates, stem2plot = read_morph_swc(swc_file, bp, ntypes=ntypes)
    sec2stem = map_sec2stem(morphology)
    
    return [morph_with_none, sec_coordinates, stem2plot, sec2stem, morphology]


def check_n_somapoints(swc_file):
    n_somapoints = 0
    with open(swc_file) as f:  
        for line in f.readlines(): 
            
            if line[0] in ['#']: continue
            
            l = line.split()
            
            if l[1] == '1':
                n_somapoints += 1
    if not n_somapoints == 1:
        raise Exception(f'The soma must have 1 point, but has {n_somapoints}')
            


def get_subtree(P, morphology):
    ''' 
    return subtree of P
    '''
    
    subtree = [P]
    
    # get index of P in sortlist
    index = morphology['sortlist'].index(P)
    
    # loop over points downstream of index and check if parents in subtree. else brake
    for point in morphology['sortlist'][index+1:]:
        parent = morphology['points'][point]['parent']
        if parent in subtree:
            subtree.append(point)
        else: return subtree
    
    return subtree


    

def get_morph_stats(morphology):
    # TODO: this is very slow for large tree structures - reimplement
    '''
    calculates:
    - number of end point from node
    - total length of subtree from node
    - maximal length of subtree from node
    TODO:
    - there's probably some smarter way of building subtrees
    - sum Ra soma for each model
    '''
    
    print(len(morphology['sec']))
    
    # get subtree of (all?) sec
    morphology['subtree'] = {}
    for i, sec in enumerate(morphology['sec']):
        print(i)
        # first point of each stem (each point in stem have same subtree downstream of branching point)
        P = morphology['sec'][ sec ] [0]
        
        # get subtree of point
        morphology['subtree'][ sec ] = get_subtree(P, morphology)
    
    # calc subtree statistics 
    #       -number of terminal branches
    #       -total distance of subtree
    #       -maximal distance to end point
    morphology['stat']    = {}
    print(len(morphology['subtree']))
    for i,sec in enumerate(morphology['subtree']):
        subtree = morphology['subtree'][ sec ]
        
        print(i)
        
        endpoints   = []
        prev_comp   = morphology['points'][subtree[0]]['parent']
        Ltot        = 0
        accumulated = {'all':{prev_comp:0}, 'end':[]}
        
        
        for point in subtree:
            
            parent = morphology['points'][point]['parent']
        
            # check if endpoint
            if not parent == prev_comp:
                endpoints.append(parent)
                accumulated['end'].append( accumulated['all'][prev_comp] )
            
            # calc length and update total and accumulated length
            inner = 0
            for xx in ['x', 'y', 'z']:
                # sign/order doesn't matter since squared (absolute coordinates)
                inner += np.square(     float(morphology['points'][point][xx]) - \
                                        float(morphology['points'][parent][xx]) 
                                        )
            dist  = np.sqrt( inner )
            
            Ltot += dist
            accumulated['all'][point] = dist + accumulated['all'][parent]
            
            prev_comp = point
            
        # last point is also an endpoint
        endpoints.append(point)
        accumulated['end'].append( accumulated['all'][point] )
    
        
        # terminal branches
        N_endpoints = len(endpoints)
        
        # total distance
        section_half_len    = get_midpoint(sec, morphology, return_half_len=True)
        total_distance      = Ltot - section_half_len
        
        # maximal distance to end point
        max_len2endpoint    = max( accumulated['end'] ) - section_half_len
        
        
        # add to stat
        morphology['stat'][sec] = { 'N_endpoints'       :   N_endpoints, 
                                    'total_distance'    :   total_distance,
                                    'max_len2endpoint'  :   max_len2endpoint
                                    }
    
    return morphology
        

def calc_len(swc_file='../Neuron/morphologies/WT-dMSN_P270-20_1.02_SGA1-m24.swc', nid=None):
    '''
    calc the length of neurite type with id nid
    
    this assumes that the neurite type is connected to the root, and the root is the soma
    '''
    
    node_dict = {}
    
    with open(swc_file) as f:    
        for line in f.readlines(): 
            
            # keep comments?
            if line.strip()[0] == '#': 
                continue
                
            l = line.split()
            
            # right type?
            if int(l[0]) == 1:
                # the root
                d2r = 0
            elif int(l[1]) == nid:
                p = node_dict[l[6]]
                
                # calc dist
                inner = 0
                for xx, cid in zip(['x', 'y', 'z'], [2,3,4]):
                    # sign/order doesn't matter since squared (absolute coordinates)
                    inner += np.square( float(l[cid]) - float(p[xx]) )
                d2r = np.sqrt( inner ) + p['d2r']
                
                node_dict[l[6]]['has_child_node'] = 1
            else:
                # wrong type (perhaps all types should be extracted?)
                continue
            
            node_dict[l[0]] = {'x'          :   float(l[2]),
                               'y'          :   float(l[3]),
                               'z'          :   float(l[4]),
                               'r'          :   float(l[5]),
                               'parent'     :   l[6],
                               'd2r'        :   d2r}
                
    
    
    for k,node in node_dict.items():
        if not 'has_child_node' in node:
            node['has_child_node'] = 0
    
    return node_dict

def move_subtree(morphology, sec_num_donor=33, sec_num_acceptor=18, stem_num_donor=3, stem_num_acceptor=0):
    '''
    uses morphology dic created by create() to create a plot structure for vizualization
    of the branches involved in the move.
    
    TODO: fix hardcoded section range of subtree to be moved.
    '''
    
    morph_branch_select = { 'subtree':{ 'x':[],
                                        'y':[],
                                        'z':[]}, 
                            'base'   :{ 'x':[],
                                        'y':[],
                                        'z':[]},
                            'moved'  :{ 'x':[],
                                        'y':[],
                                        'z':[]}                    ,
                            }


    end_secs = [sec_num_donor, sec_num_acceptor]
    tag      = ['subtree', 'moved']
    
    # TODO: fix hardcoded sec range
    subtree_sec_range = list(range(34,38))
    
    # get endpoint of anchor section (where to attache subtree)
    for i,point in enumerate(end_secs):
        point1  = morphology['sec'][point][-1]
        parent  = morphology['points'][point1]['parent']
        for coordinate in ['x','y','z']:
            c = float(morphology['points'][parent][coordinate])
            morph_branch_select[tag[i]][coordinate].append(c) 
            
    for i,stem in enumerate([stem_num_donor,stem_num_acceptor]):
            
        # add parent coordinates as start
        sec     = morphology['stem'][stem][0]
        point1  = morphology['sec'][sec][0]
        parent  = morphology['points'][point1]['parent']
        for coordinate in ['x','y','z']:
            c = morphology['points'][parent][coordinate]
            morph_branch_select['base'][coordinate].append(c) 
        
        prev_point = 'soma'   
        
        # loop over sec in stem
        for sec in morphology['stem'][stem]:
            
            if not morphology['points'][morphology['sec'][sec][0]]['parent'] == prev_point and not prev_point == 'soma':
                # since first point in sec not last point in parent sec: add None to split trace
                point1  = morphology['sec'][sec][0]
                parent  = morphology['points'][point1]['parent']
                for coordinate in ['x','y','z']:
                    c = float(morphology['points'][parent][coordinate])
                    if sec in subtree_sec_range:
                        morph_branch_select['subtree'][coordinate].append(None) 
                        morph_branch_select['moved'][coordinate].append(None)
                        morph_branch_select['subtree'][coordinate].append(c) 
                    else: 
                        morph_branch_select['base'][coordinate].append(None)
                        morph_branch_select['base'][coordinate].append(c)
            
            if sec in subtree_sec_range: 
                # add to subtree and moved
                for point in morphology['sec'][sec]:
                    for coordinate in ['x','y','z']:
                        c = float(morphology['points'][point][coordinate])
                        morph_branch_select['subtree'][coordinate].append(c)
                        # shift to new location
                        new = float(morph_branch_select['moved'][coordinate][0])
                        old = float(morph_branch_select['subtree'][coordinate][0])
                        c_new = c - old + new
                        morph_branch_select['moved'][coordinate].append(c_new)
                        
                        
            else:
                for point in morphology['sec'][sec]:
                    for coordinate in ['x','y','z']:
                        c = morphology['points'][point][coordinate]
                        morph_branch_select['base'][coordinate].append(c) 
            
            prev_point = point
            
        for coordinate in ['x','y','z']:
            if sec in subtree_sec_range:
                morph_branch_select['subtree'][coordinate].append(None) 
                morph_branch_select['moved'][coordinate].append(None)
            else: 
                morph_branch_select['base'][coordinate].append(None)
    
    
    return morph_branch_select


 
def get_somatic_connections(morphology):
    # get all sections connecting sec to soma
    # TODO: funciton is not tested, and not used...
    
    somatic_connections = {}
    for sec in morphology['sec']:
        
        parent  = 100
        s2      = sec
        connection = [s2]
        
        while not parent == '1':
            # first point of current sec
            P = morphology['sec'][ s2 ] [0]
            
            # get parent sec
            # -point
            parent = morphology['points'][P][ 'parent' ]
            # -find sec
            for s2 in morphology['sec']:
                if parent in morphology['sec'][s2]:
                    break
            if s2 in somatic_connections:
                connection = connection + somatic_connections[s2]
                somatic_connections[sec] = connection
                break
                
            connection.append(s2)
    
    return somatic_connections
            
        
def renumber_neurites(swc_file, start_index, ntype, fname='re-numbered_neurite.swc'):
    
    first_of_type = -999
    new = ''
    with open(swc_file) as f:    
        for line in f.readlines(): 
            
            if line[0] in ['#']: 
                continue
                
            l = line.split()
            
            if not len(l) == 7:
                continue
            
            if not int(l[1]) == ntype:
                continue
            
            if first_of_type == -999:
                first_of_type = int(l[0])
            
            # update index and parent and add to new
            indx = int(l[0]) - first_of_type + start_index
            
            if l[-1] == '1':
                parent = l[-1] # soma, do nothing
            else:
                parent = int(l[-1]) - first_of_type + start_index
            
            new = f'{new}{indx} {l[1]} {l[2]} {l[3]} {l[4]} {l[5]} {parent}\n'
    
    with open(fname, "w") as text_file:
        print(new, file=text_file)
        

def read_morphology_subtypes(swc_file, type_list=[], sub_morph='', type_counter={}, keep_comments=False, return_node_count=False):
    '''
    Reads a morphology, line-by-line (if type in type_list). 
    Will also renumber nodes if the order of the types differs from the swc_file
        
        arguments:
        swc_file: path/to_file.swc (str)
        type_list (list): e.g [1, 3, 4]     (example, giving soma, and dendrites: basal=3 + apical=4)
        sub_morph (str): storing new morphology (can be used to append one type to another, from one or multiple files)
        type_counter (dict): used to keep track of the number of nodes of each type (also used to update indexing of nodes)
        keep_comments (bool): store comments in sub_morph
        return_node_count (bool): keep track of node-count from previous morphologies
        
    '''
    # TODO: separate nodes and comments into two strings so that comments can also be extracted from multiple files
    first_of_type = {}
    
    with open(swc_file) as f:    
        for line in f.readlines(): 
            
            # keep comments?
            if line.strip()[0] == '#': 
                if keep_comments:
                    # what if this is not at the head of the file?
                    sub_morph += line
                continue
                
            l = line.split()
            
            # right type?
            if int(l[1]) in type_list:
                
                if not l[1] in first_of_type:
                    # TODO: perhaps more elegant if first_of_type[l[1]] could be added to start_index directly...
                    first_of_type[l[1]] = int(l[0])
                    type_counter[l[1]] = 0  # used to count how many nodes of each type we have (to now at what index to start next type)
                    start_index = sum([n for tkey, n in type_counter.items()]) + 1
                    print(l[1], start_index, type_counter)
                
                # renumber node so that each row have higher id than the one before
                if len(type_counter)==1:
                    # if this is the first type we should not have to update parent and index
                    sub_morph += line
                else:
                    # update index and parent (remove id of first node and append new start index)
                    indx = int(l[0]) - first_of_type[l[1]] + start_index
                    
                    if l[-1] == '1':
                        parent = l[-1] # soma, do nothing
                    else:
                        parent = int(l[-1]) - first_of_type[l[1]] + start_index
                    
                    sub_morph += f'{indx} {l[1]} {l[2]} {l[3]} {l[4]} {l[5]} {parent}\n'
                    
                # increment type counter
                type_counter[l[1]] += 1
                
    if return_node_count:     
        return sub_morph, sum([n for tkey, n in type_counter.items()])
    else:
        return sub_morph
    
    
def verify_indexing():
    # loop over morphology checking that ids are consecutively increased by 1 per row
    # TODO implement
    pass
    
