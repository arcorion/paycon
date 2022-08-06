#!/usr/bin/env python3
# Converts given pay amounts between different time units
# For example, if a job lists itself as $20 an hour,
# The output for month would be 20 * 40 * 4.3, or
# 3440.00 for a month's pay.
#
# Usage: paycon [-h, --help] [-i, --input hdwmy] [-o,--output hdwmy] [-t, --time hours] [-c, --CalculateOvertime] number1 [number2..]
import argparse

parser = argparse.ArgumentParser(description='Converts given pay' +
                                 ' amounts between different time units.')
parser.add_argument(
