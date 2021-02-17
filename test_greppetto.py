import unittest
from unittest import TestCase
import greppetto


class Test(TestCase):

    def test_find_pattern_in_string_with_empty_string(self):
        """
        Test find pattern in string when string is empty
        """

        # GIVEN input_line with one occurrence of the pattern
        input_line = ""
        pattern = "mypattern"
        expected_intervals = []

        # WHEN find pattern in input_line
        match_intervals = greppetto.find_pattern_in_string(input_line, pattern)

        # THEN returned matches are the expected
        self.assertEqual(match_intervals, expected_intervals, "Should be " + str(expected_intervals))

    def test_find_pattern_in_string_with_empty_pattern(self):
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
        Test find pattern in string when the string has two occurrences of the pattern
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


if __name__ == '__main__':
    unittest.main()
