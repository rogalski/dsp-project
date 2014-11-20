import matplotlib.pyplot as plt


class Plotter(object):
    def __init__(self, signal, sampling_frequency):
        self._signal = signal
        self._sampling_frequency = sampling_frequency

    def to_file(self, filename):
        self._make_plot()
        self._save_plot(filename)

    def _make_plot(self):
        raise NotImplementedError

    def _save_plot(self, filename):
        plt.savefig(filename)


class TimePlotter(Plotter):
    def _make_plot(self):
        plt.figure()
        plt.plot(self._signal)
        plt.grid(True, 'both')
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude [V]")

