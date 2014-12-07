import abc

import numpy as np
import scipy.signal

from blocks.meta import AbstractBlock
import utils


class FrequencyModem(AbstractBlock):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(FrequencyModem, self).__init__()
        self._carrier_frequency = None
        self._frequency_deviation = None

    @property
    def carrier_frequency(self):
        return self._carrier_frequency

    @carrier_frequency.setter
    def carrier_frequency(self, freq):
        if freq != self._carrier_frequency:
            self._carrier_frequency = freq
            self._invalidate()

    @property
    def frequency_deviation(self):
        return self._frequency_deviation

    @frequency_deviation.setter
    def frequency_deviation(self, deviation):
        if deviation != self._frequency_deviation:
            self._frequency_deviation = deviation
            self._invalidate()

    @abc.abstractmethod
    def _compute(self):
        raise NotImplementedError


class FrequencyDemodulator(FrequencyModem):
    def _compute(self):
        frequencies = self._compute_instantaneous_frequencies()
        without_carrier = frequencies - self._carrier_frequency
        normalized = without_carrier / self._frequency_deviation
        self._output = normalized

    def _compute_instantaneous_frequencies(self):
        hilbert = scipy.signal.hilbert(self._input)
        phase = np.unwrap(np.angle(hilbert))
        diffs = np.diff(phase) / (2 * np.pi * self._get_time_step())
        return np.append(diffs, diffs[-1])  # align for samples count

    def __repr__(self):
        template = "Frequency Demodulator (carrier {0}Hz, deviation {1}Hz)"
        return template.format(self._carrier_frequency,
                               self._frequency_deviation)


class FrequencyModulator(FrequencyModem):
    def __init__(self):
        super(FrequencyModulator, self).__init__()
        self._time = None
        self._carrier = None

    @property
    def carrier(self):
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
