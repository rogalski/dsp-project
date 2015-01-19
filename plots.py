import os

from matplotlib import ticker
from matplotlib import pyplot as plt
import numpy as np
import scipy

import utils


class SystemPlotMaker(object):
    # pylint: disable=too-few-public-methods
    def __init__(self, system, output_dir):
        self.data = utils.DataLoader()
        self._system = system
        self._output_dir = output_dir
        self._plot_counter = 0
        for f in os.listdir(self._output_dir):
            os.remove(os.path.join(self._output_dir, f))

    def make(self):
        self._make_inputs_plot()
        self._make_noise_spectrum_plots()
        self._make_channel_plots()
        self._make_demod_plots()
        self._make_filter_plots()
        self._make_error_plots()

    def _make_inputs_plot(self):
        GRID_X, GRID_Y = 1, 3
        time = self._system.timeline
        generator = self._system.get_block(self._system.GENERATOR)
        modulator = self._system.get_block(self._system.MODULATOR)
        plt.figure(figsize=(8, 12))
        plt.subplot(GRID_Y, GRID_X, 1)
        plt.plot(time, generator.output)
        plt.title(self._build_title("Sygnał modulujący"))
        self._add_std_figure_formatting('s', 'V')
        plt.subplot(GRID_Y, GRID_X, 2)
        self._plot_single_spectrum(generator.output)
        plt.title(self._build_title("Widmo sygnału modulującego"))
        plt.xlim(0, utils.DataLoader().modulating_freq * 3)
        plt.subplot(GRID_Y, GRID_X, 3)
        plt.title(self._build_title("Widmo amplitudowe sygnału zmodulowanego"))
        self._plot_single_spectrum(modulator.output)
        plt.tight_layout()
        self._save_plt("input")

    def _make_noise_time_plots(self):
        time = self._system.timeline
        channel = self._system.get_block(self._system.MULTI_PATH_CHANNEL)
        lpf = self._system.get_block(self._system.LPF)
        plt.figure()
        plt.plot(time, channel.input, '-g',
                 time, channel.output, ':b',
                 time, lpf.output, '-.r')
        plt.legend(["Sygnał nadany", "Sygnał odebrany", "Sygnał odebrany po filtracji"])
        self._add_std_figure_formatting('s', 'V')
        plt.title(self._build_title("Przebiegi czasowe w paśmie wysokiej częstotliwości"))
        self._save_plt("pre_post_noise")

        plt.figure()
        self._plot_single_spectrum(channel.output)
        plt.title(self._build_title("Widmo sygnału odebranego"))
        self._save_plt("noised_spectrum")

    def _make_noise_spectrum_plots(self):
        channel = self._system.get_block(self._system.NOISE_CHANNEL)
        filt = self._system.get_block(self._system.LPF)
        fc, c = self._compute_spectrum_for_plot(channel.output)
        ff, f = self._compute_spectrum_for_plot(filt.output)
        plt.figure()
        plt.plot(fc, c, 'g', ff, f, ':b')
        plt.legend(["Sygnał w kanale", "Sygnał odfiltrowany"])
        plt.title(self._build_title("Widma sygnałów w kanale oraz po filtracji"))
        self._format_spectrum()
        fc = self.data.carrier_freq
        plt.xlim((fc / 2, 3 * fc / 2))
        self._save_plt("filtered_spectrum")

        plt.figure()
        plt.title(self._build_title("Widmo addytywnego szumu w kanale"))
        noise_channel = self._system.get_block(self._system.NOISE_CHANNEL)
        self._plot_single_spectrum(noise_channel.noise)
        self._save_plt("added_noise")

    def _make_demod_plots(self):
        time = self._system.timeline
        demod = self._system.get_block(self._system.DEMODULATOR)
        mod = self._system.get_block(self._system.MODULATOR)
        plt.figure()
        plt.plot(time, mod.input, '-g',
                 time, demod.output, ':b')
        plt.legend(["Sygnał modulujący", "Sygnał zdemodulowany"])
        self._add_std_figure_formatting('s', 'V')
        plt.title(self._build_title("Sygnał modulujący i zdemodulowany"))
        plt.ylim((-1, 1))
        self._save_plt("modulated_demodulated")

    def _make_channel_plots(self):
        plt.figure()
        channel = self._system.get_block(self._system.MULTI_PATH_CHANNEL)
        plt.stem(channel._impulse_response, basefmt='')
        plt.title(self._build_title("Odpowiedź impulsowa kanału"))
        plt.grid('on')
        length = len(channel._impulse_response)
        plt.xlim((-length / 20, length))
        self._save_plt("channel_impulse")

    def _make_filter_plots(self):
        filt = self._system.get_block(self._system.LPF)
        b, a = filt.coefficients
        fs = self.data.sampling_freq
        length = 1000
        impulse = np.repeat(0, length)
        impulse[0] = 1
        response = scipy.signal.lfilter(b, a, impulse)

        w, h = scipy.signal.freqz(*filt.coefficients)
        f = w / np.max(w) * fs / 2
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(response, '.-')
        plt.title(self._build_title("Odpowiedź impulsowa użytego filtru Butterwortha"))
        plt.grid('on')
        plt.xlabel("Nr próbki")
        plt.ylabel("Wartość próbki")
        plt.xlim((0, length))

        plt.subplot(2, 1, 2)
        plt.plot(f, 20 * np.log10(np.abs(h)), '.-')
        plt.title(self._build_title("Odpowiedź częstotliwościowa użytego filtru Butterwortha"))
        self._add_std_figure_formatting("Hz", "dB")
        plt.ylim((-30, 1))
        plt.xlim(0, self.data.carrier_freq * 2)
        plt.tight_layout()
        self._save_plt("filter")

    def _make_error_plots(self):
        plt.figure()
        time = self._system.timeline
        demod = self._system.get_block(self._system.DEMODULATOR)
        mod = self._system.get_block(self._system.MODULATOR)
        error = demod.output - mod.input
        plt.semilogy(time, error)
        self._add_std_figure_formatting('s', 'V')
        plt.title(self._build_title("Wykres błędu demodulacji"))
        self._save_plt("error")

    def _plot_single_spectrum(self, signal, style=None):
        f, amp = self._compute_spectrum_for_plot(signal)
        args = [style] if style else []
        plt.plot(f, amp, *args)
        self._format_spectrum()

    def _format_spectrum(self):
        yLimit = -70
        plt.xlim(0, utils.DataLoader().carrier_freq * 2)
        plt.ylim((yLimit, 0))
        self._add_std_figure_formatting('Hz', 'dB')


    def _compute_spectrum_for_plot(self, signal):
        sampling_freq = self._system.sampling_frequency
        samples_count = len(signal)
        yf = np.fft.fft(signal)
        xf = np.fft.fftfreq(samples_count, 1 / sampling_freq)
        xf = np.fft.fftshift(xf)
        yplot = 1.0 / samples_count * np.fft.fftshift(yf)
        return xf, 20 * np.log10(np.abs(yplot))

    def _add_std_figure_formatting(self, x_unit, y_unit):
        # pylint: disable=no-self-use
        x_formatter = ticker.EngFormatter(unit=x_unit)
        y_formatter = ticker.EngFormatter(unit=y_unit)
        x_formatter.ENG_PREFIXES[-6] = 'u'
        y_formatter.ENG_PREFIXES[-6] = 'u'
        ax = plt.gca()
        ax.xaxis.set_major_formatter(x_formatter)
        ax.yaxis.set_major_formatter(y_formatter)
        plt.grid('on', which='both')

    def _save_plt(self, filename):
        for ext in ['png', 'svg']:
            full_filename = os.path.extsep.join((filename, ext))
            full_filename = "%02d%s" % (self._plot_counter, full_filename)
            plt.savefig(os.path.join(self._output_dir, full_filename))

    def _build_title(self, title):
        self._plot_counter += 1
        prefix = "Wykres {0}.".format(self._plot_counter)
        return " ".join((prefix, title))
