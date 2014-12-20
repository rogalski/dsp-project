import numpy as np

from blocks.meta import AbstractBlock


class MultiPathChannel(AbstractBlock):
    delay = 10
    multiplier = 0.02

    def __init__(self, delay=delay, multiplier=multiplier):
        super(MultiPathChannel, self).__init__()
        self.delay = delay
        self.multiplier = multiplier

    def _compute(self):
        delayed_signal = np.append(np.zeros((1, self.delay)),
                                   self._input[self.delay:])
        self._output = self._input + self.multiplier * delayed_signal
