import os

import numpy as np
import matplotlib

import blocks

import blocks.abstract_block
import blocks.filters.lowpass
import blocks.generators
import blocks.modulators
import blocks.noisers
import blocks.system
import plots
import utils


class InteractiveRunner(object):
    # pylint: disable=too-few-public-methods
    __INTERACTIVE__ = False
    plotOutputDir = "output"

    def __init__(self):
        self._data_loader = utils.DataLoader()
        self._system = None

    def run(self):
        self._set_up_packages()
        self._load_data()
        self._build_system()
        self._system.simulate()
        self._make_plots()

    def _set_up_packages(self):
        np.set_printoptions(threshold=np.inf)
        matplotlib.rcParams['axes.formatter.use_mathtext'] = True
        matplotlib.rcParams['axes.formatter.use_locale'] = True
        os.makedirs(self.plotOutputDir, exist_ok=True)

    def _load_data(self):
        if self.__INTERACTIVE__:
            self._data_loader.load_via_stdin()
        else:
            self._data_loader.mock()

    def _build_system(self):
        self._system = blocks.system.System()
        self._build_system_blocks()
        self._system.set_sampling_frequency(self._data_loader.sampling_freq)

    def _build_system_blocks(self):
        blocks_cascade = [self._make_generator(),
                          self._make_modulator(),
                          self._make_channel(),
                          self._make_lpf()]
        for block in blocks_cascade:
            self._system.append_block(block)
        self._system.GENERATOR = 0
        self._system.MODULATOR = 1
        self._system.CHANNEL = 2
        self._system.LPF = 3

    def _make_generator(self):
        generator = blocks.generators.SineGenerator()
        generator.set_frequency(self._data_loader.modulating_freq)
        generator.set_generation_time(self._data_loader.generation_time)
        return generator

    def _make_modulator(self):
        modulator = blocks.modulators.FrequencyModulator()
        modulator.set_frequency_deviation(self._data_loader.freq_deviation)
        modulator.set_carrier_frequency(self._data_loader.carrier_freq)
        return modulator

    def _make_channel(self):
        noise_maker = blocks.noisers.NoiseMaker()
        noise_maker.set_expected_snr(self._data_loader.expected_snr)
        return noise_maker

    def _make_lpf(self):
        lpf = blocks.filters.lowpass.LowPassFilter()
        return lpf

    def _make_plots(self):
        plots.SystemPlotMaker(self._system, self.plotOutputDir).make()


if __name__ == "__main__":
    InteractiveRunner().run()
