# if anything goes wrong, it's a sandbox

import numpy as np

CARRIER_FREQ = 10e6
MODULATING_FREQ = 2e6
FREQ_DEVIATION = 1e6
GENERATION_TIME = 1 // MODULATING_FREQ
SAMPLING_FREQ = 64 * CARRIER_FREQ

time = np.arange(0, GENERATION_TIME, 1 / SAMPLING_FREQ)
sine = np.sin(2 * np.pi * CARRIER_FREQ * time)

snr = 20
length = len(sine)
average = np.mean(sine)
var = np.sum(np.abs(sine - average) ** 2) / len(sine)
sigma = np.sqrt(var) * 10 ** (-snr / 20)

noise = sigma * np.random.randn(len(sine), 1)
sine_energy = np.sum(sine ** 2)
noise_energy = np.sum(noise ** 2)
print("Obtained SNR: ", 10 * np.log10(sine_energy / noise_energy))