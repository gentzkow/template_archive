# #! /usr/bin/env python

# import unittest, sys, os, shutil, contextlib
# sys.path.append('../..')
# from gslab_make_dev.write_logs import start_makelog
# from gslab_make_dev.dir_mod import clear_dir
# from gslab_make_dev.run_program import run_matlab
# from nostderrout import nostderrout
# import gslab_make_dev.private.metadata as metadata

# class testRunMatlab(unittest.TestCase):

#     def setUp(self):
#         makelog_file = '../log/make.log'
#         log_dir = '../log/'
#         output_dir = '../output/'
#         with nostderrout():
#             clear_dir([output_dir, log_dir])
#             start_makelog(makelog_file)

#     def test_default_log(self):
#         run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m')
#         self.assert_proper_output('../log/make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_custom_log(self):
#         os.remove('../log/make.log')
#         makelog_file = '../log/custom_make.log'
#         with nostderrout():
#             start_makelog(makelog_file)
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', makelog = makelog_file)
#         self.assert_proper_output('../log/custom_make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_independent_log(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', log = '../log/matlab.log')
#         self.assert_proper_output('../log/make.log')
#         self.assertTrue(os.path.isfile('../log/matlab.log'))
#         self.assert_proper_output('../log/matlab.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_executable(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', executable = metadata.default_executables[os.name]['matlab']) 
#         self.assert_proper_output('../log/make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_bad_executable(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', executable = 'nonexistent_matlab_executable')
#         self.assertNotIn('1.716', open('../log/make.log', 'rU').read())
    
#     def test_no_program(self):
#         with self.assertRaises(Exception):
#             run_matlab(program = 'gslab_make_dev/tests/input/nonexistent_matlab_script.m')
#         self.assertNotIn('1.716', open('../log/make.log', 'rU').read())
    
#     def test_option(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', option = '-h')
#         logfile_data = open('../log/make.log', 'rU').read()
#         if os.name == 'posix':
#             self.assertIn('matlab [-h|-help]', logfile_data)
#         else:
#             self.assertIn('matlab [-? ^| -h ^| -help]', logfile_data)
            
#     def test_wait(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script_wait1.m')
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script_wait2.m')
#         file_data = open('../log/make.log', 'rU').read()
#         self.assertIn('1.716', file_data)
#         self.assertNotIn('Error', file_data)

#     def assert_proper_output(self, filename):
#         file_data = open(filename, 'rU').read()
#         self.assertIn('0.8147', file_data)
#         self.assertNotIn('Error', file_data)

#     def tearDown(self):
#         if os.path.isdir('../log/'):
#             shutil.rmtree('../log/')
#         if os.path.isdir('../output/'):
#             shutil.rmtree('../output/')
    
# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()
