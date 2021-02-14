#!/usr/bin/python
from enum import Enum
import re
import argparse
import sys


class MatchedLineFormat(Enum):
    """Defines different formatting formats for printing pattern matching lines in files"""
    DEFAULT = 1
    UNDERSCORE = 2
    COLOR = 3
    MACHINE = 4


class MatchedLineFormatterFactory:
    """As the pattern matching lines can be presented in 4 different formats (default, underscored,
    colored and machine readable), we will use the factory pattern to instantiate a corresponding
    MatchedLineFormatter for each one.

    Note: this class is an adaptation of the example explained here:
    https://realpython.com/factory-method-python/#supporting-additional-formats
    """

    def __init__(self):
        self._formatters = {}

    def register_format(self, matched_line_format, formatter):
        """Registers a MatchingLineFormatter class for a MatchedLineFormat """
        self._formatters[matched_line_format] = formatter

    def get_formatter(self, matched_line_format):
        """Obtains a MatchingLineFormatter object for a MatchedLineFormat, or an error if not supported """
        formatter = self._formatters.get(matched_line_format)
        if not formatter:
            raise ValueError(matched_line_format)
        return formatter()


class DefaultMatchedLineFormatter:
    """Formats the information related to pattern matched lines in a file using the Default format
    (see details in the format method)
    """

    # noinspection PyMethodMayBeStatic
    def format(self, filename, line_number, line, pattern_match_intervals):
        """
        Returns a string containing the information provided by the input parameters (related to pattern matched
        lines in a file) using this formatting:

        filename:line_number:line

        In case of having multiple matches in the same line the resulting string will have just one line
        for all occurrences, as all are in the same line_number.

        :param filename: Filename of the file being parsed
        :param line_number: Line number
        :param line: String containing the actual line of the file being processed
        :param pattern_match_intervals: Set of tuples (start, end) where the pattern has been found in the line
        :return: Formatted string
        """

        formatted_line = filename + ":" + str(line_number) + ":" + line

        return formatted_line.strip()


class ColorMatchedLineFormatter:
    """Formats the information related to pattern matched lines in a file coloring the matching text
    (see details in the format method)
    """

    CHAR_FORMAT_START_PURPLE = '\033[95m'
    CHAR_FORMAT_END = '\033[0m'

    # noinspection PyMethodMayBeStatic
    def format(self, filename, line_number, line, pattern_match_intervals):
        """
           Returns a string containing the information provided by the input parameters (related to pattern matched
           lines in a file) using this formatting:

           filename:line_number:line (coloring the matching text)

           :param filename: Filename of the file being parsed
           :param line_number: Line number
           :param line: String containing the actual line of the file being processed
           :param pattern_match_intervals: Set of tuples (start, end) where the pattern has been found in the line
           :return: Formatted string
        """

        formatted_line = filename + ":" + str(line_number) + ":"

        last_match_end = 0
        for interval in pattern_match_intervals:
            formatted_line += line[last_match_end:interval[0]] + ColorMatchedLineFormatter.CHAR_FORMAT_START_PURPLE + \
                              line[interval[0]:interval[1]] + ColorMatchedLineFormatter.CHAR_FORMAT_END
            last_match_end = interval[1]
        formatted_line += line[last_match_end:]

        return formatted_line


class UnderscoreMatchedLineFormatter:
    """Formats the information related to pattern matched lines in a file underscoring ^^^ the matching text
      (see details in the format method)
    """

    # noinspection PyMethodMayBeStatic
    def format(self, filename, line_number, line, pattern_match_intervals):
        """
           Returns a string containing the information provided by the input parameters (related to pattern matched
           lines in a file) using this formatting:

            filename:line_number:line (with ^^^^ under the matching text)

           :param filename: Filename of the file being parsed
           :param line_number: Line number
           :param line: String containing the actual line of the file being processed
           :param pattern_match_intervals: Set of tuples (start, end) where the pattern has been found in the line
           :return: Formatted string
        """

        prefix = filename + ":" + str(line_number) + ":"
        formatted_line = prefix + line
        underscored_line = [' '] * len(formatted_line)

        for interval in pattern_match_intervals:
            for i in range(interval[0] + len(prefix), interval[1] + len(prefix)):
                underscored_line[i] = "^"

        return formatted_line + "\n" + "".join(underscored_line)


