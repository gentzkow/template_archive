#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make_dev.write_logs import start_makelog
from gslab_make_dev import clear_dir
from gslab_make_dev import execute_command
from gslab_make_dev.tests      import nostderrout
    

class testExecuteCommand(unittest.TestCase):

    def setUp(self):
        makelog_file = '../log/make.log'
        log_dir = '../log/'
        if os.name == 'posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        elif os.name == 'nt':
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            raise CritError(messages.crit_error_unknown_system % os.name)

        with nostderrout():
            clear_dir([log_dir])  
            start_makelog(makelog_file)

    def test_default_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        if os.name=='posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
        with nostderrout():
            execute_command(command = our_unzip) 
        logfile_data = open('../log/make.log', 'rU').readlines()
        search_str1 = 'Unzipping test_data.txt.'
        search_str2 = 'Extracting test_data.txt.'
        search_str3 = 'extracting: test_data.txt'
        found1 = logfile_data[-1].find(search_str1) != -1
        found2 = logfile_data[-1].find(search_str2) != -1
        found3 = logfile_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('test_data.txt'))
        
    def test_custom_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))    
        os.remove('../log/make.log')
        makelog_file = '../log/custom_make.log'
        log_dir = '../log/'
        if os.name=='posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
        with nostderrout():
            clear_dir([log_dir])  
            start_makelog(makelog_file)
            execute_command(command = our_unzip, makelog = '../log/custom_make.log')
        logfile_data = open('../log/custom_make.log', 'rU').readlines()
        search_str1 = 'Unzipping test_data.txt.'
        search_str2 = 'Extracting test_data.txt.'
        search_str3 = 'extracting: test_data.txt'
        found1 = logfile_data[-1].find(search_str1) != -1
        found2 = logfile_data[-1].find(search_str2) != -1
        found3 = logfile_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('test_data.txt'))
        
    def test_independent_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        if os.name=='posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'     
        with nostderrout():
            execute_command(command = our_unzip, log = '../log/command.log')
        makelog_data = open('../log/make.log', 'rU').readlines()
        search_str1 = 'Unzipping test_data.txt.'
        search_str2 = 'Extracting test_data.txt.'
        search_str3 = 'extracting: test_data.txt'
        found1 = makelog_data[-1].find(search_str1) != -1
        found2 = makelog_data[-1].find(search_str2) != -1
        found3 = makelog_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('../log/command.log'))
        commandlog_data = open('../log/command.log', 'rU').readlines()
        found1 = commandlog_data[-1].find(search_str1) != -1
        found2 = commandlog_data[-1].find(search_str2) != -1
        found3 = commandlog_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('test_data.txt'))
   
    def tearDown(self):
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isfile('test_data.txt'):
            os.remove('test_data.txt')
    
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
