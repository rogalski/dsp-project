import numpy as np

from blocks.meta import AbstractBlock


class MultiPathChannel(AbstractBlock):
    delay = 10
    power = 0.02

    def _compute(self):
        delayed_signal = np.append(np.zeros((1, self.delay)),
                                   self._input[self.delay:])
        self._output = self._input + self.power * delayed_signal
