import random
import math
import numpy as np
import slab


def gen_stimulus():  # loop to conveniently create many stimuli
    n = 0
    while n < 7:
        s = combine_sounds(length=24000, base=random.randint(0, 6), n_sounds=6)
        a = 'p'
        while a == "p":
            s.play()
            a = input('Take?')
        if a == "y":
            s.write("uso_500ms/" + "new_uso_" + input("File number:") + '.wav')
        elif a == "s":
            break
        else:
            continue
    print("Finished")


def combine_sounds(length=24000, base=0, n_sounds=6):
    bases = ['dryer', 'particl2', 'spray', 'shaver', 'tear', 'crumple', 'coffmill']  # set of base sounds

    folders = ['cherry1', 'cherry2', 'cherry3', 'wood2', 'wood3',
               'bank', 'bowl', 'candybwl', 'colacan', 'metal15', 'metal10', 'metal05', 'trashbox',
               'case1', 'case2', 'case3', 'dice2', 'dice3',
               'bottle1', 'bottle2', 'china3', 'china4',
               'saw2', 'sandpp1', 'sandpp2',
               'sticks',
               'clap1', 'clap2', 'cap1', 'cap2', 'snap', 'cracker',
               'bell2', 'bells3', 'coin2', 'coin3',
               'book1', 'book2',
               'castanet', 'maracas', 'drum',
               'stapler', 'punch']  # set of sounds that get added on top

    sout = slab.Sound('mitsubishi_wavs/' + bases[base] + '.wav')  # reading in base sound
    base_sr = sout.samplerate
    sout = sout.data[:, 0]  # taking the data array of the base sound
    if base != 0:  # base sound 0 is already 24000 samples long, the following line doesn't have to be executed
        sout = sout[np.where((sout > 0.03) == True)[0][0]:np.where((sout > 0.03) == True)[0][-1]][1000:25000]   # cutting bases 24000 samples long and taking only parts where it is louder than 0.03

    for i in range(n_sounds):
        f = random.choice(folders)  # selecting random sound
        s = slab.Sound('mitsubishi_wavs/' + f + '.wav')  # reading in sound
        s_sr = s.samplerate
        if base_sr != s_sr:
            print("Error: Samplerates don't match")
        offset = math.ceil(np.random.random(1) * length) # - 4800)  # create random offset between 0 and 24000
        if offset < 0:
            offset = 0
        s = np.append(np.zeros(offset), s)  # append array of zeros with length of offset in front of sound
        s = np.append(s, np.zeros(length))  # append array of zeros with length of length at the end of sound
        s = s[:length]  # /15000  # cut array down from beginning on to 24000 samples long -> this way the randomly selected sounds get added on top of base from a random sample onwards
        sout = np.sum((sout, s), axis=0)
    # sout.data = sout.data*0.5
    sout = sout / abs(sout).max()  # normalize data to 1 as maximum
    return slab.Sound(data=sout, samplerate=48000)
