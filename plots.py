import os

from matplotlib import ticker
from matplotlib import pyplot as plt
import numpy as np
import scipy

import utils


class SystemPlotMaker(object):
    # pylint: disable=too-few-public-methods
    def __init__(self, system, output_dir):
        self._system = system
        self._output_dir = output_dir

    def make(self):
        self._make_inputs_plot()
        self._make_noise_time_plots()
        self._make_demod_plots()
        self._make_filter_plots()
        self._make_error_plots()

    def _make_inputs_plot(self):
        time = self._system.timeline
        generator = self._system.get_block(self._system.GENERATOR)
        modulator = self._system.get_block(self._system.MODULATOR)
        plt.figure(figsize=(8, 12))
        plt.subplot(4, 1, 1)
        plt.plot(time, generator.output)
        plt.title("Wykres 1. Sygnał modulujący")
        self._add_std_figure_formatting('s', 'V')
        plt.subplot(4, 1, 2)
        self._plot_spectrum(modulator.carrier)
        plt.title("Wykres 2. Widmo nośnej")
        plt.subplot(4, 1, 3)
        plt.plot(time, modulator.output)
        plt.title("Wykres 3. Sygnał zmodulowany")
        self._add_std_figure_formatting('s', 'V')
        plt.subplot(4, 1, 4)
        plt.title("Wykres 4. Widmo amplitudowe sygnału zmodulowanego")
        self._plot_spectrum(modulator.output)
        plt.tight_layout()
        self._save_plt("input")

    def _make_noise_time_plots(self):
        time = self._system.timeline
        channel = self._system.get_block(self._system.CHANNEL)
        lpf = self._system.get_block(self._system.LPF)
        plt.figure()
        plt.plot(time, channel.input, '-g',
                 time, channel.output, ':b',
                 time, lpf.output, '-.r')
        plt.legend(["Sygnał nadany", "Sygnał odebrany", "Sygnał odebrany po filtracji"])
        self._add_std_figure_formatting('s', 'V')
        plt.title("Wykres 5. Przebiegi czasowe w paśmie wysokiej częstotliwości")
        self._save_plt("pre_post_noise")

        plt.figure()
        self._plot_spectrum(channel.output)
        plt.title("Wykres 6. Widmo sygnału odebranego")
        plt.xlim(0, utils.DataLoader().carrier_freq * 6)
        self._save_plt("noised_spectrum")

    def _make_demod_plots(self):
        time = self._system.timeline
        demod = self._system.get_block(self._system.DEMODULATOR)
        mod = self._system.get_block(self._system.MODULATOR)
        plt.figure()
        plt.plot(time, mod.input,
                 time, demod.output)
        plt.legend(["Sygnał modulujący", "Sygnał zdemodulowany"])
        self._add_std_figure_formatting('s', 'V')
        plt.title("Wykres 7. Sygnał modulujący i zdemodulowany")
        self._save_plt("modulated_demodulated")

    def _make_filter_plots(self):
        filt = self._system.get_block(self._system.LPF)
        b, a = filt.coefficients
        fs = utils.DataLoader().sampling_freq
        length = 120
        impulse = np.repeat(0, length)
        impulse[0] = 1
        response = scipy.signal.lfilter(b, a, impulse)

        w, h = scipy.signal.freqz(*filt.coefficients)
        f = w / np.pi * fs
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.stem(response)
        plt.title("Wykres 8. Odpowiedź impulsowa użytego filtru Butterwortha")
        plt.grid('on')

        plt.subplot(2, 1, 2)
        plt.plot(f, 20 * np.log10(np.abs(h)))
        plt.title("Wykres 9. Odpowiedź częstotliwościowa użytego filtru Butterwortha")
        self._add_std_figure_formatting("Hz", "dB")
        plt.ylim((-80, 1))
        self._save_plt("filter")

    def _make_error_plots(self):
        plt.figure()
        time = self._system.timeline
        demod = self._system.get_block(self._system.DEMODULATOR)
        mod = self._system.get_block(self._system.MODULATOR)
        error = demod.output - mod.input
        plt.plot(time, error)
        self._add_std_figure_formatting('s', 'V')
        plt.title("Wykres 10. Wykres błędu demodulacji")
        self._save_plt("error")

    def _plot_spectrum(self, signal):
        yLimit = -100
        sampling_freq = self._system.sampling_frequency
        samples_count = len(signal)
        yf = np.fft.fft(signal)
        xf = np.fft.fftfreq(samples_count, 1 / sampling_freq)
        xf = np.fft.fftshift(xf)
        yplot = 1.0 / samples_count * np.fft.fftshift(yf)
        plt.plot(xf, 20 * np.log10(np.abs(yplot)))
        plt.xlim(0, utils.DataLoader().carrier_freq * 2)
        self._add_std_figure_formatting('Hz', 'dBV')
        plt.ylim((yLimit, 0))

    def _add_std_figure_formatting(self, x_unit, y_unit):
        # pylint: disable=no-self-use
        x_formatter = ticker.EngFormatter(unit=x_unit)
        y_formatter = ticker.EngFormatter(unit=y_unit)
        x_formatter.ENG_PREFIXES[-6] = 'u'
        y_formatter.ENG_PREFIXES[-6] = 'u'
        ax = plt.gca()
        ax.xaxis.set_major_formatter(x_formatter)
        ax.yaxis.set_major_formatter(y_formatter)
        plt.grid('on')

    def _save_plt(self, filename):
        plt.savefig(os.path.join(self._output_dir, filename + '.svg'))
        plt.savefig(os.path.join(self._output_dir, filename + '.png'))
