#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib

from gslab_make_dev.write_logs import start_makelog
from gslab_make_dev.dir_mod import clear_dir
from gslab_make_dev.run_program import run_lyx
from gslab_make_dev.tests import nostderrout
import gslab_make_dev.private.metadata as metadata
    

class testRunLyx(unittest.TestCase):

    def setUp(self):
        makelog_file = '../log/make.log'
        log_dir	= '../log'
        output_dir = '../output/'
        with nostderrout():
            clear_dir([output_dir, log_dir])
            start_makelog(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx')
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_custom_log(self):
        os.remove('../log/make.log')
        makelog_file = '../log/custom_make.log'
        with nostderrout():        
            start_makelog(makelog_file)
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', makelog = makelog_file)
        logfile_data = open(makelog_file, 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_independent_log(self):
        with nostderrout():
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', log = '../log/lyx.log')
        makelog_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', makelog_data)
        self.assertTrue(os.path.isfile('../log/lyx.log'))
        lyxlog_data = open('../log/lyx.log', 'rU').read()
        self.assertIn('LaTeX', lyxlog_data)
        self.assertIn(lyxlog_data, makelog_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))    
        
    def test_executable(self):
        with nostderrout():
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', executable = metadata.default_executables[os.name]['lyx']) 
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', executable = 'nonexistent_lyx_executable')
        logfile_data = open('../log/make.log', 'rU').read()
        if os.name == 'posix':
            self.assertIn('/bin/sh: nonexistent_lyx_executable: command not found', logfile_data)
        else:
            self.assertIn('\'nonexistent_lyx_executable\' is not recognized as an internal or external command', logfile_data)
    
    def test_no_program(self):
        with self.assertRaises(Exception):
            run_lyx(program = 'gslab_make_dev/tests/input/nonexistent_lyx_file.lyx')
        self.assertFalse(os.path.isfile('../output/lyx_test_file.pdf'))
    
    def test_option(self):
        with nostderrout():
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', option = '-e pdf')
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_pdfout(self): 
        with nostderrout():    
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', pdfout = 'gslab_make_dev/tests/input/custom_outfile.pdf')
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/custom_outfile.pdf'))
        self.assertFalse(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_comments(self):  
        temp_dir = '../temp/'
        with nostderrout():   
            clear_dir([temp_dir])
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', doctype = 'comments')
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../temp/lyx_test_file_comments.pdf'))
        self.assertFalse(os.path.isfile('../output/lyx_test_file_comments.pdf'))

    def test_handout_pdfout(self):
        temp_dir = '../temp/'
        with nostderrout():    
            clear_dir([temp_dir])
            run_lyx(program = 'gslab_make_dev/tests/input/lyx_test_file.lyx', doctype = 'handout', pdfout = 'gslab_make_dev/tests/input/custom_outfile.pdf')
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/custom_outfile.pdf'))
        self.assertFalse(os.path.isfile('../temp/lyx_test_file_handout.pdf'))
        
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isdir('../temp/'):
            shutil.rmtree('../temp/')
        if os.path.isfile('gslab_make_dev/tests/input/lyx_test_file.pdf'):
            os.remove('gslab_make_dev/tests/input/lyx_test_file.pdf')
        if os.path.isfile('gslab_make_dev/tests/input/custom_outfile.pdf'):
            os.remove('gslab_make_dev/tests/input/custom_outfile.pdf')
    
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
