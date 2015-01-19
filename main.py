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

    def __init__(self):
        self.data = utils.DataLoader()
        self._data = utils.DataLoader()
        self._system = None

    @property
    def half_band_width(self):
        carrier_freq = self.data.carrier_freq
        mod_freq = self.data.modulating_freq
        freq_dev = self.data.freq_deviation
        return mod_freq + freq_dev

    def run(self):
        self._set_up_packages()
        self._load_data()
        self._build_system()
        self._system.simulate()
        self._report_info()
        self._make_plots()

    def _set_up_packages(self):
        np.set_printoptions(threshold=np.inf)
        matplotlib.rc('font', family='DejaVu Sans', size='10')
        matplotlib.rc('legend', fontsize=10)
        matplotlib.rc('lines', markersize=3)
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
                          self._make_band_pass_filter(),
                          self._make_demodulator()]
        for block in blocks_cascade:
            self._system.append_block(block)

        # just for sake of readability later
        self._system.GENERATOR = 0
        self._system.MODULATOR = 1
        self._system.MULTI_PATH_CHANNEL = 2
        self._system.NOISE_CHANNEL = 3
        self._system.LPF = 4
        self._system.DEMODULATOR = 5

    def _make_generator(self):
        generator = blocks.generators.BandNoiseGenerator()
        generator.generation_time = self._data.generation_time
        generator.bandwidth = self._data.modulating_freq
        return generator

    def _make_modulator(self):
        modulator = blocks.modems.FrequencyModulator()
        modulator.frequency_deviation = self._data.freq_deviation
        modulator.carrier_frequency = self._data.carrier_freq
        return modulator

    def _make_noiser(self):
        noise_maker = blocks.noisers.BandNoiser()
        noise_maker.expected_snr = self._data.expected_snr
        carrier_freq = self.data.carrier_freq
        half_band_width = self.half_band_width
        noise_maker.freqs = [f + carrier_freq for f in (-half_band_width,
                                                        half_band_width)]
        return noise_maker

    def _make_band_pass_filter(self):
        filter_block = blocks.filters.BandPassFilter()
        carrier_freq = self.data.carrier_freq
        half_band_width = self.half_band_width
        filter_block.freqs = [f + carrier_freq for f in (-half_band_width,
                                                         half_band_width)]
        return filter_block

    def _make_demodulator(self):
        demodulator = blocks.modems.FrequencyDemodulator()
        demodulator.frequency_deviation = self._data.freq_deviation
        demodulator.carrier_frequency = self._data.carrier_freq
        return demodulator

    def _report_info(self):
        actual_snr = self._system.get_block(self._system.NOISE_CHANNEL).actual_snr
        print("Actual SNR: ", actual_snr)

    def _make_plots(self):
        plots.SystemPlotMaker(self._system, self.plotOutputDir).make()


if __name__ == "__main__":
    InteractiveRunner().run()
