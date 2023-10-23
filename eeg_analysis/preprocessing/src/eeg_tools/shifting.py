import mne
import numpy as np
import pandas as pd


def shift_me(data, metadata=None, sfreq=None):
    onset_delay = metadata['onset_delay_avg'].iloc[0]
    onset_delay_in_samples = int(onset_delay * sfreq)
    shifted_data = np.roll(data, -onset_delay_in_samples)
    return shifted_data


def shift_epochs_by_onset_delay(epochs):
    print('Creating list for shifted epochs')
    epochs_shifted_list = list()
    print('Start shifting')
    for idx in range(len(epochs)):
        epoch = epochs[idx]
        epoch.apply_function(shift_me, metadata=epoch.metadata, sfreq=epochs.info['sfreq'])
        epochs_shifted_list.append(epoch)
    print('Concatenate epochs back together...')
    epochs_shifted_concatenated = mne.concatenate_epochs(epochs_shifted_list, add_offset=False)
    print('Setting annotations...')
    epochs_shifted_concatenated.set_annotations(annotations=epochs.annotations)
    print('Done')
    return epochs_shifted_concatenated


def crop_epochs(epochs, tmin, tmax):
    print('Cropping epochs')
    epochs.crop(tmin=tmin, tmax=tmax, include_tmax=True)
    return epochs

