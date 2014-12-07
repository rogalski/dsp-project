import numpy as np

from blocks.meta import NullBlock


def freq_to_omega(freq):
    return 2 * np.pi * freq


class DataLoader(object):
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
        self.freq_deviation = 2.41e6
        self.generation_time = 1 / self.modulating_freq
        self.sampling_freq = 64 * self.carrier_freq
        self.expected_snr = 80

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
        self.carrier_freq = int(input("Carrier Freq [Hz] = "))

    def _load_modulating_freq(self):
        self.modulating_freq = int(input("Modulating Freq [Hz] = "))

    def _load_freq_deviation(self):
        self.freq_deviation = int(input("Freq Deviation [Hz] = "))

    def _load_sampling_freq(self):
        freq = input("Sampling Freq [Hz] (empty = 128*carrier_freq) = ")
        self.sampling_freq = int(freq) if freq else 128 * self.carrier_freq

    def _load_generation_time(self):
        time = input("Generation Time [s] (default = 4/modulating_freq) = ")
        self.generation_time = int(time) if time else 4 / self.modulating_freq

    def _load_expected_snr(self):
        self.expected_snr = int(input("Expected SNR [dB] = "))

    def _validate(self):
        if self.modulating_freq / self.carrier_freq > MUCH_LOWER:
            error = "Modulating freq should be much lower than carrier."
            raise BadDataException(error)

        if self.freq_deviation > self.carrier_freq:
            error = "Frequency deviation should be lower than carrier freq."
            raise BadDataException(error)


MUCH_LOWER = 0.05


class BadDataException(Exception):
    pass


def ignore_block(func):
    # Decorate maker with it to make NullBlock instead of functional
    # pylint: disable=unused-argument
    return lambda *args, **kwargs: NullBlock()
