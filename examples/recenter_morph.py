
import os

def recenter(mfile, return_fname=False):

    recentered_morph = ''
    
    with open(mfile) as f:    
        for line in f.readlines():
            if line[0] in ['#', ' ']: 
                # if there's comments or empty rows before the actual values, simply add them as is
                recentered_morph += line
                continue
            
            l = line.split()
            if len(l) < 7:
                print(l)
            if l[6] == '-1':
                # this is the root of the tree (soma). This should be the first node (and might give errors if it is not)
                # We want to subtract the x,y,z-values from this point for all points in the file
                x0 = float(l[2])
                y0 = float(l[3])
                z0 = float(l[4])
                
                print('-checking if morphology is centered...')
                if x0 == 0 and y0 == 0 and z0 == 0:
                    # this morphology is already centered
                    print('-> the morphology is already centered')
                    return None
                print('-> the morphology is NOT centered: centering...')
                newline = ''
            else:
                newline = '\n'
            
            # now all we have to do is subtract these values from all points (values are given in absolute coordinates)
            recentered_morph += '{}{} {} {:0.3f} {:0.3f} {:0.3f} {} {}'.format(newline, l[0], l[1], 
                                                                        float(l[2])-x0,
                                                                        float(l[3])-y0,
                                                                        float(l[4])-z0,
                                                                        l[5], l[6])
    # write to file
    file_name, extension = os.path.splitext(mfile)
    new_file_name = f'{file_name}_centered.swc'
    
    print(f'-> writing centered morphology to file:\n\t{new_file_name}')
    with open(new_file_name, 'w') as f:
        f.write(recentered_morph)
    
    print(f'-> renaming old swc file to :\n\t{file_name}.org')
    os.rename(mfile, f'{file_name}.org')
    
    if return_fname:
        return new_file_name


    
# plot
def compare_by_plotting_morphologies(morph_list):
    import morph_lib_creator
    import matplotlib.pyplot as plt
    import numpy as np
    fig,ax = plt.subplots(1,1)
    for swc_file in morph_list:
        morph_with_none, a, b, c, d = morph_lib_creator.create(swc_file)
        # get coordinates
        x = np.array(morph_with_none['x']).astype(float)
        y = np.array(morph_with_none['y']).astype(float)
        z = np.array(morph_with_none['z']).astype(float)
        # plot dendrites
        ax.plot(x,y)
    plt.axis('off')
    plt.show()



if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(description='simple script for centering of a morphology')
    parser.add_argument('-m','--morphology_file_path', help='full path to the morphology file to center', required=True)

    args, ip = parser.parse_known_args()

    mfile = args.morphology_file_path
    
    new_file_name = recenter(mfile, return_fname=True)
    
    if new_file_name:
        compare_by_plotting_morphologies([mfile, new_file_name])

