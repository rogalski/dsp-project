import scipy.signal as signal

from blocks.meta import AbstractBlock


class BandPassFilter(AbstractBlock):
    def __init__(self):
        super(BandPassFilter, self).__init__()
        self._freqs = None
        self._b = None
        self._a = None

    def _compute(self):
        self._compute_filter_coefficients()
        self._output = signal.filtfilt(self._b, self._a, self._input)

    def _compute_filter_coefficients(self):
        filter_order = 4
        cutoff_omegas = self._get_normalized_cutoff_omegas()
        print("Filter cutoff omegas", cutoff_omegas)
        coefficients = signal.butter(filter_order, cutoff_omegas,
                                     output='ba', btype='bandpass',
                                     analog=False)
        self._b = coefficients[0]
        self._a = coefficients[1]

    @property
    def freqs(self):
        return self._freqs

    @freqs.setter
    def freqs(self, freqs):
        if freqs != self._freqs:
            self._freqs = freqs
            self._invalidate()

    @property
    def coefficients(self):
        return self._b, self._a

    def _get_normalized_cutoff_omegas(self):
        return [2 * f / self._sampling_frequency
                for f in self._freqs]
