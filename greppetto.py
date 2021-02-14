#!/usr/bin/python
from enum import Enum
import re
import argparse


class LineFormatType(Enum):
    UNDERSCORE = 1
    COLOR = 2
    MACHINE = 3


class LineFormatterFactory:
    """As the matching lines can be presented in 3 different formats (underscored, colored and machine readable),
    we will use the factory pattern to instantiate a corresponding LineFormatter for each type.

    Note: this class is an adaptation of this example:
    https://realpython.com/factory-method-python/#supporting-additional-formats
    """

    def __init__(self):
        self._formatters = {}

    def register_format(self, line_format_type, formatter):
        """Registers a LineFormatter class for a LineFormatType """
        self._formatters[line_format_type] = formatter

    def get_formatter(self, line_format_type):
        """Obtains a LineFormatter object for a LineFormatType, or an error if not supported """
        formatter = self._formatters.get(line_format_type)
        if not formatter:
            raise ValueError(line_format_type)
        return formatter()


class ColorLineFormatter:
    """This LineFormatter formats lines from a file returning
        filename:line_number:line (with colored matched patterns)"""

    CHAR_FORMAT_START_PURPLE = '\033[95m'
    CHAR_FORMAT_END = '\033[0m'

    # noinspection PyMethodMayBeStatic
    def format(self, filename, line_number, line, pattern_match_intervals):
        formatted_line = filename + ":" + str(line_number) + ":"

        last_match_end = 0
        for interval in pattern_match_intervals:
            formatted_line += line[last_match_end:interval[0]] + ColorLineFormatter.CHAR_FORMAT_START_PURPLE + \
                              line[interval[0]:interval[1]] + ColorLineFormatter.CHAR_FORMAT_END
            last_match_end = interval[1]
        formatted_line += line[last_match_end:]

        return formatted_line


class UnderscoreLineFormatter:
    """This LineFormatter formats lines from a file returning
          filename:line_number:line (with ^^^ under the matched patterns)"""

    # noinspection PyMethodMayBeStatic
    def format(self, filename, line_number, line, pattern_match_intervals):

        prefix = filename + ":" + str(line_number) + ":"
        formatted_line = prefix + line
        underscored_line = [' '] * len(formatted_line)

        for interval in pattern_match_intervals:
            for i in range(interval[0] + len(prefix), interval[1] + len(prefix)):
                underscored_line[i] = "^"

        return formatted_line + "\n" + "".join(underscored_line)


def find_pattern_in_line(line, pattern):
    """Search all non-overlapping matches of the pattern in a line and returns
     a list of intervals (match start, match end) where the pattern has been found."""

    match_intervals = []
    cre = re.compile(pattern)

    for match in cre.finditer(line):
        match_intervals.append((match.start(), match.end()))

    return match_intervals


def print_pattern_in_file(filename, pattern, print_line_format):
    factory = LineFormatterFactory()
    factory.register_format(LineFormatType.COLOR, ColorLineFormatter)
    factory.register_format(LineFormatType.UNDERSCORE, UnderscoreLineFormatter)
    line_formatter = factory.get_formatter(print_line_format)

    cre = re.compile(pattern)

    with open(filename, 'r') as f:

        for line_number, line in enumerate(f, start=1):
            stripped_line = line.strip()
            match_intervals = find_pattern_in_line(stripped_line, pattern)

            if len(match_intervals) > 0:
                print(line_formatter.format(filename, line_number, stripped_line, match_intervals))

    f.close()


if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-r", "--regex", required=True, help="regexp to search")
    ap.add_argument("-f", "--files", required=True, help="files where to search")

    group = ap.add_mutually_exclusive_group()
    group.add_argument("-u", "--underscore", help="prints '^' under the matching text", action="store_true")
    group.add_argument("-c", "--color", help="highlight the matching text", action="store_true")
    group.add_argument("-m", "--machine", help="generate machine-readable output format:\n  "
                                               "file_name:no_line:start_pos:matched_text", action="store_true")

    args = ap.parse_args()

    if args.underscore:
        print_pattern_in_file(args.files, args.regex, LineFormatType.UNDERSCORE)
    elif args.color:
        print_pattern_in_file(args.files, args.regex, LineFormatType.COLOR)
    elif args.machine:
        print_pattern_in_file(args.files, args.regex, LineFormatType.MACHINE)
    else:
        print_pattern_in_file(args.files, args.regex, LineFormatType.COLOR)
