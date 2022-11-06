"""Rules to extract volume"""
from __future__ import annotations

__all__ = ["RULE_VOLUME"]

from maha.parsers.rules.numeral.rule import RULE_NUMERAL, parse_numeral
from maha.parsers.templates import FunctionValue
from maha.rexy import ExpressionGroup, named_group, non_capturing_group

from ..common import (
    FRACTIONS,
    combine_patterns,
    get_fractions_of_unit_pattern,
    spaced_patterns,
    wrap_pattern,
)
from .template import VolumeValue
from .values import *


def get_pattern(singular_frac_group, singular, all_units, dual=None):
    """Get regex pattern for volume."""
    if dual:
        return non_capturing_group(
            spaced_patterns(RULE_NUMERAL, all_units),
            named_group(
                "fractions", get_fractions_of_unit_pattern(singular_frac_group)
            ),
            dual,
            singular,
        )

    return non_capturing_group(
        spaced_patterns(RULE_NUMERAL, all_units),
        named_group("fractions", get_fractions_of_unit_pattern(singular_frac_group)),
        singular,
    )


def get_unit_fraction_value(matched_text):
    val1, val2 = matched_text.split(" ", 1)
    fraction = FRACTIONS.get_matched_expression(val1)
    if not fraction:
        fraction = FRACTIONS.get_matched_expression(val2)
        value = get_matched_value(val1)
    else:
        value = get_matched_value(val2)
    value.value = fraction.value  # type: ignore
    return value


UnitsGroup = ExpressionGroup(ONE_CUBICMETER, TWO_CUBICMETERS, SEVERAL_CUBICMETERS)


def get_matched_value(matched_text) -> ValueUnit:
    exp_val = UnitsGroup.get_matched_expression(matched_text).value  # type: ignore
    return ValueUnit(value=exp_val.value, unit=exp_val.unit)


def get_groups():
    return ["cubic_meters"]


def parse_volume(match):
    """Parse volume."""
    groups = match.capturesdict()

    volume_groups = get_groups()
    if groups.get("fractions"):
        value = get_unit_fraction_value(groups.get("fractions")[0])
        return VolumeValue(value)
    matched_group = [
        groups.get(group)[0] for group in volume_groups if groups.get(group)
    ][0]

    valueunit = get_matched_value(matched_group)
    numeral = parse_numeral(match)
    if numeral:
        valueunit.value = numeral
    return VolumeValue(valueunit)


_cubicmeters = named_group(
    "cubicmeters",
    non_capturing_group(ONE_CUBICMETER, TWO_CUBICMETERS, SEVERAL_CUBICMETERS),
)

all_units = non_capturing_group(
    _cubicmeters,
)

dual_units = non_capturing_group(
    named_group("cubicmeters", TWO_CUBICMETERS),
)
singular_units = non_capturing_group(
    named_group("cubicmeters", ONE_CUBICMETER),
)
RULE_VOLUME_CUBICMETERS = FunctionValue(
    parse_volume,
    combine_patterns(
        get_pattern(
            ONE_CUBICMETER,
            named_group("cubicmeters", ONE_CUBICMETER),
            _cubicmeters,
            named_group("cubicmeters", TWO_CUBICMETERS),
        )
    ),
)

RULE_VOLUME = FunctionValue(
    parse_volume,
    wrap_pattern(
        get_pattern(
            non_capturing_group(
                ONE_CUBICMETER,
            ),
            singular_units,
            all_units,
            dual_units,
        ),
    ),
)
