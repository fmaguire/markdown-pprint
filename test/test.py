#!/usr/bin/env python

import unittest
import markdownpprint as mdpp
import os
import sys
import shutil
import re

class TestConversion(unittest.TestCase):
    '''
    Test case for checking correct conversion and prettification of eqs
    '''

    def setUp(self):
        '''
        As static mode changes file need to copy test input to check conversion
        without needing to remake test files
        '''
        self.test_input = 'test_input.md'
        self.test_output = 'test_output.md'
        self.test_input_copy = 'test_input_copy.md'

    def test_static(self):
        '''
        Test default static mode correctly modified input file
        '''
        # copy test input file as it will be changed
        shutil.copy(self.test_input, self.test_input_copy)

        # run main with default settings
        mdpp.main(self.test_input_copy)

        # parse example output and actual output
        with open(self.test_input_copy, 'r') as mdpp_out_fh:
            mdpp_output = mdpp_out_fh.read()

        with open(self.test_output, 'r') as test_out_fh:
            test_output = test_out_fh.read()

        # make sure they are the same
        self.assertMultiLineEqual(mdpp_output, test_output)

        # clean up test input copy
        os.remove(self.test_input_copy)

    def test_streaming_input(self):
        '''
        Test that streaming mode leaves input file unchanged
        '''
        # copy input file in case it does change
        shutil.copy(self.test_input, self.test_input_copy)

        # run main in streaming mode
        mdpp.main(self.test_input_copy, streaming=True)

        # read the used input and the file it was copied from
        with open(self.test_input_copy, 'r') as mdpp_out_fh:
            mdpp_input = mdpp_out_fh.read()

        with open(self.test_input, 'r') as test_input_fh:
            test_input = test_input_fh.read()

        # assert input hasn't changed
        self.assertMultiLineEqual(mdpp_input, test_input)

        # clean up input file copy
        os.remove(self.test_input_copy)

    def test_streaming_output(self):
        '''
        Test that streaming mode stdout output matches sample output
        '''
        # copy input file in case it does change
        shutil.copy(self.test_input, self.test_input_copy)

        # run main in streaming mode
        mdpp.main(self.test_input_copy, streaming=True)

        # stdout is a stringIO instance so needs parsing after capture
        mdpp_stdout = sys.stdout.getvalue().strip()

        # parse test output
        with open(self.test_output, 'r') as test_out_fh:
            test_output = test_out_fh.read()

        # assert stdout is same as test output
        self.assertMultiLineEqual(mdpp_stdout + '\n', test_output)

        # clean up input file copy
        os.remove(self.test_input_copy)

    def test_status(self):
        '''
        Tests the status parsing ability
        '''
        # if it works, should not produce two copies of equations
        
        # copy input file in case it does change
        shutil.copy(self.test_input, self.test_input_copy)
        
        # run main 
        mdpp.main(self.test_input_copy)
        # run main again
        mdpp.main(self.test_input_copy)

        # parse test output (which is input)
        with open(self.test_input_copy, 'r') as mdpp_out_fh:
            mdpp_input = mdpp_out_fh.read()

        # check how many equations are in there
        r = re.compile("```(.*?)```",re.DOTALL)
        eqenvs = r.findall(mdpp_input)
        self.assertEqual(len(eqenvs),2)

        # clean up input file copy
        os.remove(self.test_input_copy)

if __name__=='__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
