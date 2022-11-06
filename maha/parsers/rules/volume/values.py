from maha.parsers.templates import Value, VolumeUnit
from maha.rexy import non_capturing_group

from ..common import TWO_SUFFIX, ValueUnit

ONE_CUBICMETER = Value(ValueUnit(1, VolumeUnit.CUBICMETERS), "متر مكعب")
TWO_CUBICMETERS = Value(ValueUnit(2, VolumeUnit.CUBICMETERS), "متر" + TWO_SUFFIX)
SEVERAL_CUBICMETERS = Value(
    ValueUnit(1, VolumeUnit.CUBICMETERS), non_capturing_group("مترات", "[أا]متار")
)
