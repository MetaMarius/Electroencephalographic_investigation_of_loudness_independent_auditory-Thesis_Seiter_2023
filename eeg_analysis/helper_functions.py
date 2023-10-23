from os import listdir
from scipy.signal import find_peaks
import numpy as np
import pandas as pd
import mne
import math
from scipy.integrate import trapz


def get_ids(subset=None):
    df = pd.read_excel('C:/USO_Project/eeg_analysis/participant_selection.xlsx')
    if subset is None:
        ids = df['all participants'].tolist()
    elif subset == 'good':
        ids = df['good participants'].tolist()
    elif subset == 'bad':
        ids = df['bad participants '].tolist()
    elif subset == 'new good':
        ids = df['new good'].tolist()
    new_list = [item for item in ids if type(item) == str]
    return new_list


def read_epochs(ids, root_path='C:/USO_Project/eeg_preprocessing/data'):
    epochs = {subject: None for subject in ids}
    for subject in epochs:
        epochs[subject] = mne.read_epochs(f'{root_path}/{subject}/epochs/{subject}-epo.fif')
    return epochs


def read_evokeds(ids, sorting, root_path='C:/USO_Project/eeg_preprocessing/data'):
    if sorting == 'subjects':
        evokeds = {subject: [] for subject in ids}
        for subject in evokeds:
            evokeds[subject] = mne.read_evokeds(f'{root_path}/{subject}/evokeds/{subject}-ave.fif')
        return evokeds
    elif sorting == 'condition':
        evokeds = {}
        for subject in ids:
            evoked = mne.read_evokeds(f'{root_path}/{subject}/evokeds/{subject}-ave.fif')
            for condition in evoked:
                if condition.comment not in evokeds.keys():
                    evokeds[condition.comment] = [condition]
                else:
                    evokeds[condition.comment].append(condition)
        del evokeds['Button Press'], evokeds['Deviant']
        evokeds = dict(sorted(evokeds.items()))
        return evokeds


def read_evokeds_old(root, ids, how='per distance', averaged=False):
    evoked_files = list()
    for id in ids:
        evoked_files.append(root + '/data/'f'{id}/evokeds'f'/{id}-ave.fif')
    evokeds = [mne.read_evokeds(file) for file in evoked_files]

    if how == 'per distance':
        evoked_dict = dict()
        for subject in evokeds:
            for distance in subject:
                if distance.comment not in evoked_dict.keys():
                    evoked_dict[distance.comment] = [distance]
                else:
                    evoked_dict[distance.comment].append(distance)
                if distance.comment in ['Deviant', 'Button Press']:
                    del evoked_dict[distance.comment]
        if averaged is True:
            for distance in evoked_dict:
                evoked_dict[distance] = mne.grand_average(evoked_dict[distance])
        evoked_dict = {k: evoked_dict[k] for k in sorted(evoked_dict)}
        return evoked_dict

    if how == 'per distance and participant':
        evoked_dict = dict()
        for id in ids:
            for subject in evokeds:
                for distance in subject:
                    if id in distance.filename:
                        if distance.comment not in evoked_dict.keys():
                            evoked_dict[distance.comment] = {id: distance}
                        else:
                            evoked_dict[distance.comment].update({id: distance})
                        if distance.comment in ['Deviant', 'Button Press']:
                            del evoked_dict[distance.comment]
        evoked_dict = {k: evoked_dict[k] for k in sorted(evoked_dict)}
        return evoked_dict

    if how == 'per participant':
        evoked_dict = dict()
        for id in ids:
            for subject in evokeds:
                for distance in subject:
                    if id in distance.filename:
                        if id not in evoked_dict.keys():
                            evoked_dict[id] = [distance]
                        else:
                            evoked_dict[id].append(distance)
                        if distance.comment in ['Deviant', 'Button Press']:
                            evoked_dict[id].remove(distance)
        if averaged is True:
            for subject in evoked_dict:
                evoked_dict[subject] = mne.grand_average(evoked_dict[subject])
        return evoked_dict

    if how == 'per participant and distance':
        evoked_dict = dict()
        for id in ids:
            for subject in evokeds:
                for distance in subject:
                    if id in distance.filename:
                        if id not in evoked_dict.keys():
                            evoked_dict[id] = {distance.comment: distance}
                        else:
                            evoked_dict[id].update({distance.comment: distance})
                        if distance.comment in ['Deviant', 'Button Press']:
                            del evoked_dict[id][distance.comment]
        for id in evoked_dict:
            evoked_dict[id] = ({k: evoked_dict[id][k] for k in sorted(evoked_dict[id])})
        return evoked_dict


def apply_baseline(epochs, tmin=None, tmax=0):
    for participant in epochs:
        epochs[participant].apply_baseline((tmin, tmax))
    return epochs


def calculate_mean_amplitudes_of_evoked_per_distance(evokeds, ids, tmin, tmax, channels):

    cropped_evokeds = dict()
    for distance in evokeds:
        for participant in evokeds[distance]:
            if distance not in cropped_evokeds.keys():
                cropped_evokeds[distance] = [participant.copy().pick(channels).crop(tmin=tmin, tmax=tmax)]
            else:
                cropped_evokeds[distance].append(participant.copy().pick(channels).crop(tmin=tmin, tmax=tmax))

    mean_amplitudes_65_channels = dict()
    for distance in cropped_evokeds:
        for participant in cropped_evokeds[distance]:
            if distance not in mean_amplitudes_65_channels.keys():
                mean_amplitudes_65_channels[distance] = [participant.data.mean(axis=1) * 1e6]
            else:
                mean_amplitudes_65_channels[distance].append(participant.data.mean(axis=1) * 1e6)

    mean_amplitudes_avg = dict()
    for distance in mean_amplitudes_65_channels:
        for participant in mean_amplitudes_65_channels[distance]:
            if distance not in mean_amplitudes_avg.keys():
                mean_amplitudes_avg[distance] = [participant.mean(axis=0)]
            else:
                mean_amplitudes_avg[distance].append(participant.mean(axis=0))
    return mean_amplitudes_avg


