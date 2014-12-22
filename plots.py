import os

from matplotlib import ticker
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
        plt.figure(figsize=(8, 12))
        plt.subplot(4, 1, 1)
        plt.plot(time, generator.output)
        plt.title("Modulating signal")
        self._add_std_figure_formatting('s', 'V')
        plt.subplot(4, 1, 2)
        plt.plot(time, modulator.carrier)
        plt.title("Carrier")
        self._add_std_figure_formatting('s', 'V')
        plt.subplot(4, 1, 3)
        plt.plot(time, modulator.output)
        plt.title("Modulated signal")
        self._add_std_figure_formatting('s', 'V')
        plt.subplot(4, 1, 4)
        plt.title("Modulated signal amplitude spectrum")
        self._plot_spectrum(modulator.output)
        plt.tight_layout()
        self._save_plt("input")

    def _make_noise_plots(self):
        time = self._system.timeline
        channel = self._system.get_block(self._system.CHANNEL)
        lpf = self._system.get_block(self._system.LPF)
        plt.figure()
        plt.plot(time, channel.output, ':b',
                 time, channel.input, '-g',
                 time, lpf.output, '-.r')
        plt.legend(["Post-Channel", "Pre-Channel", "After LPF"])
        self._add_std_figure_formatting('s', 'V')
        self._save_plt("pre_post_noise")

        plt.figure()
        self._plot_spectrum(channel.noise)
        self._save_plt("noise_spectrum")

    def _make_demod_plots(self):
        time = self._system.timeline
        demod = self._system.get_block(self._system.DEMODULATOR)
        mod = self._system.get_block(self._system.MODULATOR)
        plt.figure()
        plt.plot(time, mod.input,
                 time, demod.output)
        plt.legend(["Modulator output", "Demodulator output"])
        self._add_std_figure_formatting('s', 'V')
        self._save_plt("modulated_demodulated")

    def _plot_spectrum(self, signal):
        sampling_freq = self._system.sampling_frequency
        samples_count = len(signal)
        yf = np.fft.fft(signal)
        xf = np.fft.fftfreq(samples_count, 1 / sampling_freq)
        xf = np.fft.fftshift(xf)
        yplot = np.fft.fftshift(yf)
        plt.stem(xf, 1.0 / samples_count * np.abs(yplot))
        plt.xlim(0, utils.DataLoader().carrier_freq * 2)
        self._add_std_figure_formatting('Hz', 'V')

    def _add_std_figure_formatting(self, x_unit, y_unit):
        # pylint: disable=no-self-use
        x_formatter = ticker.EngFormatter(unit=x_unit, places=1)
        y_formatter = ticker.EngFormatter(unit=y_unit, places=1)
        x_formatter.ENG_PREFIXES[-6] = 'u'
        y_formatter.ENG_PREFIXES[-6] = 'u'
        ax = plt.gca()
        ax.xaxis.set_major_formatter(x_formatter)
        ax.yaxis.set_major_formatter(y_formatter)
        plt.grid('on')

    def _save_plt(self, filename):
        plt.savefig(os.path.join(self._output_dir, filename + '.svg'))
