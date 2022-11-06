from __future__ import annotations

__all__ = ["VolumeValue"]


from dataclasses import dataclass, field

from maha.parsers.templates import VolumeUnit

from ..common import ValueUnit


@dataclass
class VolumeValue:

    valueunit: ValueUnit
    normalized_unit: VolumeUnit = field(default=VolumeUnit.CUBICMETERS, repr=False)

    @property
    def value(self):
        return self.valueunit.value

    @property
    def unit(self):
        return self.valueunit.unit

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value}, unit={self.unit})"
