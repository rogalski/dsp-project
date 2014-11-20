import numpy as np


def freq_to_omega(freq):
    return 2 * np.pi * freq


class DataLoader(object):
    _instance = None

    carrier_freq = None
    modulating_freq = None
    freq_deviation = None
    generation_time = None
    expected_snr = None
    sampling_freq = None

    def __new__(cls, *args, **kwargs):
        # singleton pattern
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def mock(self):
        self.carrier_freq = 50e6
        self.modulating_freq = 10e6
        self.freq_deviation = 20e6
        self.generation_time = 2 / self.modulating_freq
        self.sampling_freq = 250 * self.carrier_freq
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
        print(dir(self))
        if self.modulating_freq / self.carrier_freq > MUCH_LOWER:
            raise BadDataException("Modulating freq should be much lower than carrier.")

        if self.freq_deviation > self.carrier_freq:
            raise BadDataException("Frequency deviation should be not bigger than carrier freq.")


MUCH_LOWER = 0.05


class BadDataException(Exception):
    pass


