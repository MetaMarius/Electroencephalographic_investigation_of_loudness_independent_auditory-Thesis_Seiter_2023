import numpy as np
import pandas as pd
from eeg_analysis import helper_functions as hf
import mne
from matplotlib import pyplot as plt
from scipy.stats import f_oneway
from scipy.stats import page_trend_test
import scipy.stats as st

# get evokeds
ids = hf.get_ids()
evokeds = hf.read_evokeds(sorting='subjects', ids=ids)
times = evokeds['03d3rc'][0].times

# calculate gfps
gfps = {subject: {} for subject in ids}
for subject in evokeds:
    for evoked in evokeds[subject]:
        gfps[subject][evoked.comment] = evoked.data.std(axis=0, ddof=0)
    gfps[subject] = dict(sorted(gfps[subject].items()))

# calculate mean gfps of subjects
grand_average_evokeds = hf.read_evokeds_old('C:/USO_Project/eeg_preprocessing/', averaged=True, ids=ids, how='per participant')
mean_gfps = {}
for subject in grand_average_evokeds:
    mean_gfps[subject] = grand_average_evokeds[subject].data.std(axis=0, ddof=0)


# check-up plot
fig, ax = plt.subplots()
ax.plot(evokeds['03d3rc'][0].times, mean_gfps['03d3rc'], color='black')
ax.plot(evokeds['03d3rc'][0].times, gfps['03d3rc']['Distance 1'], label='Distance 1')
ax.plot(evokeds['03d3rc'][0].times, gfps['03d3rc']['Distance 2'], label='Distance 2')
ax.plot(evokeds['03d3rc'][0].times, gfps['03d3rc']['Distance 3'], label='Distance 3')
ax.plot(evokeds['03d3rc'][0].times, gfps['03d3rc']['Distance 4'], label='Distance 4')
ax.plot(evokeds['03d3rc'][0].times, gfps['03d3rc']['Distance 5'], label='Distance 5')
ax.legend()

# subtract mean gfps from the distance gfps
difference_wave_gfps_per_subject = {subject: {} for subject in ids}
for subject in ids:
    difference_wave_gfps_per_subject[subject] = {
        'Distance 1 - Mean': np.subtract(gfps[subject]['Distance 1'], mean_gfps[subject]),
        'Distance 2 - Mean': np.subtract(gfps[subject]['Distance 2'], mean_gfps[subject]),
        'Distance 3 - Mean': np.subtract(gfps[subject]['Distance 3'], mean_gfps[subject]),
        'Distance 4 - Mean': np.subtract(gfps[subject]['Distance 4'], mean_gfps[subject]),
        'Distance 5 - Mean': np.subtract(gfps[subject]['Distance 5'], mean_gfps[subject])}

# chek-up plot
fig, ax = plt.subplots()
ax.plot(evokeds['03d3rc'][0].times, difference_wave_gfps_per_subject['03d3rc']['Distance 1 - Mean'], label='Distance 1 - Mean')
ax.plot(evokeds['03d3rc'][0].times, difference_wave_gfps_per_subject['03d3rc']['Distance 2 - Mean'], label='Distance 2 - Mean')
ax.plot(evokeds['03d3rc'][0].times, difference_wave_gfps_per_subject['03d3rc']['Distance 3 - Mean'], label='Distance 3 - Mean')
ax.plot(evokeds['03d3rc'][0].times, difference_wave_gfps_per_subject['03d3rc']['Distance 4 - Mean'], label='Distance 4 - Mean')
ax.plot(evokeds['03d3rc'][0].times, difference_wave_gfps_per_subject['03d3rc']['Distance 5 - Mean'], label='Distance 5 - Mean')
ax.legend()

# reorder gfps per subject to gfps per distance
difference_gfps_per_distance = {distance: {} for distance in difference_wave_gfps_per_subject['03d3rc']}
for subject in difference_wave_gfps_per_subject:
    for distance in difference_wave_gfps_per_subject[subject]:
        difference_gfps_per_distance[distance][subject] = (difference_wave_gfps_per_subject[subject][distance])

# create mean gfps per distance
averaged_difference_gfps_per_distance = {}
for distance in difference_gfps_per_distance:
    arrays_of_distance = [difference_gfps_per_distance[distance][subject] for subject in difference_gfps_per_distance[distance]]
    averaged_difference_gfps_per_distance[distance] = np.mean(arrays_of_distance, axis=0)

# plotting
for distance in averaged_difference_gfps_per_distance:
    plt.plot(evokeds['03d3rc'][0].times, averaged_difference_gfps_per_distance[distance] * 1e6, label=distance)
plt.legend()
plt.ylabel('Δ Voltage [µv]')
plt.xlabel('Time [s]')
plt.axvline(0, color='black', linestyle='dashed')
plt.axvline(0.12, color='grey', linestyle='dashed')
plt.axvline(0.4, color='grey', linestyle='dashed')
plt.axhline(0, color='black', linewidth=0.5)
plt.show()

# compute integrals of gfps ordered by distance
integrals_per_distance = {distance: [] for distance in difference_gfps_per_distance}
for distance in difference_gfps_per_distance:
    for subject in difference_gfps_per_distance[distance]:
        integrals_per_distance[distance].append(hf.compute_integral(difference_gfps_per_distance[distance][subject], tmin=0.0, tmax=0.))


# page Test:
page_results = {}
tmin = 0.0
tmax = 0.04
while tmax <= 0.8:
    # compute integrals of gfps ordered by subject
    integrals_per_subject = {subject: [] for subject in difference_wave_gfps_per_subject}
    for subject in difference_wave_gfps_per_subject:
        for distance in difference_wave_gfps_per_subject[subject]:
            integrals_per_subject[subject].append(hf.compute_integral(difference_wave_gfps_per_subject[subject][distance], tmin=0.4, tmax=0.8))

    array_for_page_test = []
    for subject in integrals_per_subject:
        array_for_page_test.append(integrals_per_subject[subject])
    res = page_trend_test(array_for_page_test, predicted_ranks=[5, 2, 1, 3, 4])
    page_results[f'{tmin} - {tmax}'] = res
    tmin += 0.04
    tmax += 0.04

df = pd.DataFrame(data=page_results, index=[0])
df.to_excel('C:/USO_Project/eeg_analysis/data/page_results/distance_difference_nothing_cleaned_distance_based.xlsx')


###########################################################
# plotting gfp differences for every subject

for subject in difference_wave_gfps_per_subject:
    fig, ax = plt.subplots()
    for distance in difference_wave_gfps_per_subject[subject]:
        ax.plot(evokeds['03d3rc'][0].times, difference_wave_gfps_per_subject[subject][distance], label=distance)
    ax.legend()








