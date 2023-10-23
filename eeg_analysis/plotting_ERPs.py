import matplotlib.pyplot as plt
import mne
from eeg_analysis import helper_functions as hf

ids = hf.get_ids()
epochs = hf.read_epochs(ids=ids)
all_epochs = mne.concatenate_epochs(list(epochs.values()))
evokeds = all_epochs.average()
evokeds.plot_joint(times=[0.068, 0.1, 0.2, 0.56], title=None)

evokeds_per_distance = hf.read_evokeds(ids=ids, sorting='condition')
mne.viz.plot_compare_evokeds(evokeds_per_distance)








