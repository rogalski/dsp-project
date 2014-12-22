import ast

import numpy as np

from blocks.meta import NullBlock


def freq_to_omega(freq):
    return 2 * np.pi * freq


class DataLoader(object):
    MUCH_LOWER = 0.5

    _inst = None

    carrier_freq = None
    modulating_freq = None
    freq_deviation = None
    generation_time = None
    expected_snr = None
    sampling_freq = None

    def __new__(cls):
        # singleton pattern
        if cls._inst is None:
            cls._inst = super(DataLoader, cls).__new__(cls)
        return cls._inst

    def mock(self):
        self.carrier_freq = 50e6
        self.modulating_freq = 10e6
        self.freq_deviation = 2.41 * self.modulating_freq
        self.generation_time = 4 / self.modulating_freq
        self.sampling_freq = 64 * self.carrier_freq
        self.expected_snr = 15

    def load_via_stdin(self):
        self._load_data()
        self._validate()

    def _load_data(self):
        self._load_carrier_freq()
        self._load_modulating_freq()
        self._load_freq_deviation()
        self._load_sampling_freq()
        self._load_generation_time()
        self._load_expected_snr()

    def _load_carrier_freq(self):
        raw = input("Carrier Freq [Hz] = ")
        self.carrier_freq = ast.literal_eval(raw)

    def _load_modulating_freq(self):
        raw = input("Modulating Freq [Hz] = ")
        self.modulating_freq = ast.literal_eval(raw)

    def _load_freq_deviation(self):
        raw = input("Freq Deviation [Hz] = ")
        self.freq_deviation = ast.literal_eval(raw)

    def _load_sampling_freq(self):
        freq = input("Sampling Freq [Hz] (empty = 64*carrier_freq) = ")
        if freq:
            self.sampling_freq = ast.literal_eval(freq)
        else:
            self.sampling_freq = 64 * self.carrier_freq

    def _load_generation_time(self):
        time = input("Generation Time [s] (default = 4/modulating_freq) = ")
        if time:
            self.generation_time = ast.literal_eval(time)
        else:
            self.generation_time = 4 / self.modulating_freq

    def _load_expected_snr(self):
        snr = input("Expected SNR [dB] = ")
        self.expected_snr = ast.literal_eval(snr)

    def _validate(self):
        if self.modulating_freq / self.carrier_freq > self.MUCH_LOWER:
            error = "Modulating freq should be much lower than carrier."
            raise BadDataException(error)

        if self.freq_deviation > self.carrier_freq:
            error = "Frequency deviation should be lower than carrier freq."
            raise BadDataException(error)


class BadDataException(Exception):
    pass


def ignore_block(func):
    # Decorate maker with it to make NullBlock instead of functional
    # pylint: disable=unused-argument
    return lambda *args, **kwargs: NullBlock()