class MachineReadableMatchedLineFormatter:
    """Formats the information related to pattern matched lines in a file using a machine readable formatting
         (see details in the format method)
    """

    # noinspection PyMethodMayBeStatic
    def format(self, filename, line_number, line, pattern_match_intervals):
        """
        Returns a string containing the information provided by the input parameters (related to pattern matched
        lines in a file) using this formatting:
            filename:line_number:start_pos:matched_text

        In case there are multiple matches several lines will be added:
            filename:line_number:start_pos1:matched_text
            filename:line_number:start_pos2:matched_text

        :param filename: Filename of the file being parsed
        :param line_number: Line number
        :param line: String containing the actual line of the file being processed
        :param pattern_match_intervals: Set of tuples (start, end) where the pattern has been found in the line
        :return: Formatted string
        """
        formatted_line = ""
        prefix = filename + ":" + str(line_number) + ":"

        for interval in pattern_match_intervals:
            formatted_line = formatted_line + prefix + str(interval[0]) + ":" + line[interval[0]:interval[1]] + "\n"

        return formatted_line.strip()


def find_pattern_in_string(input_string, pattern):
    """
    Search for all non-overlapping matches of a pattern in a string

    :param input_string: String where to search the pattern
    :param pattern: Regular expression with the pattern to search
    :return: list of intervals (match start, match end) of input_string where the pattern has been found.
    """
    match_intervals = []
    cre = re.compile(pattern)

    for match in cre.finditer(input_string):
        match_intervals.append((match.start(), match.end()))

    return match_intervals


def find_pattern_in_files(files, pattern, print_line_format):
    """
    Search for a pattern in a list of files (or in stdin if none is provided) and print the
    matching lines using the format specified in print_line_format

    :param files: Files to be processed. stdin will be used if none is provided
    :param pattern: Regular expression with the pattern to search
    :param print_line_format: Format to use when printing the matching lines
    """
    factory = MatchedLineFormatterFactory()

    factory.register_format(MatchedLineFormat.DEFAULT, DefaultMatchedLineFormatter)
    factory.register_format(MatchedLineFormat.COLOR, ColorMatchedLineFormatter)
    factory.register_format(MatchedLineFormat.UNDERSCORE, UnderscoreMatchedLineFormatter)
    factory.register_format(MatchedLineFormat.MACHINE, MachineReadableMatchedLineFormatter)
    line_formatter = factory.get_formatter(print_line_format)

    if files is not None:
        for filename in files:
            with open(filename, 'r') as f:
                for line_number, line in enumerate(f, start=1):
                    match_intervals = find_pattern_in_string(line.strip(), pattern)
                    if len(match_intervals) > 0:
                        print(line_formatter.format(filename, line_number, line.strip(), match_intervals))
            f.close()
    else:
        line_number = 0
        for line in sys.stdin:
            line_number += 1
            match_intervals = find_pattern_in_string(line.strip(), pattern)
            if len(match_intervals) > 0:
                print(line_formatter.format("-", line_number, line.strip(), match_intervals))


if __name__ == '__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-r", "--regex", required=True, help="regexp to search")
    ap.add_argument("-f", "--files", metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')

    # Create a group for mutually exclusive arguments
    group = ap.add_mutually_exclusive_group()
    group.add_argument("-u", "--underscore", help="prints '^' under the matching text", action="store_true")
    group.add_argument("-c", "--color", help="highlight the matching text", action="store_true")
    group.add_argument("-m", "--machine", help="generate machine-readable output format:\n  "
                                               "file_name:no_line:start_pos:matched_text", action="store_true")
    args = ap.parse_args()

    if args.underscore:
        find_pattern_in_files(args.files, args.regex, MatchedLineFormat.UNDERSCORE)
    elif args.color:
        find_pattern_in_files(args.files, args.regex, MatchedLineFormat.COLOR)
    elif args.machine:
        find_pattern_in_files(args.files, args.regex, MatchedLineFormat.MACHINE)
    else:
        find_pattern_in_files(args.files, args.regex, MatchedLineFormat.DEFAULT)