def calculate_mean_amplitudes_of_epochs_per_distance(root, ids, tmin, tmax, channels):
    epochs = read_epochs(root=root, ids=ids)
    epochs_dict = {'Distance 1': [],
                   'Distance 2': [],
                   'Distance 3': [],
                   'Distance 4': [],
                   'Distance 5': []}
    for participant in epochs:
        for distance in epochs_dict:
            epochs_dict[distance].append(participant[distance])

    cropped_epochs = dict()
    for distance in epochs_dict:
        for participant in epochs_dict[distance]:
            if distance not in cropped_epochs.keys():
                cropped_epochs[distance] = [participant.pick(channels).crop(tmin=tmin, tmax=tmax)]
            else:
                cropped_epochs[distance].append(participant.pick(channels).crop(tmin=tmin, tmax=tmax))

    mean_amplitudes_GFP_65_channels = dict()
    for distance in cropped_epochs:
        for participant in cropped_epochs[distance]:
            for epoch in participant:
                if distance not in mean_amplitudes_GFP_65_channels.keys():
                    mean_amplitudes_GFP_65_channels[distance] = [epoch.mean(axis=1) * 1e6]
                else:
                    mean_amplitudes_GFP_65_channels[distance].append(epoch.mean(axis=1) * 1e6)

    mean_amplitudes_GFP_avg = dict()
    for distance in mean_amplitudes_GFP_65_channels:
        for epoch in mean_amplitudes_GFP_65_channels[distance]:
            if distance not in mean_amplitudes_GFP_avg.keys():
                mean_amplitudes_GFP_avg[distance] = [epoch.mean(axis=0)]
            else:
                mean_amplitudes_GFP_avg[distance].append(epoch.mean(axis=0))

    finished_dict = make_lists_in_dict_same_len(d=mean_amplitudes_GFP_avg)
    return finished_dict


def make_lists_in_dict_same_len(d):
    lengths = []
    for l in d:
        lengths.append(len(d[l]))
    max_len = max(lengths)
    for l in d:
        while len(d[l]) < max_len:
            d[l].append(np.nan)
    return d


def calculate_mean_amplitude_difference_waves(evokeds, tmin, tmax, channels):
    cropped_evokeds = dict()
    for distance in evokeds:
        for participant in evokeds[distance]:
            if distance not in cropped_evokeds.keys():
                cropped_evokeds[distance] = [participant.copy().pick(channels).crop(tmin=tmin, tmax=tmax)]
            else:
                cropped_evokeds[distance].append(participant.copy().pick(channels).crop(tmin=tmin, tmax=tmax))

    mean_amplitudes_GFP_65_channels = dict()
    for distance in cropped_evokeds:
        for participant in cropped_evokeds[distance]:
            if distance not in mean_amplitudes_GFP_65_channels.keys():
                mean_amplitudes_GFP_65_channels[distance] = [participant.data.mean(axis=1) * 1e6]
            else:
                mean_amplitudes_GFP_65_channels[distance].append(participant.data.mean(axis=1) * 1e6)

    mean_amplitudes_GFP_avg = dict()
    for distance in mean_amplitudes_GFP_65_channels:
        for participant in mean_amplitudes_GFP_65_channels[distance]:
            if distance not in mean_amplitudes_GFP_avg.keys():
                mean_amplitudes_GFP_avg[distance] = [participant.mean(axis=0)]
            else:
                mean_amplitudes_GFP_avg[distance].append(participant.mean(axis=0))
    return mean_amplitudes_GFP_avg


def find_peak_amplitude_in_evoked(evoked, tmin, tmax, channels):
    cropped = evoked.pick(channels).crop(tmin, tmax)
    peaks = cropped.get_peak()
    return peaks


def calculate_mean_amplitude_for_gfp(gfps, tmin, tmax):
    # convert times into indexes:
    tmin_sample = convert_time_into_sample(tmin)
    tmax_sample = convert_time_into_sample(tmax)
    mean_amplitudes = {'Distance 1': [],
                       'Distance 2': [],
                       'Distance 3': [],
                       'Distance 4': [],
                       'Distance 5': []}
    for distance in gfps:
        for subject in gfps[distance]:
            mean_amplitudes[distance].append(np.mean(subject[tmin_sample:tmax_sample]))
    return mean_amplitudes


def compute_integral(array, tmin, tmax):
    tmin_sample = convert_time_into_sample(tmin)
    tmax_sample = convert_time_into_sample(tmax)
    integral = trapz(array[tmin_sample:tmax_sample])
    return integral


def convert_time_into_sample(time, sample_freq=500):
    time += 0.2
    sample = time * sample_freq
    print('Time adjusted by adding 0.2 seconds')
    return int(sample)


def swap_first_and_second_keys(original_dict):
    one_first_key = list(original_dict.keys())[0]
    reordered_dict = {second_key: {first_key: None for first_key in original_dict.keys()} for second_key in original_dict[one_first_key].keys()}
    for first_key in reordered_dict:
        for second_key in reordered_dict[first_key]:
            reordered_dict[first_key][second_key] = original_dict[second_key][first_key]
    return reordered_dict









