#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make_dev.write_logs import start_makelog
from gslab_make_dev.dir_mod import clear_dir
from gslab_make_dev.run_program import run_python
from nostderrout import nostderrout
import gslab_make_dev.private.metadata as metadata
    

class testRunPython(unittest.TestCase):

    def setUp(self):
        makelog_file = '../log/make.log'
        log_dir	= '../log'
        output_dir = '../output/'
        with nostderrout():
            clear_dir([output_dir, log_dir])
            start_makelog(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py')
        self.assertIn('Test script complete', open('../log/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_custom_log(self):
        os.remove('../log/make.log')
        makelog_file = '../log/custom_make.log'
        with nostderrout():
            start_makelog(makelog_file)
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', makelog = makelog_file)
        self.assertIn('Test script complete', open(makelog_file).read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', log = '../log/python.log')
        self.assertIn('Test script complete', open('../log/make.log').read())
        self.assertTrue(os.path.isfile('../log/python.log'))
        self.assertIn('Test script complete', open('../log/python.log').read())        
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', executable = metadata.default_executables[os.name]['python']) 
        self.assertIn('Test script complete', open('../log/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', executable = 'nonexistent_python_executable')
        self.assertNotIn('Test script complete', open('../log/make.log').read())

    def test_no_program(self):
        with self.assertRaises(Exception):
            run_python(program = 'gslab_make_dev/tests/input/nonexistent_python_script.py')
        self.assertNotIn('Test script complete', open('../log/make.log').read())
    
    def test_options(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', option = '-h')
        logfile_data = open('../log/make.log', 'rU').read()
        self.assertIn('Options and arguments (and corresponding environment variables):', logfile_data)
    
    def test_args(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', args = '-i \'Input\'')
        output_data = open('output.txt', 'rU').read()
        self.assertIn('Input', output_data)
    
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
