#! /usr/bin/env python

import unittest
import sys
import os
import re
import decimal
import shutil
from subprocess import check_call, CalledProcessError

# Ensure that Python can find and load the GSLab libraries
#os.chdir(os.path.dirname(os.path.realpath(__file__)))
from gslab_make_dev import tablefill
from gslab_make_dev.tests import nostderrout


class testTablefill(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('./build/'):
            os.mkdir('./build/')

    def testInput(self):
        for ext in ['lyx', 'tex']:
            with nostderrout():
                message = tablefill(input    = 'gslab_make_dev/tests/input/tables_appendix.txt ' + \
                                               'gslab_make_dev/tests/input/tables_appendix_two.txt', 
                                    template = 'gslab_make_dev/tests/input/tablefill_template.%s' % ext, 
                                    output   = './build/tablefill_template_filled.%s' % ext)
            self.assertIn('filled successfully', message)
            tag_data = open('gslab_make_dev/tests/input/tablefill_template.%s' % ext, 'rU').readlines()
            filled_data = open('./build/tablefill_template_filled.%s' % ext, 'rU').readlines()
            self.assertEqual(len(tag_data), len(filled_data))
            for n in range(len(tag_data)):
                if ext == 'tex':
                    self.tag_compare_latex(tag_data[n], filled_data[n])
                elif ext == 'lyx':
                    self.tag_compare_lyx(tag_data[n], filled_data[n]) 

    def tag_compare_latex(self, tag_line, filled_line):
        tag_line    = tag_line.split('&')
        filled_line = filled_line.split('&')
        for col in range(len(tag_line)):
            if re.match('^.*#\d+#', tag_line[col]) or re.match('^.*#\d+,#', tag_line[col]):
                entry_tag = re.split('#', tag_line[col])[1]
                decimal_places = int(entry_tag.replace(',', ''))
                if decimal_places > 0:
                    self.assertTrue(re.search('\.', filled_line[col]))
                    decimal_part = re.split('\.', filled_line[col])[1]
                    non_decimal = re.compile(r'[^\d.]+')
                    decimal_part = non_decimal.sub('', decimal_part)
                    self.assertEqual(len(decimal_part), decimal_places)
                else:
                    self.assertFalse(re.search('\.', filled_line[col]))
                if re.match('^.*#\d+,#', tag_line[col]):
                    integer_part = re.split('\.', filled_line[col])[0]
                    if len(integer_part) > 3:
                        self.assertEqual(integer_part[-4], ',')

    def tag_compare_lyx(self, tag_line, filled_line):
        if re.match('^.*#\d+#', tag_line) or re.match('^.*#\d+,#', tag_line):
            entry_tag = re.split('#', tag_line)[1]
            decimal_places = int(entry_tag.replace(',', ''))
            if decimal_places > 0:
                self.assertTrue(re.search('\.', filled_line))
                decimal_part = re.split('\.', filled_line)[1]
                non_decimal = re.compile(r'[^\d.]+')
                decimal_part = non_decimal.sub('', decimal_part)
                self.assertEqual(len(decimal_part), decimal_places)
            else:
                self.assertFalse(re.search('\.', filled_line))
            if re.match('^.*#\d+,#', tag_line):
                integer_part = re.split('\.', filled_line)[0]
                if len(integer_part) > 3:
                    self.assertEqual(integer_part[-4], ',')

    def testBreaksRoundingString(self):
        for ext in ['lyx', 'tex']:
            with nostderrout():
                error = tablefill(input    =  'gslab_make_dev/tests/input/tables_appendix.txt ' + 
                                              'gslab_make_dev/tests/input/tables_appendix_two.txt', 
                                  template =  'gslab_make_dev/tests/input/tablefill_template_breaks.%s' % ext, 
                                  output   =  './build/tablefill_template_filled.%s' % ext)
            self.assertIn('InvalidOperation', error)

    def testIllegalSyntax(self):
        # missing arguments
        for ext in ['lyx', 'tex']:
            with nostderrout():
                error = tablefill(input   = 'gslab_make_dev/tests/input/tables_appendix.txt ' + \
                                            'gslab_make_dev/tests/input/tables_appendix_two.txt', 
                                  template = 'gslab_make_dev/tests/input/tablefill_template.%s' % ext)
            self.assertIn('KeyError', error)

        # non-existent input 1
        for ext in ['lyx', 'tex']:
            with nostderrout():
                error = tablefill(input    = 'gslab_make_dev/tests/input/fake_file.txt ' + \
                                             'gslab_make_dev/tests/input/tables_appendix_two.txt', 
                                  template = 'gslab_make_dev/tests/input/tablefill_template_breaks.%s' % ext, 
                                  output   = './build/tablefill_template_filled.%s' % ext)
            self.assertIn('IOError', error)

        # non-existent input 2
        for ext in ['lyx', 'tex']:
            with nostderrout():
                error = tablefill(input    = 'gslab_make_dev/tests/input/tables_appendix.txt ' + \
                                             'gslab_make_dev/tests/input/fake_file.txt', 
                                  template = 'gslab_make_dev/tests/input/tablefill_template_breaks.%s' % ext, 
                                  output   = './build/tablefill_template_filled.%s' % ext)
            self.assertIn('IOError', error)

    def testArgumentOrder(self):
        for ext in ['lyx', 'tex']:
            with nostderrout():
                message = tablefill(input    = 'gslab_make_dev/tests/input/tables_appendix.txt ' + \
                                               'gslab_make_dev/tests/input/tables_appendix_two.txt', 
                                    output   = './build/tablefill_template_filled.%s' % ext,
                                    template = 'gslab_make_dev/tests/input/tablefill_template.%s' % ext)
            self.assertIn('filled successfully', message)

            with open('./build/tablefill_template_filled.%s' % ext, 'rU') as filled_file:
                filled_data_args1 = filled_file.readlines()

            with nostderrout():
                message = tablefill(output   = './build/tablefill_template_filled.%s' % ext, 
                                    template = 'gslab_make_dev/tests/input/tablefill_template.%s' % ext, 
                                    input    = 'gslab_make_dev/tests/input/tables_appendix.txt ' + \
                                               'gslab_make_dev/tests/input/tables_appendix_two.txt')
            self.assertIn('filled successfully', message)

            with open('./build/tablefill_template_filled.%s' % ext, 'rU') as filled_file:
                filled_data_args2 = filled_file.readlines()

            self.assertEqual(filled_data_args1, filled_data_args2)

    def tearDown(self):
        if os.path.exists('./build/'):
            shutil.rmtree('./build/')


if __name__ == '__main__':
    os.getcwd()
    unittest.main()
