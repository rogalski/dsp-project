import os

import numpy as np
import matplotlib

import blocks
import plots
import utils
import system


class InteractiveRunner(object):
    # pylint: disable=too-few-public-methods
    __INTERACTIVE__ = False
    plotOutputDir = "_output"
    NO_NOISE = True
    NO_LPR = True

    def __init__(self):
        self._data = utils.DataLoader()
        self._system = None

    def run(self):
        self._set_up_packages()
        self._load_data()
        self._build_system()
        self._system.simulate()
        self._make_plots()

    def _set_up_packages(self):
        np.set_printoptions(threshold=np.inf)
        matplotlib.rcParams['axes.formatter.use_locale'] = True
        os.makedirs(self.plotOutputDir, exist_ok=True)

    def _load_data(self):
        if self.__INTERACTIVE__:
            self._data.load_via_stdin()
        else:
            self._data.mock()

    def _build_system(self):
        self._system = system.System()
        self._build_system_blocks()
        self._system.sampling_frequency = self._data.sampling_freq

    def _build_system_blocks(self):
        blocks_cascade = [self._make_generator(),
                          self._make_modulator(),
                          blocks.channels.MultiPathChannel(),
                          self._make_noiser(),
                          self._make_low_pass_filter(),
                          self._make_demodulator()]
        for block in blocks_cascade:
            self._system.append_block(block)

        # just for sake of readability later
        self._system.GENERATOR = 0
        self._system.MODULATOR = 1
        self._system.CHANNEL = 3
        self._system.LPF = 4
        self._system.DEMODULATOR = 5

    def _make_generator(self):
        generator = blocks.generators.SineGenerator()
        generator.frequency = self._data.modulating_freq
        generator.generation_time = self._data.generation_time
        return generator

    def _make_modulator(self):
        modulator = blocks.modems.FrequencyModulator()
        modulator.frequency_deviation = self._data.freq_deviation
        modulator.carrier_frequency = self._data.carrier_freq
        return modulator

    def _make_noiser(self):
        noise_maker = blocks.noisers.Noiser()
        noise_maker.expected_snr = self._data.expected_snr
        return noise_maker

    def _make_low_pass_filter(self):
        filter_block = blocks.filters.LowPassFilter()
        cutoff_freq = self._data.carrier_freq + self._data.freq_deviation
        filter_block.cutoff_frequency = cutoff_freq
        return filter_block

    def _make_demodulator(self):
        demodulator = blocks.modems.FrequencyDemodulator()
        demodulator.frequency_deviation = self._data.freq_deviation
        demodulator.carrier_frequency = self._data.carrier_freq
        return demodulator

    def _make_plots(self):
        plots.SystemPlotMaker(self._system, self.plotOutputDir).make()


if __name__ == "__main__":
    InteractiveRunner().run()
