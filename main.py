import os

import matplotlib.pyplot as plt
import numpy as np

import blocks
import blocks.generators
import blocks.modulators
import blocks.noisers
import blocks.system
import utils


CARRIER_FREQ = 50e6
MODULATING_FREQ = 1e6
FREQ_DEVIATION = 45e6
GENERATION_TIME = 4 / MODULATING_FREQ
SAMPLING_FREQ = 64 * CARRIER_FREQ


def make_signal_generator():
    generator = blocks.generators.SawGenerator()
    generator.set_frequency(utils.DataLoader().modulating_freq)
    generator.set_generation_time(utils.DataLoader().generation_time)
    return generator


def make_fm_modulator():
    modulator = blocks.modulators.FrequencyModulator()
    modulator.set_frequency_deviation(utils.DataLoader().freq_deviation)
    modulator.set_carrier_frequency(utils.DataLoader().carrier_freq)
    return modulator


def make_noiser():
    noiser = blocks.noisers.WhiteNoiser()
    noiser.set_expected_snr(30)
    return noiser


def make_system():
    system = blocks.system.System()
    system.append_block(make_signal_generator())
    system.append_block(make_fm_modulator())
    system.append_block(make_noiser())
    system.set_sampling_frequency(SAMPLING_FREQ)
    return system


def main():
    np.set_printoptions(threshold=np.inf)
    utils.DataLoader().load_via_stdin()
    system = make_system()
    system.simulate()

    os.makedirs("output", exist_ok=True)

    print(system)
    for index, block in enumerate(system):
        print("Processing block", index)
        plt.figure(figsize=(50, 5))
        plt.plot(system.get_timeline(), block.get_input(),
                 system.get_timeline(), block.get_output())
        plt.grid(True, 'both')
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude [V]")
        plt.title("Input and output of {0}".format(block))
        plt.savefig("output/{}.png".format(index))
        try:
            print("SNR", block.get_snr())
        except AttributeError:
            pass


if __name__ == "__main__":
    main()
