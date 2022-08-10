#!/usr/bin/env python3
# Converts given pay amounts between different time units
# For example, if a job lists itself as $20 an hour,
# The output for month would be 20 * 40 * 4.3, or
# 3440.00 for a month's pay.
# If nothing is passed, returns help.
# If only a number is passed, returns a "best guess" of all 
# conversions, assuming 0-120 (inc) is hourly, 120.01-12000 is monthly,
# and all values above are yearly pay, based on first number passed.
#
# Usage: paycon [-h, --help] [-i, --in-unit hwmy] [-e, --WeeklyHours N] N [N..]

import argparse

def main():
    """Take in arguments, handle conversions"""
    arguments = process_arguments()
    value = 60000 # Remove this later
    in_unit = None # Remove this later
    if in_unit == None:
        in_unit = autoselect(value) # Chooses in-unit if none passed
    conversion = convert(in_unit=in_unit, value=value)
    display(conversion, in_unit, value)

def process_arguments() -> argparse.ArgumentParser.parse_args:
    """Create the parser object based on arguments"""
    # Using Anthon's SmartFormatter - check class at bottom
    parser = argparse.ArgumentParser(description= \
            "Converts pay value for different time units.  If no time unit "
            "passed, guesses unit based on 0-120 for hour, 120.01-12000 for "
            "month, and 12000.01+ for year.")
    parser.add_argument('-t', '--time-unit', metavar='unit', type=str, nargs=1, \
            help='time unit for the passed pay amount(s)')
    parser.add_argument('-e', '--weekly-hours', metavar='hours', type=float, nargs=1, \
            help='number of hours worked per week (default: 40)')
    parser.add_argument('pay_rate', metavar='rate', type=float, nargs='+', \
                        help='amount paid per time period')
    arguments = parser.parse_args()
    return arguments

def convert(value: float, in_unit: str='hour', work_week: float=40,\
            overtime: float=40) -> dict:
    """Takes:
        in_unit - input unit of time to be converted
        value - value of time per input unit (pay)
        work_week - number of hours worked (per week)
        overtime - number of hours above which overtime starts
    """
    # These variables will be necessary for later calculations
    # There are exactly 52 weeks and one day in a year
    weeks_per_year = 52 + 1/7
    months_per_year = 12
    # This is an average - actual weeks per month varies
    weeks_per_month = weeks_per_year / months_per_year
    hours_per_month = work_week * weeks_per_month
    
    # Determine hourly pay rate
    if in_unit == 'hour':
        hourly = value
    elif in_unit == 'week':
        hourly = value / work_week
    elif in_unit == 'month':
        hourly = value / hours_per_month
    elif in_unit == 'year':
        hourly = value / months_per_year / hours_per_month
    else:
        raise Exception("Not a valid time unit")

    # Create a lookup dictionary to calculate out unit from hourly rate
    out_units = {'hour': hourly,
                 'week': hourly * work_week,
                 'month': hourly * work_week * weeks_per_month,
                 'year': hourly * months_per_year * \
                      work_week * weeks_per_month}

    return out_units

def autoselect(value: float) -> str:
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

def display(conversion: dict, in_unit: str, value: float, \
            out_units: str='dwmy') -> None:
    print(f'Output for a {in_unit} at a pay rate of ${value}')
    for key in conversion:
        key_value = conversion[key]
        print(key + "ly: " + f'${key_value:,.2f}')


if __name__ == "__main__":
    main()
