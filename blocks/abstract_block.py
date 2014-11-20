class AbstractBlock(object):
    def __init__(self):
        self._input = None
        self._output = None
        self._sampling_frequency = 0
        self._is_valid = False

    def get_input(self):
        return self._input

    def set_input(self, value):
        if value != self._input:
            self._input = value
            self._invalidate()

    def get_output(self):
        if not self._is_valid:
            self._process()
        return self._output

    def get_sampling_frequency(self):
        return self._sampling_frequency

    def set_sampling_frequency(self, value):
        if value != self._sampling_frequency:
            self._sampling_frequency = value
            self._invalidate()

    def _process(self):
        self._compute()
        self._validate()

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
