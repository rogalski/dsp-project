import numpy as np
import scipy.signal

from blocks.meta import AbstractBlock


class FrequencyDemodulator(AbstractBlock):
    def __init__(self):
        super(FrequencyDemodulator, self).__init__()

    def _compute(self):
        i = self._input
        q = scipy.signal.hilbert(self._input).imag
        d = np.arctan2(q, i)
        self._output = np.append([0], np.diff(d))
        # self._output = d
