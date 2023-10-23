import numpy as np
from eeg_analysis import helper_functions as hf
import mne
from matplotlib import pyplot as plt
from scipy.stats import page_trend_test
import pandas as pd
import time

# check up plots
ev = hf.read_evokeds_old(root='C:/USO_Project/eeg_preprocessing/', how='per distance', ids=ids, averaged=True)
mne.viz.plot_compare_evokeds(ev, ci=False)
ev = mne.grand_average(list(ev.values()))
ev.plot()
# get epochs
ids = hf.get_ids()
epochs = hf.read_epochs(ids=ids)
hf.apply_baseline(epochs=epochs)

distances = ['Distance 1', 'Distance 2', 'Distance 3', 'Distance 4', 'Distance 5']
rolloffs = ['< 5600', '5600 - 8700', '8700 - 11100', '11100 - 15000', '> 15000']
evokeds_ordered = {subject: {distance: {rolloff: None for rolloff in rolloffs} for distance in distances} for subject in ids}
# group epochs by distance and rolloff and create evokeds
for subject in evokeds_ordered:
    for distance in evokeds_ordered[subject]:
        evokeds_ordered[subject][distance] = {
            '< 5600': epochs[subject][f"Event_description == '{distance}' and rolloff < 5600"].average(),
            '5600 - 8700': epochs[subject][f"Event_description == '{distance}' and 5600 < rolloff < 8700"].average(),
            '8700 - 11100': epochs[subject][f"Event_description == '{distance}' and 8700 < rolloff < 11100"].average(),
            '11100 - 15000': epochs[subject][f"Event_description == '{distance}' and 11100 < rolloff < 15000"]. average(),
            '> 15000': epochs[subject][f"Event_description == '{distance}' and rolloff > 15000"].average()}
times = evokeds_ordered['03d3rc']['Distance 1']['< 5600'].times

# calculate gfps
gfps = {subject: {distance: {rolloff: None for rolloff in rolloffs} for distance in distances} for subject in ids}
for subject in evokeds_ordered:
    for distance in evokeds_ordered[subject]:
        for rolloff in evokeds_ordered[subject][distance]:
            gfps[subject][distance][rolloff] = evokeds_ordered[subject][distance][rolloff].data.std(axis=0, ddof=0)


# get effect of rolloff:


# calculate means
rolloff_means = {subject: {distance: [] for distance in distances} for subject in ids}
for subject in rolloff_means:
    for distance in rolloff_means[subject]:
        rolloff_means[subject][distance] = np.mean(list(gfps[subject][distance].values()), axis=0)


# reorder gfps
gfps_reordered = {subject: {rolloff: {distance: None for distance in distances} for rolloff in rolloffs} for subject in ids}
for subject in gfps:
    for distance in gfps[subject]:
        for rolloff in gfps[subject][distance]:
            gfps_reordered[subject][rolloff][distance] = gfps[subject][distance][rolloff]

# subtract mean from each condition
gfps_roll_mean_subtracted = {subject: {rolloff: {} for rolloff  in rolloffs} for subject in ids}
for subject in gfps_reordered:
    for rolloff in gfps_reordered[subject]:
        gfps_roll_mean_subtracted[subject][rolloff] = {
            'Distance 1 - mean': np.subtract(gfps_reordered[subject][rolloff]['Distance 1'], rolloff_means[subject]['Distance 1']),
            'Distance 2 - mean': np.subtract(gfps_reordered[subject][rolloff]['Distance 2'], rolloff_means[subject]['Distance 2']),
            'Distance 3 - mean': np.subtract(gfps_reordered[subject][rolloff]['Distance 3'], rolloff_means[subject]['Distance 3']),
            'Disrance 4 - mean': np.subtract(gfps_reordered[subject][rolloff]['Distance 4'], rolloff_means[subject]['Distance 4']),
            'Distance 5 - mean': np.subtract(gfps_reordered[subject][rolloff]['Distance 5'], rolloff_means[subject]['Distance 5'])}

# average difference waves over the distances
# reorder

gfps_roll_mean_subtracted_avg = {subject: {} for subject in ids}
for subject in gfps_roll_mean_subtracted:
    gfps_roll_mean_subtracted_avg[subject] = {
        'below 5600 Hz - Mean, distance cleaned': np.mean(list(gfps_roll_mean_subtracted[subject]['< 5600'].values()), axis=0),
        '5600 Hz to 8700 Hz - Mean, distance cleaned': np.mean(list(gfps_roll_mean_subtracted[subject]['5600 - 8700'].values()), axis=0),
        '8700 Hz to 11100 Hz - Mean, distance cleaned': np.mean(list(gfps_roll_mean_subtracted[subject]['8700 - 11100'].values()), axis=0),
        '11100 Hz to 15000 Hz - Mean, distance cleaned': np.mean(list(gfps_roll_mean_subtracted[subject]['11100 - 15000'].values()), axis=0),
        'over 15000 Hz - Mean, distance cleaned': np.mean(list(gfps_roll_mean_subtracted[subject]['> 15000'].values()), axis=0)}


# plot
gfps_roll_mean_subtracted_avg_swapped = hf.swap_first_and_second_keys(gfps_roll_mean_subtracted_avg)
for rolloff in gfps_roll_mean_subtracted_avg_swapped:
    plt.plot(times, np.mean(list(gfps_roll_mean_subtracted_avg_swapped[rolloff].values()), axis=0) * 1e6, label=rolloff)
plt.legend(loc=(1.04, 0.5))
plt.ylabel('Δ Voltage [µv]')
plt.xlabel('Time [s]')
plt.axvline(0, color='black', linestyle='dashed')
plt.axhline(0, color='black', linewidth=0.5)
plt.show()
plt.savefig('C:/USO_Project/Write_Up/thesis_plots/rolloff_distance_cleaned.png', bbox_inches='tight')


# page test
page_results = {}
tmin = 0.0
tmax = 0.04
while tmax <= 0.8:
    integrals = {subject: {rolloff: None for rolloff in gfps_roll_mean_subtracted_avg_swapped.keys()} for subject in ids}
    for subject in gfps_roll_mean_subtracted_avg:
        for rolloff in gfps_roll_mean_subtracted_avg[subject]:
            integrals[subject][rolloff] = hf.compute_integral(gfps_roll_mean_subtracted_avg[subject][rolloff], tmin=tmin, tmax=tmax)
    array_for_page_test = []
    for subject in integrals:
        array_for_page_test.append(list(integrals[subject].values()))
    res = page_trend_test(array_for_page_test, predicted_ranks=[5, 4, 3, 2, 1])
    page_results[f'{tmin} - {tmax}'] = res
    tmin += 0.04
    tmax += 0.04

df = pd.DataFrame(data=page_results, index=[0])
df.to_excel('C:/USO_Project/eeg_analysis/data/page_results/rolloff_difference_distance_cleaned_rolloff_based_below_5600_is_highest_rank.xlsx')


####################################################
# plot average gfps per distance
rolloff_means_swap = hf.swap_first_and_second_keys(rolloff_means)
for distance in rolloff_means_swap:
    plt.plot(times, np.mean(list(rolloff_means_swap[distance].values()), axis=0) * 1e6, label=distance)
plt.legend()
plt.show()


