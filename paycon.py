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
    try:
        value, time_unit, hours = process_arguments()
    except Exception as e:
        print(str(e))
    else:
        conversion = convert(value, time_unit, hours)
        display(conversion, time_unit, value)

def process_arguments() -> argparse.ArgumentParser.parse_args:
    """
    Processes arguments for necessary conversions
    Returns
    tuple in the shape "float value, unit string, float weekly hours"
    """
    parser = argparse.ArgumentParser(description= \
            "Converts pay value for different time units.  If no time unit "
            "passed, guesses unit based on 0-120 for hour, 120.01-12000 for "
            "month, and 12000.01+ for year.")
    parser.add_argument('-t', '--time-unit', metavar='unit', nargs=1, \
            help='time unit for the passed pay amount(s)')
    parser.add_argument('-w', '--working-hours', metavar='hours', type=float, nargs=1, \
            help='number of hours worked per week (default: 40)')
    parser.add_argument('pay_rate', metavar='rate', type=float, nargs='+', \
                        help='amount paid per time period')
    arguments = parser.parse_args()

    #
    # Assigning value
    #
    value = arguments.pay_rate[0]
    
    #
    # Assigning time_unit
    #
    if arguments.time_unit is not None:
        unit = arguments.time_unit[0]
    else:
        unit = None

    # value is a required argument at the command level
    # since these are not, confirming assignment
    if unit == None:
        time_unit = autoselect_unit(value)
    elif unit[0] == 'h':
        time_unit = 'hour'
    elif unit[0] == 'w':
        time_unit = 'week'
    elif unit[0] == 'm':
        time_unit = 'month'
    elif unit[0] == 'y':
        time_unit = 'year'
    else:
        raise Exception(f"{unit} not a valid time unit.  Please use (h)our,"
                        f" (w)eek, (m)onth, or (y)ear")
    
    #
    # Assigning weekly_hours
    #
    if arguments.working_hours is not None:
        working_hours = arguments.working_hours[0]
    else:
        working_hours = 40.0

    return value, time_unit, working_hours

def convert(value: float, time_unit: str='hour', work_week: float=40) -> dict:
    """Takes:
        time_unit- input unit of time to be converted
        value - value of time per input unit (pay)
        work_week - number of hours worked (per week)
        Returns:
        Dictionary of pay for each time unit, with units as keys
        and pay amount as values.
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
                 'year': hourly * months_per_year * \
                      work_week * weeks_per_month}

    return out_units

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

def display(conversion: dict, time_unit: str, value: float, \
            out_units: str='dwmy') -> None:
    print(f'Output for a {time_unit} at a pay rate of ${value}')
    for key in conversion:
        key_value = conversion[key]
        print(key + "ly: " + f'${key_value:,.2f}')

if __name__ == "__main__":
    main()
