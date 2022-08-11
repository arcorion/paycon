#!/usr/bin/env python3
# Converts given pay amounts between different time units
# For example, if a job lists itself as $20 an hour,
# The output for month would be 20 * 40 * 4.3, or
# 3440.00 for a month's pay.
# If nothing is passed, returns help.
# If only a number is passed, returns a "best guess" of all
# conversions, assuming 0-120 (inc) is hourly, 120.01-12000 is monthly,
# and all values above are yearly pay, based on first number passed.

import argparse


def main():
    """
    Converts passed arguments to amount of pay for a list of
    possible time units and displays results
    """
    values, time_unit, hours = process_arguments()
    if time_unit == '':
        print("Invalid time unit.  Use (h)our, (w)eek, (m)onth),"
              "or (y)ear.")
        return

    # List of tuples, (value, conversion dict)
    conversions = []
    for value in values:
        conversions.append(convert(value, time_unit, hours))

    display(conversions, time_unit, hours)


def process_arguments() -> tuple:
    """
    Processes arguments for necessary conversions
    Returns
    tuple in the shape "float value, unit string, float weekly hours"
    """
    parser = argparse.ArgumentParser(
        description="Converts pay value for different time units.  If no time "
                    "unit passed, guesses unit based on 0-120 for hour, "
                    "120.01-12000 for month, and 12000.01+ for year.")
    parser.add_argument('-t', '--time-unit', metavar='unit', nargs=1,
                        help='time unit for the passed pay amount(s)')
    parser.add_argument('-w', '--working-hours', metavar='hours', type=float,
                        nargs=1,
                        help='number of hours worked per week (default: 40)')
    parser.add_argument('pay_rate', metavar='rate', type=float, nargs='+',
                        help='amount paid per time period')
    arguments = parser.parse_args()

    values = []
    for rate in arguments.pay_rate:
        values.append(rate)

    if arguments.time_unit is None:
        time_unit = autoselect_unit(values[0])
    else:
        time_unit = arguments.time_unit[0]

        if time_unit == 'h':
            time_unit = 'hour'
        elif time_unit == 'w':
            time_unit = 'week'
        elif time_unit == 'm':
            time_unit = 'month'
        elif time_unit == 'y':
            time_unit = 'year'
        else:
            time_unit = ''

    if arguments.working_hours is not None:
        working_hours = arguments.working_hours[0]
    else:
        working_hours = 40.0

    return values, time_unit, working_hours


def convert(value: float, time_unit, work_week: float) -> tuple:
    """Takes:
        time_unit- input unit of time to be converted
        value - value of time per input unit (pay)
        work_week - number of hours worked (per week)
        Returns:
        A tuple with the original value as the zeroeth element and a
        dictionary of units as keys and pay amount as values as the second.
    """
    # These variables will be necessary for later calculations
    # There are exactly 52 weeks and one day in a year
    weeks_per_year = 52 + 1/7
    months_per_year = 12
    # This is an average - actual weeks per month varies
    weeks_per_month = weeks_per_year / months_per_year
    hours_per_month = work_week * weeks_per_month

    # Determine hourly pay rate
    if time_unit == 'hour':
        hourly = value
    elif time_unit == 'week':
        hourly = value / work_week
    elif time_unit == 'month':
        hourly = value / hours_per_month
    elif time_unit == 'year':
        hourly = value / months_per_year / hours_per_month
    else:
        raise Exception(f"Not a valid time unit: {time_unit}")

    # Create a lookup dictionary to calculate out unit from hourly rate
    out_units = {'hour': hourly,
                 'week': hourly * work_week,
                 'month': hourly * work_week * weeks_per_month,
                 'year': hourly * months_per_year *
                 work_week * weeks_per_month}

    return (value, out_units)


def autoselect_unit(value: float) -> str:
    """
    Takes:
    value - pay amount
    Returns:
    String representing predicted type of in unit
    """
    # If only a number is passed, returns a "best guess" of all
    # conversions, assuming 0-120 (inc) is hourly, 120.01-12000 is monthly,
    # and all values above are yearly pay, based on first number passed.
    if value >= 0 and value <= 120:
        return 'hour'
    elif value > 120 and value <= 12000:
        return 'month'
    else:
        return 'year'


def display(conversions: list, time_unit: str, working_hours: float) -> None:
    print(f"{working_hours} work weeks, with {time_unit}ly inputs:")
    # Lines in order from title, hourly, weekly, monthly, yearly
    lines = ["in:  \t", "hourly\t", "weekly\t", "monthly\t", "yearly\t"]

    currency = '$'

    for conversion in conversions:
        value = conversion[0]
        amounts = conversion[1]

        lines[0] += f"{currency}{value:<20,.2f}"

        next_line = 1
        for amount in amounts.values():
            lines[next_line] += f"{currency}{amount:<20,.2f}"
            next_line += 1

    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
