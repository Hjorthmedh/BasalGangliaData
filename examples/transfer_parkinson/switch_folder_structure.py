import os
import glob
import shutil
import sys

sys.path.append("../../tools")

def transfer_and_adapt_pd_model():
    for condition in ['PD0','PD1','PD2','PD3']:
        for subtype in ['dspn','ispn']:
            #Transfer swc files from 1,2,3...-format to vargroup-folder structure
            #e.g. dspn/str-dspn-e150917_c6_D1-m21-6-DE/morphology/21-6-DE-cor-rep-ax-res3-var0.swc
            morph_source = os.path.join('..', '..', 'Parkinson', '20220225',
                                        condition,'neurons','striatum', subtype)
            destination_base_1 = os.path.join('..', '..', 'Parkinson', '20220930_1')
            destination_subtype_path_1 = os.path.join(destination_base_1,condition, 'neurons', 'striatum', subtype)
            match_and_copy_morphs(morph_source, destination_subtype_path_1)

            #Using destination_subtype_path_1 as morph source
            #and bgmod folder as model source
            # transfer to destination_subtype_path_2
            destination_base_2 = os.path.join('..', '..', 'Parkinson', '20220930_2')
            destination_subtype_path_2 = os.path.join(destination_base_2, condition, 'neurons', 'striatum', subtype)
            #newModel = 'str-dspn-e150602_c1_D1-mWT-0728MSN01-pd2-v20220114'
            model_source = os.path.join('..', '..', '..', 'bgmod', 'models', 'optim', 'parkinsonian')
            bgmod_folders = os.listdir(model_source)

            # Both pd0 ("") and pd2 ("-pd2") files are in this "-pd2" folder
            bgmod_folder_paths = glob.glob(os.path.join(model_source, 'str-'+subtype+'*-pd2*'))

            #condition_model is only for the files
            if condition in ['PD1','PD2','PD3']:
                condition_model = '-pd2'
            else:
                condition_model = ''
            for bgmod_folder_path in bgmod_folder_paths:
                bgmod_folder = os.path.split(bgmod_folder_path)[1]
                destination = bgmod_folder[0:-14]
                destination_path_1 = os.path.join(destination_subtype_path_1, destination)
                destination_path_2 = os.path.join(destination_subtype_path_2, destination)
                if not os.path.exists(destination_path_2):
                    os.makedirs(destination_path_2)

                # Transfer mechanisms
                from transfer.mechanisms import transfer_mechanisms
                transfer_mechanisms(source=bgmod_folder_path, destination=destination_path_2)

                # Transfer parameters
                from transfer.parameters import transfer_parameters
                transfer_parameters(source=bgmod_folder_path,
                                    destination=destination_path_2,
                                    selected=False,
                                    condition=condition_model)
                from clean.math_exp import rename_math_exp
                parapth=os.path.join(destination_path_2,'parameters.json')
                rename_math_exp(parapth,destination_path_2)

                # Transfer selected models from val_models.json
                from transfer.selected_models import transfer_selected_models
                transfer_selected_models(source=bgmod_folder_path, destination=destination_path_2)

                # Transfer morphologies
                from transfer.morphology import transfer_morphologies
                transfer_morphologies(source=destination_path_1,
                                      destination=destination_path_2,
                                      selected=False)

                # Create the meta.json which combines all information on the model
                from meta.create_meta import write_meta
                write_meta(directory=destination_path_2, selected=False)


def match_and_copy_morphs(morph_source,destination_subtype_path):
    folders = os.listdir(morph_source)
    for folder in folders:
        swc_file_path = glob.glob(os.path.join(morph_source, folder, '*.swc'))
        swc_file_path = swc_file_path[0]
        swc_file_name = os.listdir(os.path.join(morph_source, folder))
        swc_file_name = swc_file_name[0]
        if swc_file_name[0:-5] == '21-6-DE-cor-rep-ax-res3-var':
            destination = 'str-dspn-e150917_c6_D1-m21-6-DE'
        elif swc_file_name[0:-5] == 'WT-0728MSN01-cor-rep-ax-res3-var':
            destination = 'str-dspn-e150602_c1_D1-mWT-0728MSN01'
        elif swc_file_name[0:-5] == 'WT-1215MSN03-cor-rep-ax-res3-var':
            destination = 'str-dspn-e150917_c9_d1-mWT-1215MSN03'
        elif swc_file_name[0:-5] == 'WT-P270-20-15ak-cor-res3-var':
            destination = 'str-dspn-e150917_c10_D1-mWT-P270-20'
        elif swc_file_name[0:-5] == '46-3-DE-cor-rep-ax-res3-var':
            destination = 'str-ispn-e160118_c10_D2-m46-3-DE'
        elif swc_file_name[0:-5] == '51-5-DE-cor-rep-ax-res3-var':
            destination = 'str-ispn-e150908_c4_D2-m51-5-DE'
        elif swc_file_name[0:-5] == 'WT-MSN1-cor-rep-ax-res3-var':
            destination = 'str-ispn-e150917_c11_D2-mWT-MSN1'
        elif swc_file_name[0:-5] == 'WT-P270-09-15ak-cor-res3-var':
            destination = 'str-ispn-e151123_c1_D2-mWT-P270-09'
        else:
            raise Exception("The swc name could not be matched.")

        destination_path = os.path.join(destination_subtype_path, destination, 'morphology')
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        destination_file_path = os.path.join(destination_path, swc_file_name)
        shutil.copyfile(swc_file_path, destination_file_path)

if __name__ == "__main__":
    transfer_and_adapt_pd_model()