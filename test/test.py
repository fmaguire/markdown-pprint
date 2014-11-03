#!/usr/bin/env python

import unittest
import markdownpprint as mdpp
import os
import shutil

class TestOverallStaticConversion(unittest.TestCase):
    '''
    Test case to checking for correct conversion of a known input
    when markdownpp is run in static mode
    '''

    def setUp(self):
        '''
        As static mode changes file need to copy test input to check conversion
        without needing to remake test files
        '''
        self.test_input = 'test/test_input.md'
        self.test_input_copy = 'test/test_input_copy.md'
        self.test_output = 'test/test_output.md'
        shutil.copy2(self.test_input, self.test_input_copy)

    def test_static(self):
        '''
        Very simple test to assess whether markdownpp in static mode
        correctly converts test input by comparison to
        a manually checked test output
        '''
        mdpp.main(self.test_input_copy)

        mdpp_output = open(self.test_input_copy, 'r').read()
        test_output = open(self.test_output, 'r').read()

        self.assertMultiLineEqual(mdpp_output, test_output)

    def tearDown(self):
        '''
        Remove copied test file
        '''
        os.remove(self.test_input_copy)

if __name__=='__main__':

    unittest.main()
