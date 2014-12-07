import abc


class AbstractBlock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._input = None
        self._output = None
        self._sampling_frequency = 0
        self._is_valid = False

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        if value != self._input:
            self._input = value
            self._invalidate()

    @property
    def output(self):
        if not self._is_valid:
            self._process()
        return self._output

    @property
    def sampling_frequency(self):
        return self._sampling_frequency

    @sampling_frequency.setter
    def sampling_frequency(self, value):
        if value != self._sampling_frequency:
            self._sampling_frequency = value
            self._invalidate()

    def _process(self):
        self._compute()
        self._validate()

    @abc.abstractmethod
    def _compute(self):
        raise NotImplementedError

    def _invalidate(self):
        self._is_valid = False

    def _validate(self):
        self._is_valid = True

    def _get_time_step(self):
        try:
            return 1 / self._sampling_frequency
        except (TypeError, ZeroDivisionError):
            return 0


class NullBlock(AbstractBlock):
    def _compute(self):
        self._output = self._input
