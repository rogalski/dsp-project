import scipy.signal as signal

from blocks.meta import AbstractBlock


class LowPassFilter(AbstractBlock):
    def _compute(self):
        filter_order = 4
        cutoff_freq = self.cutoff_frequency
        # pylint: disable=unbalanced-tuple-unpacking
        b, a = signal.butter(filter_order, cutoff_freq, output='ba')
        self._output = signal.filtfilt(b, a, self._input)

    @property
    def cutoff_frequency(self):
        # pylint: disable=no-self-use
        return 0.35
