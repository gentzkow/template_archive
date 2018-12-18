#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make_dev.write_logs import start_makelog
from gslab_make_dev.dir_mod import clear_dir
from gslab_make_dev.run_program import run_stata
from nostderrout import nostderrout
import gslab_make_dev.private.metadata as metadata
    

class testRunStata(unittest.TestCase):

    def setUp(self):
        makelog_file = '../log/make.log'
        log_dir	= '../log'
        output_dir = '../output/'
        with nostderrout():
            clear_dir([output_dir, log_dir])
            start_makelog(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do')
        self.assertIn('end of do-file', open('../log/make.log').read())
        
    def test_custom_log(self):
        os.remove('../log/make.log')
        makelog_file = '../log/custom_make.log'
        with nostderrout():    
            start_makelog(makelog_file)
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', makelog = makelog_file)
        self.assertIn('end of do-file', open(makelog_file).read())

    def test_independent_log(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', log = '../log/stata.log')
        self.assertIn('end of do-file', open('../log/make.log').read())
        self.assertTrue(os.path.isfile('../log/stata.log'))
        self.assertIn('end of do-file', open('../log/stata.log').read())
        
    def test_executable(self):
        with nostderrout():
			run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', executable = metadata.default_executables[os.name]['stata']) 
        self.assertIn('end of do-file', open('../log/make.log').read())
        
    def test_bad_executable(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', executable = 'nonexistent_stata_executable')
        self.assertFalse('end of do-file' in open('../log/make.log').read())
    
    def test_no_program(self):
        with self.assertRaises(Exception):
            run_stata(program = 'gslab_make_dev/tests/input/nonexistent_stata_script.do')
        self.assertNotIn('end of do-file', open('../log/make.log').read())
    
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        if os.path.isfile('gslab_make_dev/tests/input/output.txt'):
            os.remove('gslab_make_dev/tests/input/output.txt')  
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
