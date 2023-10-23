from os import listdir
import os
from scipy.signal import find_peaks
import pathlib
import slab

samplerate = 48000
slab.set_default_samplerate(samplerate)
onset_ramp = 0.01
DIR = pathlib.Path(os.getcwd())
file_path = DIR / "data" / "uso_500ms_raw"
file_names = [file_path / f for f in listdir(file_path)]
sound_files = [slab.Sound(file_name) for file_name in file_names]

i = 1
for sound_file in sound_files:
    y = sound_file.data[:, 0]
    peaks = find_peaks(y, height=0.5)
    peak_index = peaks[0][0]
    for duration in [0.1, 0.2, 0.3, 0.4]:
        start = peak_index - slab.Signal.in_samples(onset_ramp, samplerate)
        start = max(start, 0)
        end = start + slab.Signal.in_samples(duration, samplerate)
        output = sound_file.data[start:end]
        folder_name = DIR / "data" / str('uso_' + str(int((duration * 1000))) + 'ms')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        uso_name = folder_name / str("uso_" + str(int((duration * 1000))) + "ms_" + str(i) + ".wav")
        output = slab.Sound(data=output, samplerate=48000)
        output.level -= 5
        output = output.ramp(duration=0.005)
        output.write(uso_name, normalise=False)
        i += 1

