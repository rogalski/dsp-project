import numpy as np

from blocks.meta import AbstractBlock


class Noiser(AbstractBlock):
    def __init__(self):
        super(Noiser, self).__init__()
        self._expected_snr = 20
        self._noise = None

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

    def _compute(self):
        var = self._get_input_variance()
        sigma = np.sqrt(var) * (10 ** (-self._expected_snr / 20))
        self._noise = sigma * np.random.randn(self._input.size)
        self._output = self._input + self._noise

    def _get_input_variance(self):
        length = self._input.size
        average = np.mean(self._input)
        return np.sum(np.abs(self._input - average) ** 2) / length

    @property
    def noise(self):
        return self._noise
