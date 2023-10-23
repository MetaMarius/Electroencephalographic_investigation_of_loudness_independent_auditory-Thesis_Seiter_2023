import slab
import os
import pathlib
from os import listdir
import mne
import pandas as pd
import numpy as np


def get_file_paths(root_path):
    root_path = root_path / 'data'
    participants = listdir(root_path)
    file_paths = {participant: [] for participant in participants}
    for participant in file_paths:
        folder_path = root_path / participant
        if os.path.exists(folder_path / 'slab_result_files'):
            path = folder_path / 'slab_result_files'
            file_paths[participant] = [path / f for f in listdir(path)]
        else:
            print("ERROR: No directory named 'slab_result_files'. The result files should be stored like this: root/data/participant_id/slab_result_files/result_file.txt")
            break
    return file_paths


def get_stage_results(root_path, stage='experiment'):
    file_paths = get_file_paths(root_path=root_path)
    stage_result_files = {participant: [] for participant in file_paths}
    for participants in file_paths:
        for file in file_paths[participants]:
            if stage == 'experiment':
                is_experiment = slab.ResultsFile.read_file(file, tag='stage') == 'experiment'
                if is_experiment:
                    stage_result_files[participants].append(slab.ResultsFile.read_file(file))
            elif stage == 'test':
                is_experiment = slab.ResultsFile.read_file(file, tag='stage') == 'test'
                if is_experiment:
                    stage_result_files[participants].append(slab.ResultsFile.read_file(file))
            elif stage == 'training':
                is_experiment = slab.ResultsFile.read_file(file, tag='stage') == 'training'
                if is_experiment:
                    stage_result_files[participants].append(slab.ResultsFile.read_file(file))
    return stage_result_files


def get_trialsequence_data(result_files):
    trialsequence_data = {participant: [] for participant in result_files}
    for participant in result_files:
        for file in result_files[participant]:
            for dictionary in file:
                if 'sequence' in dictionary:
                    trialsequence_data[participant].append(dictionary['sequence']['data'])
    return trialsequence_data


def concatenate_trialsequence_data(trialsequence_data):
    trialsequence_data_conc = {participant: [] for participant in trialsequence_data}
    for participant in trialsequence_data:
        for round in trialsequence_data[participant]:
            # uso_ids_con[participant].append([{'sound_id': None}])
            for index in round:
                trialsequence_data_conc[participant].append(index)
    return trialsequence_data_conc


def create_trialsequence_data_dictionary(root_path):
    stage_result_files = get_stage_results(root_path=root_path)
    trialsequence_data = get_trialsequence_data(result_files=stage_result_files)
    trialsequence_data_conc = concatenate_trialsequence_data(trialsequence_data=trialsequence_data)
    return trialsequence_data_conc


def get_keys_from_value(dict, val):
    return [k for k, v in dict.items() if v == val][0]


def create_metadata_frame_from_raw_annotations(raw):
    # get event array from raw
    events = mne.events_from_annotations(raw)
    metadata = pd.DataFrame(events[0])
    # adjust data frame
    metadata.rename(columns={0: 'Sample'}, inplace=True)
    metadata.rename(columns={2: 'Event_ID'}, inplace=True)
    metadata.drop(1, axis=1, inplace=True)
    # dictionary key rename because annotation descriptions are bad in our case
    events[1]['New Segment'] = events[1].pop('New Segment/')
    events[1]['Distance 1'] = events[1].pop('Stimulus/S  1')
    events[1]['Distance 2'] = events[1].pop('Stimulus/S  2')
    events[1]['Distance 3'] = events[1].pop('Stimulus/S  3')
    events[1]['Distance 4'] = events[1].pop('Stimulus/S  4')
    events[1]['Distance 5'] = events[1].pop('Stimulus/S  5')
    events[1]['Deviant'] = events[1].pop('Stimulus/S  6')
    events[1]['Button Press'] = events[1].pop('Stimulus/S  7')
    #
    for event_id in events[1].values():
        metadata.loc[metadata['Event_ID'] == event_id, 'Event_description'] = get_keys_from_value(events[1], event_id)
    return metadata


def attach_uso_id_to_metadata(metadata, root_path, id):
    uso_id_conc = create_trialsequence_data_dictionary(root_path)
    metadata['USO_ID'] = np.nan
    uso_id_conc_idx = 0
    for event_idx, event in enumerate(metadata['Event_description']):
        if event == 'Deviant':
            uso_id_conc_idx += 1
            continue
        elif event == 'Button Press':
            continue
        elif event == 'New Segment':
            continue
        else:
            metadata.loc[event_idx, 'USO_ID'] = int(uso_id_conc[id][uso_id_conc_idx][0]['sound_id'])
            uso_id_conc_idx += 1
    return metadata


uso_csv = pd.read_csv('C:/Users/ms26cize/USO_Bachelor_Thesis/analysis/data/stimuli/USO_features.csv')


def attach_uso_csv_to_metadata(metadata):
    # path = input('Path to USO csv: ')
    uso_csv = pd.read_csv('C:/Users/ms26cize/USO_Bachelor_Thesis/analysis/data/stimuli/USO_features.csv')
    uso_features = list(uso_csv.columns)
    uso_features.remove('Unnamed: 0.1')
    uso_features.remove('Unnamed: 0')
    uso_features.remove('USO_id')
    uso_features.remove('dist_group')
    for idx, event in enumerate(metadata['Event_description']):
        event_description = metadata.loc[idx, 'Event_description']
        uso_id = metadata.loc[idx, 'USO_ID']
        for uso_feature in uso_features:
            if event_description == 'New Segment':
                metadata.loc[idx, uso_feature] = np.nan
            if event_description == 'Button Press':
                metadata.loc[idx, uso_feature] = np.nan
            if event_description == 'Distance 1':
                metadata.loc[idx, uso_feature] = pd.Series.mean(uso_csv.loc[
                    (uso_csv['USO_id'] == uso_id) & (uso_csv['dist_group'] == 1), uso_feature])
            if event_description == 'Distance 2':
                metadata.loc[idx, uso_feature] = pd.Series.mean(uso_csv.loc[
                    (uso_csv['USO_id'] == uso_id) & (uso_csv['dist_group'] == 2), uso_feature])
            if event_description == 'Distance 3':
                metadata.loc[idx, uso_feature] = pd.Series.mean(uso_csv.loc[
                    (uso_csv['USO_id'] == uso_id) & (uso_csv['dist_group'] == 3), uso_feature])
            if event_description == 'Distance 4':
                metadata.loc[idx, uso_feature] = pd.Series.mean(uso_csv.loc[
                    (uso_csv['USO_id'] == uso_id) & (uso_csv['dist_group'] == 4), uso_feature])
            if event_description == 'Distance 5':
                metadata.loc[idx, uso_feature] = pd.Series.mean(uso_csv.loc[
                    (uso_csv['USO_id'] == uso_id) & (uso_csv['dist_group'] == 5), uso_feature])
    return metadata


def create_metadata(raw, root_path, id):
    print('Create the data frame')
    metadata = create_metadata_frame_from_raw_annotations(raw=raw)
    print('Attaching USO IDs to metadata')
    metadata_with_uso_id = attach_uso_id_to_metadata(metadata=metadata, root_path=root_path, id=id)
    print('Attaching USO features to metadata')
    metadata_complete = attach_uso_csv_to_metadata(metadata=metadata_with_uso_id)
    return metadata_complete


