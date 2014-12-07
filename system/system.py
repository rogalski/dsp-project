from blocks.meta import AbstractBlock


class System(object):  # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self._blocks = []
        self._sampling_frequency = 0

    def __iter__(self):
        return self._blocks.__iter__()

    def __repr__(self):
        return " ".join((super(System, self).__repr__(),
                         str(self._blocks)))

    def get_blocks(self):
        return self._blocks

    def append_block(self, block):
        if not isinstance(block, AbstractBlock):
            e = "Bad block. Expected {0}. Found {1}".format(AbstractBlock,
                                                            type(block))
            raise TypeError(e)
        self._blocks.append(block)

    def simulate(self):
        self._connect_blocks()

    def _connect_blocks(self):
        for previous_block, next_block in zip(self._blocks[:-1],
                                              self._blocks[1:]):
            next_block.input = previous_block.output

    @property
    def sampling_frequency(self):
        return self._sampling_frequency

    @sampling_frequency.setter
    def sampling_frequency(self, freq):
        self._sampling_frequency = freq
        for block in self._blocks:
            try:
                block.sampling_frequency = freq
            except AttributeError:
                pass

    @property
    def timeline(self):
        if not self._blocks:
            return None
        return self._blocks[0].input

    def get_block(self, pos):
        return self._blocks[pos]
