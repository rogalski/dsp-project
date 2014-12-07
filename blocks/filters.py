import scipy.signal as signal

from blocks.meta import AbstractBlock


class LowPassFilter(AbstractBlock):
    def __init__(self):
        super(LowPassFilter, self).__init__()
        self._cutoff_frequency = None

    def _compute(self):
        filter_order = 8
        cutoff_freq = self._get_normalized_cutoff_freq()
        # pylint: disable=unbalanced-tuple-unpacking
        b, a = signal.butter(filter_order, cutoff_freq,
                             output='ba', btype='low', analog=False)

        self._output = signal.filtfilt(b, a, self._input)

    @property
    def cutoff_frequency(self):
        return self._cutoff_frequency

    @cutoff_frequency.setter
    def cutoff_frequency(self, freq):
        if freq != self._cutoff_frequency:
            self._cutoff_frequency = freq
            self._invalidate()

    def _get_normalized_cutoff_freq(self):
        return 8 * self._cutoff_frequency / self._sampling_frequency
