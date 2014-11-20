from blocks.abstract_block import AbstractBlock


class System(object):
    def __init__(self):
        self._blocks = []
        self._sampling_frequency = 0

    def __iter__(self):
        return self._blocks.__iter__()

    def __repr__(self):
        return " ".join((super(System, self).__repr__(), str(self._blocks)))

    def get_blocks(self):
        return self._blocks

    def append_block(self, block):
        if not isinstance(block, AbstractBlock):
            e = "Bad block type. Expected {0}. Found {1}".format(AbstractBlock,
                                                                 type(block))
            raise TypeError(e)
        self._blocks.append(block)

    def simulate(self):
        self._connect_blocks()

    def _connect_blocks(self):
        for index, block in enumerate(self._blocks):
            if index == 0:
                continue
            block.set_input(self._blocks[index - 1].get_output())

    def get_sampling_frequency(self):
        return self._sampling_frequency

    def set_sampling_frequency(self, freq):
        self._sampling_frequency = freq
        for block in self._blocks:
            try:
                block.set_sampling_frequency(freq)
            except AttributeError:
                pass

    def get_timeline(self):
        if not self._blocks:
            return None
        return self._blocks[0].get_input()

    def get_block(self, pos):
        return self._blocks[pos]
