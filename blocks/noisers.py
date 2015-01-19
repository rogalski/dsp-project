import numpy as np
from scipy import signal

from blocks.meta import AbstractBlock


class BandNoiser(AbstractBlock):
    def __init__(self):
        super(BandNoiser, self).__init__()
        self._expected_snr = 20
        self._noise = None
        self._freqs = None

    @property
    def actual_snr(self):
        mean = np.mean(self._input)
        power_signal = np.sum((self._input - mean) ** 2)
        power_noise = np.sum(self._noise ** 2)
        return 10 * np.log10(power_signal / power_noise)

    @property
    def expected_snr(self):
        return self._expected_snr

    @expected_snr.setter
    def expected_snr(self, snr):
        if snr != self._expected_snr:
            self._expected_snr = snr
            self._invalidate()

    @property
    def freqs(self):
        return self._freqs

    @freqs.setter
    def freqs(self, freqs):
        if freqs != self._freqs:
            self._freqs = freqs
            self._invalidate()

    def _compute(self):
        self._compute_base_noise()
        self._limit_noise_bandwidth()
        self._rescale_noise()
        self._output = self._input + self._noise

    def _compute_base_noise(self):
        var = self._get_input_variance()
        sigma = np.sqrt(var) * (10 ** (-self._expected_snr / 20))
        self._noise = sigma * np.random.randn(self._input.size)

    def _limit_noise_bandwidth(self):
        if not self.freqs:
            return
        omegas = self._get_normalized_cutoff_omegas()
        b, a = signal.butter(4, omegas, btype='bandpass')
        self._noise = signal.lfilter(b, a, self._noise)

    def _rescale_noise(self):
        snr_difference = self.actual_snr - self.expected_snr
        self._noise *= 10 ** (snr_difference / 20)

    def _get_input_variance(self):
        length = self._input.size
        average = np.mean(self._input)
        return np.sum(np.abs(self._input - average) ** 2) / length

    @property
    def noise(self):
        return self._noise

    def _get_normalized_cutoff_omegas(self):
        return [2 * f / self._sampling_frequency
                for f in self._freqs]