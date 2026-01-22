# paycon
Pay converter - converts pay amounts between different time units

## Installation/Requirements

To install, you can either clone this package or just download the raw paycon.py file.  Usage is typically something like:

    python paycon.py 40000
    
    or

    python3 paycon.py 30
    
    or
    
    ./paycon.py -w 20 -t h 18

If running on a Linux system, you'll need to make the program executable.

    chmod +x paycon.py

In a Windows system, you can just run "python paycon.py" or "python3 paycon.py".

The only requirement for paycon is [Python 3](https://www.python.org/downloads/).

## Help

    usage: paycon.py [-h] [-t unit] [-w hours] rate [rate ...]
    
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

## Usage examples

    $ ./paycon.py -w 30 -t h 30 40
    Working 30.0 hours a week, based on hourly inputs:
    in:  	$30.00               $40.00
    hourly	$30.00               $40.00
    weekly	$900.00              $1,200.00
    monthly	$3,910.71            $5,214.29
    yearly	$46,928.57           $62,571.43

    $ ./paycon.py 10000000
    Working 40.0 hours a week, based on yearly inputs:
    in:  	$10,000,000.00
    hourly	$4,794.52
    weekly	$191,780.82
    monthly	$833,333.33
    yearly	$10,000,000.00
