# paycon
Pay converter - converts pay amounts between different time units

## Help
``
Converts pay value for different time units. If no time unit passed, guesses unit based on 0-120 for hour,
120.01-12000 for month, and 12000.01+ for year.

positional arguments:
  rate                  amount paid per time period

options:
  -h, --help            show this help message and exit
  -t unit, --time-unit unit
                        time unit for the passed pay amount(s)
  -w hours, --working-hours hours
                        number of hours worked per week (default: 40)
``
