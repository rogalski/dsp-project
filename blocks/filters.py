import scipy.signal as signal

from blocks.meta import AbstractBlock


class LowPassFilter(AbstractBlock):
    def __init__(self):
        super(LowPassFilter, self).__init__()
        self._cutoff_frequency = None
        self._b = None
        self._a = None

    def _compute(self):
        self._compute_filter_coefficients()
        self._output = signal.filtfilt(self._b, self._a, self._input)

    def _compute_filter_coefficients(self):
        filter_order = 8
        cutoff_freq = self._get_normalized_cutoff_frequency()
        coeff = signal.butter(filter_order, cutoff_freq,
                              output='ba', btype='low', analog=False)
        self._b = coeff[0]
        self._a = coeff[1]

    @property
    def cutoff_frequency(self):
        return self._cutoff_frequency

    @cutoff_frequency.setter
    def cutoff_frequency(self, freq):
        if freq != self._cutoff_frequency:
            self._cutoff_frequency = freq
            self._invalidate()

    @property
    def coefficients(self):
        return self._b, self._a

    def _get_normalized_cutoff_frequency(self):
        return 8 * self._cutoff_frequency / self._sampling_frequency
