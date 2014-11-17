import numpy as np

from blocks.abstract_block import AbstractBlock


class WhiteNoiser(AbstractBlock):
    def __init__(self):
        super(WhiteNoiser, self).__init__()
        self._expected_snr = 20
        self._noise = None

    def get_snr(self):
        mean = np.mean(self._input)
        power_signal = np.sum((self._input - mean) ** 2)
        power_noise = np.sum(self._noise ** 2)
        return 10 * np.log10(power_signal / power_noise)

    def get_expected_snr(self):
        return self._expected_snr

    def set_expected_snr(self, snr):
        if snr != self._expected_snr:
            self._expected_snr = snr
            self._invalidate()

    def _compute(self):
        var = self._get_input_variance()
        sigma = np.sqrt(var) * (10 ** (-self._expected_snr / 20))
        self._noise = sigma * np.random.randn(len(self._input))
        self._output = self._input + self._noise

    def _get_input_variance(self):
        length = len(self._input)
        average = np.mean(self._input)
        return np.sum(np.abs(self._input - average) ** 2) / length
