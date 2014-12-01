import numpy as np

import utils
from blocks.meta import AbstractBlock


class FrequencyModulator(AbstractBlock):
    def __init__(self):
        super(FrequencyModulator, self).__init__()
        self._carrier_frequency = None
        self._frequency_deviation = None

        self._time = None
        self._carrier = None

    def get_carrier_frequency(self):
        return self._carrier_frequency

    def set_carrier_frequency(self, freq):
        if freq != self._carrier_frequency:
            self._carrier_frequency = freq
            self._invalidate()

    def get_frequency_deviation(self):
        return self._frequency_deviation

    def set_frequency_deviation(self, deviation):
        if deviation != self._frequency_deviation:
            self._frequency_deviation = deviation
            self._invalidate()

    def get_carrier(self):
        return self._carrier

    def _compute(self):
        self._compute_time()
        self._compute_carrier()
        self._compute_output()

    def _compute_time(self):
        self._time = np.arange(0, len(self._input) / self._sampling_frequency,
                               self._get_time_step())

    def _compute_carrier(self):
        omega = utils.freq_to_omega(self._carrier_frequency)
        self._carrier = np.sin(omega * self._time)

    def _compute_output(self):
        omega = utils.freq_to_omega(self._carrier_frequency)
        omega_dev = utils.freq_to_omega(self._frequency_deviation)
        ph = np.cumsum(self._get_normalized_input()) / self._sampling_frequency
        self._output = np.sin(omega * self._time + omega_dev * ph)

    def _get_normalized_input(self):
        return self._input / np.max(np.abs(self._input))

    def __repr__(self):
        template = "Frequency Modulator (carrier {0}Hz, deviation {1}Hz)"
        return template.format(self._carrier_frequency,
                               self._frequency_deviation)
