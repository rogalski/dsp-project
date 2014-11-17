from .abstract_block import AbstractBlock


class NullBlock(AbstractBlock):
    def _compute(self):
        self._output = self._input
