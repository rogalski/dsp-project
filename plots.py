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
        self._make_demod_plots()

    def _make_inputs_plot(self):
        time = self._system.timeline
        generator = self._system.get_block(self._system.GENERATOR)
        modulator = self._system.get_block(self._system.MODULATOR)
        plt.figure()
        plt.subplot(4, 1, 1)
        plt.plot(time, generator.output)
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude [V]")
        plt.subplot(4, 1, 2)
        plt.plot(time, modulator.get_carrier())
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude [V]")
        plt.subplot(4, 1, 3)
        plt.plot(time, modulator.output)
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude [V]")
        plt.subplot(4, 1, 4)
        self._plot_spectrum(modulator.output)
        self._save_plt("Inputs")

    def _make_noise_plots(self):
        time = self._system.timeline
        channel = self._system.get_block(self._system.CHANNEL)
        lpf = self._system.get_block(self._system.LPF)
        plt.figure()
        plt.plot(time, channel.output, ':b',
                 time, channel.input, '-r',
                 time, lpf.output, '-.g')
        plt.legend(["Post-Channel", "Pre-Channel", "After LPF"])
        self._save_plt("PrePostNoise")

        plt.figure()
        self._plot_spectrum(channel.noise)
        self._save_plt("noise_spectrum")

    def _make_demod_plots(self):
        time = self._system.timeline
        demod = self._system.get_block(self._system.DEMOD)
        mod = self._system.get_block(self._system.MODULATOR)
        plt.figure()
        plt.plot(time, mod.output,
                 time, demod.output)
        print(demod.output)
        plt.legend(["mod", "demod"])
        self._save_plt("demod")

    def _plot_spectrum(self, signal):
        sampling_freq = self._system.sampling_frequency
        samples_count = len(signal)
        yf = np.fft.fft(signal)
        xf = np.fft.fftfreq(samples_count, 1 / sampling_freq)
        xf = np.fft.fftshift(xf)
        yplot = np.fft.fftshift(yf)
        plt.stem(xf, 1.0 / samples_count * np.abs(yplot))
        plt.xlim(0, utils.DataLoader().carrier_freq * 2)

    def _save_plt(self, filename):
        plt.savefig(os.path.join(self._output_dir, filename))
