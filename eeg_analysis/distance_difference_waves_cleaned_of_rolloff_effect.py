import numpy as np
from eeg_analysis import helper_functions as hf
import mne
from matplotlib import pyplot as plt
from scipy.stats import page_trend_test
import pandas as pd


# get epochs
ids = hf.get_ids()
epochs = hf.read_epochs(ids=ids)
hf.apply_baseline(epochs=epochs)

# find a combination of conditions so individual occurences are maximum
all_epochs = mne.concatenate_epochs(list(epochs.values()))


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



# calculate means
distance_means = {subject: {rolloff: [] for rolloff in rolloffs} for subject in ids}
# reorder
for subject in gfps:
    for distance in gfps[subject]:
        for rolloff in gfps[subject][distance]:
            distance_means[subject][rolloff].append(gfps[subject][distance][rolloff])

for subject in distance_means:
    for rolloff in distance_means[subject]:
        m = np.mean(distance_means[subject][rolloff], axis=0)
        distance_means[subject][rolloff] = m

# subtract means
gfps_dis_mean_subtracted = {subject: {distance: {} for distance in distances} for subject in ids}
for subject in gfps:
    for distance in gfps[subject]:
        gfps_dis_mean_subtracted[subject][distance] = {
            '< 5600 - mean': np.subtract(gfps[subject][distance]['< 5600'], distance_means[subject]['< 5600']),
            '5600 to 8700 - mean': np.subtract(gfps[subject][distance]['5600 - 8700'], distance_means[subject]['5600 - 8700']),
            '8700 to 11100 - mean': np.subtract(gfps[subject][distance]['8700 - 11100'], distance_means[subject]['8700 - 11100']),
            '11100 to 15000 - mean': np.subtract(gfps[subject][distance]['11100 - 15000'], distance_means[subject]['11100 - 15000']),
            '> 15000 - mean': np.subtract(gfps[subject][distance]['> 15000'], distance_means[subject]['> 15000'])
        }

# average difference waves over the rolloffs
gfps_dis_mean_subtracted_avg = {subject: {} for subject in ids}
for subject in gfps_dis_mean_subtracted:
    gfps_dis_mean_subtracted_avg[subject] = {
        'Distance 1 - Mean, rolloff cleaned': np.mean(list(gfps_dis_mean_subtracted[subject]['Distance 1'].values()), axis=0),
        'Distance 2 - Mean, rolloff cleaned': np.mean(list(gfps_dis_mean_subtracted[subject]['Distance 2'].values()), axis=0),
        'Distance 3 - Mean, rolloff cleaned': np.mean(list(gfps_dis_mean_subtracted[subject]['Distance 3'].values()), axis=0),
        'Distance 4 - Mean, rolloff cleaned': np.mean(list(gfps_dis_mean_subtracted[subject]['Distance 4'].values()), axis=0),
        'Distance 5 - Mean, rolloff cleaned': np.mean(list(gfps_dis_mean_subtracted[subject]['Distance 5'].values()), axis=0)
    }

# plot
gfps_dis_mean_subtracted_avg_swapped = hf.swap_first_and_second_keys(gfps_dis_mean_subtracted_avg)
for distance in gfps_dis_mean_subtracted_avg_swapped:
    plt.plot(times, np.mean(list(gfps_dis_mean_subtracted_avg_swapped[distance].values()), axis=0) * 1e6, label=distance)
plt.legend(loc=(1.04, 0.5))
plt.xlabel(xlabel='Time [s]')
plt.ylabel(ylabel='Δ Voltage [µV]')
plt.axvline(0, color='black', linestyle='dashed')
plt.axvline(0.12, color='grey', linestyle='dashed')
plt.axvline(0.4, color='grey', linestyle='dashed')
plt.axhline(0, color='black', linewidth=0.5)
plt.show()
plt.savefig('C:/USO_Project/Write_Up/thesis_plots/distance_rolloff_cleaned.png', bbox_inches='tight')


# page test

page_results = {}
tmin = 0.0
tmax = 0.04
while tmax < 0.9:
    integrals = {subject: {rolloff: None for rolloff in gfps_dis_mean_subtracted_avg_swapped.keys()} for subject in ids}
    for subject in gfps_dis_mean_subtracted_avg:
        for rolloff in gfps_dis_mean_subtracted_avg[subject]:
            integrals[subject][rolloff] = hf.compute_integral(gfps_dis_mean_subtracted_avg[subject][rolloff], tmin=tmin, tmax=tmax)
    array_for_page_test = []
    for subject in integrals:
        array_for_page_test.append(list(integrals[subject].values()))
    res = page_trend_test(array_for_page_test, predicted_ranks=[5, 2, 1, 3, 4])
    page_results[f'{tmin} - {tmax}'] = res
    tmin += 0.04
    tmax += 0.04

df = pd.DataFrame(data=page_results, index=[0])
df.to_excel('C:/USO_Project/eeg_analysis/data/page_results/distance_difference_rolloff_cleaned_norm_based.xlsx')

############################################
# plot gfps per rolloff

distance_means_swapped = hf.swap_first_and_second_keys(distance_means)
for rolloff in distance_means_swapped:
    plt.plot(times, np.mean(list(distance_means_swapped[rolloff].values()), axis=0) *1e6, label=rolloff)
plt.legend()
plt.show()




