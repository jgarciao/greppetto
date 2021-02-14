#!/usr/bin/python
import re
import argparse


class Format:
    START_PURPLE = '\033[95m'
    START_UNDERLINE = '\033[4m'
    END = '\033[0m'


def format_line(filename, line_number, line, pattern_match_intervals):

    formatted_line = filename + ":" + str(line_number) + ":"

    last_match_end = 0
    for interval in pattern_match_intervals:
        formatted_line += line[last_match_end:interval[0]] + Format.START_PURPLE + \
                          line[interval[0]:interval[1]] + Format.END
        last_match_end = interval[1]
    formatted_line += line[last_match_end:]

    return formatted_line


def find_pattern_in_line(line, pattern):
    """Search all non-overlapping matches of the pattern in a line and returns
     a list of intervals (match start, match end) where the pattern has been found."""

    match_intervals = []
    cre = re.compile(pattern)

    for match in cre.finditer(line):
        match_intervals.append((match.start(), match.end()))

    return match_intervals


def find_pattern_in_file(filename, pattern):

    cre = re.compile(pattern)

    with open(filename, 'r') as f:

        for line_number, line in enumerate(f, start=1):
            stripped_line = line.strip()
            match_intervals = find_pattern_in_line(stripped_line, pattern)

            if len(match_intervals) > 0:
                print(format_line(filename, line_number, stripped_line, match_intervals))

    f.close()


if __name__ == '__main__':

    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-r", "--regex", required=True,
                    help="regexp to search")
    ap.add_argument("-f", "--files", required=True,
                    help="files where to search")
    args = ap.parse_args()

    find_pattern_in_file(args.files, args.regex)
