import os

from matplotlib import pyplot as plt
import numpy as np

import utils


class SystemPlotMaker(object):
    # pylint: disable=too-few-public-methods
    def __init__(self, system, output_dir):
        self._system = system
        self._output_dir = output_dir

    def make(self):
        self._make_inputs_plot()
        self._make_noise_plots()

    def _make_inputs_plot(self):
        time = self._system.get_timeline()
        generator = self._system.get_block(self._system.GENERATOR)
        modulator = self._system.get_block(self._system.MODULATOR)
        plt.figure()
        plt.subplot(4, 1, 1)
        plt.plot(time, generator.get_output())
        plt.subplot(4, 1, 2)
        plt.plot(time, modulator.get_carrier())
        plt.subplot(4, 1, 3)
        plt.plot(time, modulator.get_output())
        plt.subplot(4, 1, 4)
        self._plot_spectrum(modulator.get_output())
        self._save_plt("Inputs")

    def _make_noise_plots(self):
        time = self._system.get_timeline()
        channel = self._system.get_block(self._system.CHANNEL)
        lpf = self._system.get_block(self._system.LPF)
        plt.figure()
        plt.plot(time, channel.get_output(), ':b',
                 time, channel.get_input(), '-r',
                 time, lpf.get_output(), '-.g')
        plt.legend(["Post-Channel", "Pre-Channel", "After LPF"])
        self._save_plt("PrePostNoise")

    def _plot_spectrum(self, signal):
        sampling_freq = self._system.get_sampling_frequency()
        N = len(signal)
        yf = np.fft.fft(signal)
        xf = np.fft.fftfreq(N, 1 / sampling_freq)
        xf = np.fft.fftshift(xf)
        yplot = np.fft.fftshift(yf)
        plt.stem(xf, 1.0 / N * np.abs(yplot))
        plt.xlim(0, utils.DataLoader().carrier_freq * 2)

    def _save_plt(self, filename):
        plt.savefig(os.path.join(self._output_dir, filename))