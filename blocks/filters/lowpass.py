import scipy.signal as signal

from blocks.abstract_block import AbstractBlock


class LowPassFilter(AbstractBlock):
    def _compute(self):
        filter_order = 4
        cutoff_freq = self._get_cutoff_frequency()
        b, a = signal.butter(filter_order, cutoff_freq, output='ba')
        self._output = signal.filtfilt(b, a, self._input)

    def _get_cutoff_frequency(self):
        return 50 / 125
