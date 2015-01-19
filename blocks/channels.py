import numpy as np

from blocks.meta import AbstractBlock


class MultiPathChannel(AbstractBlock):
    def __init__(self, delay=120, paths=5):
        super(MultiPathChannel, self).__init__()
        self._init_impulse_response(delay, paths)

    def _init_impulse_response(self, delay, paths):
        rng = 4
        imp = np.zeros(delay * paths)
        for p in range(paths):
            val = 1 if p == 0 else np.random.randint(-rng, rng) / 10
            imp[delay * p] = val
        self._impulse_response = imp

    def _compute(self):
        out = np.convolve(self._impulse_response, self._input)
        self._output = out[0:self._input.size]
