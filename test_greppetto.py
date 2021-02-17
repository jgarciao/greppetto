import unittest
from unittest import TestCase
import greppetto


class Test(TestCase):

    def test_find_pattern_in_string_with_empty_string(self):
        """
        Test find pattern in string when string is empty
        """

        # GIVEN empty input_line and one pattern
        input_line = ""
        pattern = "mypattern"
        expected_intervals = []

        # WHEN find pattern in input_line
        match_intervals = greppetto.find_pattern_in_string(input_line, pattern)

        # THEN returned matches are the expected
        self.assertEqual(match_intervals, expected_intervals, "Should be " + str(expected_intervals))

    def test_find_pattern_in_string_with_empty_pattern_raises_error(self):
        """
        Test find pattern in string when pattern is empty
        """

        # GIVEN input_line with one occurrence of the pattern
        input_line = "text text text text text"
        pattern = ""

        # WHEN find pattern in input_line with empty pattern raises ValueError
        with self.assertRaises(ValueError):
            greppetto.find_pattern_in_string(input_line, pattern)

    def test_find_pattern_in_string_with_1_occurrences_of_pattern(self):
        """
        Test find pattern in string when the string has one occurrences of the pattern
        """

        # GIVEN input_line with one occurrence of the pattern
        input_line = "text mypattern text"
        pattern = "mypattern"
        expected_intervals = [(5, 14)]

        # WHEN find pattern in input_line
        match_intervals = greppetto.find_pattern_in_string(input_line, pattern)

        # THEN returned matches are the expected
        self.assertEqual(match_intervals, expected_intervals, "Should be " + str(expected_intervals))

    def test_find_pattern_in_string_with_2_occurrences_of_pattern(self):
        """
        Test find pattern in string when the string has two occurrences of the pattern
        """

        # GIVEN input_line with two occurrences of the pattern
        input_line = "text mypattern text mypattern"
        pattern = "mypattern"
        expected_intervals = [(5, 14), (20, 29)]

        # WHEN find pattern in input_line
        match_intervals = greppetto.find_pattern_in_string(input_line, pattern)

        # THEN returned matches are the expected
        self.assertEqual(match_intervals, expected_intervals, "Should be " + str(expected_intervals))

    def test_default_matched_line_formatter(self):
        """
        Test DefaultMatchedLineFormatter with an input_line that contains the pattern
        """

        # GIVEN input_line with one occurrence of the pattern
        filename = "myfilename"
        line_number = "1"
        input_line = "text mypattern text mypattern"
        match_intervals = [(5, 14), (20, 29)]
        expected_formatted_line = "myfilename:1:text mypattern text mypattern"

        # WHEN find pattern in input_line
        factory = greppetto.MatchedLineFormatterFactory()
        factory.register_format(greppetto.MatchedLineFormat.DEFAULT, greppetto.DefaultMatchedLineFormatter)
        line_formatter = factory.get_formatter(greppetto.MatchedLineFormat.DEFAULT)

        formatted_string = line_formatter.format(filename, line_number, input_line, match_intervals)

        # THEN the formatted string has the expected format
        self.assertEqual(formatted_string, expected_formatted_line, "Should be " + str(expected_formatted_line))

    def test_color_matched_line_formatter(self):
        """
        Test ColorMatchedLineFormatter with an input_line that contains the pattern
        """

        # GIVEN input_line with one occurrence of the pattern
        filename = "myfilename"
        line_number = "1"
        input_line = "text mypattern text mypattern"
        match_intervals = [(5, 14), (20, 29)]
        expected_formatted_line = "myfilename:1:text [95mmypattern[0m text [95mmypattern[0m"

        # WHEN find pattern in input_line
        factory = greppetto.MatchedLineFormatterFactory()
        factory.register_format(greppetto.MatchedLineFormat.COLOR, greppetto.ColorMatchedLineFormatter)
        line_formatter = factory.get_formatter(greppetto.MatchedLineFormat.COLOR)

        formatted_string = line_formatter.format(filename, line_number, input_line, match_intervals)

        # THEN the formatted string has the expected format
        self.assertEqual(formatted_string, expected_formatted_line, "Should be " + str(expected_formatted_line))

    def test_underscore_matched_line_formatter(self):
        """
        Test UnderscoreMatchedLineFormatter with an input_line that contains the pattern
        """

        # GIVEN input_line with one occurrence of the pattern
        filename = "myfilename"
        line_number = "1"
        input_line = "text mypattern text mypattern"
        match_intervals = [(5, 14), (20, 29)]
        expected_formatted_line = "myfilename:1:text mypattern text mypattern\n" + \
                                  "                  ^^^^^^^^^      ^^^^^^^^^"

        # WHEN find pattern in input_line
        factory = greppetto.MatchedLineFormatterFactory()
        factory.register_format(greppetto.MatchedLineFormat.UNDERSCORE, greppetto.UnderscoreMatchedLineFormatter)
        line_formatter = factory.get_formatter(greppetto.MatchedLineFormat.UNDERSCORE)

        formatted_string = line_formatter.format(filename, line_number, input_line, match_intervals)

        # THEN the formatted string has the expected format
        self.assertEqual(formatted_string, expected_formatted_line, "Should be " + str(expected_formatted_line))

    def test_machine_matched_line_formatter(self):
        """
        Test MachineReadableMatchedLineFormatter with an input_line that contains the pattern twice
        """

        # GIVEN input_line with one occurrence of the pattern
        filename = "myfilename"
        line_number = "1"
        input_line = "text mypattern text mypattern"
        match_intervals = [(5, 14), (20, 29)]
        expected_formatted_line = "myfilename:1:5:mypattern\n" + \
                                  "myfilename:1:20:mypattern"

        # WHEN find pattern in input_line
        factory = greppetto.MatchedLineFormatterFactory()
        factory.register_format(greppetto.MatchedLineFormat.MACHINE, greppetto.MachineReadableMatchedLineFormatter)
        line_formatter = factory.get_formatter(greppetto.MatchedLineFormat.MACHINE)

        formatted_string = line_formatter.format(filename, line_number, input_line, match_intervals)

        # THEN the formatted string has the expected format
        self.assertEqual(formatted_string, expected_formatted_line, "Should be " + str(expected_formatted_line))


if __name__ == '__main__':
    unittest.main()
