import numpy as np

from blocks.meta import AbstractBlock


class Generator(AbstractBlock):
    def __init__(self):
        super(Generator, self).__init__()
        self._generation_time = 0
        self._amplitude = 1
        self._offset = 0

    # known issue #30 @ https://bitbucket.org/logilab/pylint/
    # pylint: disable=arguments-differ
    @property
    def input(self):
        return super(Generator, self).input

    @input.setter
    def input(self, value):
        err = "Input {} cannot be explicitly set for generator.".format(value)
        raise ValueError(err)

    @property
    def generation_time(self):
        return self._generation_time

    @generation_time.setter
    def generation_time(self, time):
        if time != self._generation_time:
            self._generation_time = time
            self._invalidate()

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, amplitude):
        if amplitude != self._amplitude:
            self._amplitude = amplitude
            self._invalidate()

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if offset != self._offset:
            self._offset = offset
            self._invalidate()

    def _compute(self):
        self._compute_time()
        self._compute_signal()
        self._validate()

    def _compute_time(self):
        start = 0
        stop = self._generation_time
        step = 1.0 / self._sampling_frequency
        self._input = np.arange(start, stop, step)

    def _compute_signal(self):
        raise NotImplementedError


class OscillatingGenerator(Generator):
    def __init__(self):
        super(OscillatingGenerator, self).__init__()
        self._frequency = None

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if frequency != self._frequency:
            self._frequency = frequency
            self._invalidate()

    def _compute_signal(self):
        raise NotImplementedError


class SineGenerator(OscillatingGenerator):
    def _compute_signal(self):
        omega = 2 * np.pi * self._frequency
        sine = np.sin(omega * self._input)
        self._output = self._amplitude * sine + self._offset

    def __repr__(self):
        return "Sine Generator ({0}Hz)".format(self._frequency)


class SquareGenerator(OscillatingGenerator):
    def __init__(self):
        super(SquareGenerator, self).__init__()
        self.__offset = -0.5

    def _compute_signal(self):
        step = 1 / self._frequency
        square = (self._input % step < (step / 2)).astype(float)
        self._output = self._amplitude * square + self.__offset

    def __repr__(self):
        return "Square Generator ({0}Hz)".format(self._frequency)


class SawGenerator(OscillatingGenerator):
    def __init__(self):
        super(SawGenerator, self).__init__()
        self.__offset = -0.5

    def _compute_signal(self):
        saw = (self._input % (1 / self._frequency)) * self._frequency
        self._output = self._amplitude * saw + self.__offset

    def __repr__(self):
        return "Square Generator ({0}Hz)".format(self._frequency)
