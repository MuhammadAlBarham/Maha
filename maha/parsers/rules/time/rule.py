from ..common import combine_patterns
from .values import *


def get_combined_value(groups, expression):
    value = TimeValue()
    for group in groups:
        value += next(iter(expression.parse(group))).value
    return value


def parse_time(match):
    groups = match.capturesdict()

    _year = groups.get("years")
    _months = groups.get("months")
    _weeks = groups.get("weeks")
    _days = groups.get("days")
    _hours = groups.get("hours")
    _minutes = groups.get("minutes")
    _month_day = groups.get("month_day")
    _year_month = groups.get("year_month")

    value = TimeValue()

    if _month_day:
        value += get_combined_value(_month_day, month_day_expressions)
    if _year_month:
        value += get_combined_value(_year_month, year_month_expressions)
    if _year:
        value += get_combined_value(_year, years_expressions)
    if _weeks:
        value += get_combined_value(_weeks, weeks_expressions)
    if _days:
        value += get_combined_value(_days, days_expressions)
    if _months:
        value += get_combined_value(_months, months_expressions)
    if _hours:
        value += get_combined_value(_hours, hours_expressions)
    if _minutes:
        value += get_combined_value(_minutes, minutes_expressions)
    return value


years_expressions = ExpressionGroup(
    AFTER_N_YEARS,
    BEFORE_N_YEARS,
    LAST_TWO_YEARS,
    NEXT_TWO_YEARS,
    LAST_YEAR,
    NEXT_YEAR,
    NUMERAL_YEAR,
    ORDINAL_YEAR,
    THIS_YEAR,
)
months_expressions = ExpressionGroup(
    AFTER_N_MONTHS,
    BEFORE_N_MONTHS,
    AFTER_SPECIFIC_NEXT_MONTH,
    LAST_TWO_MONTHS,
    NEXT_TWO_MONTHS,
    LAST_MONTH,
    NEXT_MONTH,
    NEXT_SPECIFIC_MONTH,
    PREVIOUS_SPECIFIC_MONTH,
    BEFORE_SPECIFIC_PREVIOUS_MONTH,
    THIS_MONTH,
    SPECIFIC_MONTH,
)
weeks_expressions = ExpressionGroup(
    AFTER_N_WEEKS,
    BEFORE_N_WEEKS,
    LAST_TWO_WEEKS,
    NEXT_TWO_WEEKS,
    LAST_WEEK,
    NEXT_WEEK,
    THIS_WEEK,
)
days_expressions = ExpressionGroup(
    AFTER_N_DAYS,
    BEFORE_N_DAYS,
    AFTER_NEXT_WEEKDAY,
    PREVIOUS_WEEKDAY,
    NEXT_WEEKDAY,
    AFTER_TOMORROW,
    TOMORROW,
    YESTERDAY,
    LAST_DAY,
    LAST_SPECIFIC_DAY,
    BEFORE_PREVIOUS_WEEKDAY,
    BEFORE_YESTERDAY,
    THIS_DAY,
    WEEKDAY,
)
hours_expressions = ExpressionGroup(
    AFTER_N_HOURS,
    BEFORE_N_HOURS,
    LAST_TWO_HOURS,
    NEXT_TWO_HOURS,
    LAST_HOUR,
    NEXT_HOUR,
    NUMERAL_HOUR,
    ORDINAL_HOUR,
    THIS_HOUR,
)
minutes_expressions = ExpressionGroup(
    AFTER_N_MINUTES,
    BEFORE_N_MINUTES,
    LAST_TWO_MINUTES,
    NEXT_TWO_MINUTES,
    LAST_MINUTE,
    NEXT_MINUTE,
    NUMERAL_MINUTE,
    ORDINAL_MINUTE,
    THIS_MINUTE,
)

month_day_expressions = ExpressionGroup(
    ORDINAL_SPECIFIC_DAY,
    LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH,
    ORDINAL_AND_SPECIFIC_MONTH,
    ORDINAL_AND_THIS_MONTH,
    NUMERAL_AND_SPECIFIC_MONTH,
    NUMERAL_AND_THIS_MONTH,
)
year_month_expressions = ExpressionGroup(YEAR_WITH_MONTH)

years_group = named_group("years", years_expressions.join())
months_group = named_group("months", months_expressions.join())
weeks_group = named_group("weeks", weeks_expressions.join())
days_group = named_group("days", days_expressions.join())
hours_group = named_group("hours", hours_expressions.join())
minutes_group = named_group("minutes", minutes_expressions.join())
month_day_group = named_group("month_day", month_day_expressions.join())
year_month_group = named_group("year_month", year_month_expressions.join())

RULE_TIME_YEARS = FunctionValue(parse_time, combine_patterns(years_group))
RULE_TIME_MONTHS = FunctionValue(parse_time, combine_patterns(months_group))
RULE_TIME_WEEKS = FunctionValue(parse_time, combine_patterns(weeks_group))
RULE_TIME_DAYS = FunctionValue(parse_time, combine_patterns(days_group))
RULE_TIME_HOURS = FunctionValue(parse_time, combine_patterns(hours_group))
RULE_TIME_MINUTES = FunctionValue(parse_time, combine_patterns(minutes_group))
RULE_TIME_MONTH_DAY = FunctionValue(parse_time, combine_patterns(month_day_group))
RULE_TIME_YEAR_MONTH = FunctionValue(parse_time, combine_patterns(year_month_group))

RULE_TIME = FunctionValue(
    parse_time,
    combine_patterns(
        month_day_group,
        year_month_group,
        years_group,
        months_group,
        weeks_group,
        days_group,
        hours_group,
        minutes_group,
        seperator=TIME_WORD_SEPARATOR,
        combine_all=True,
    ),
)
