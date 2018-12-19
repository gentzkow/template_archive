#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib, zipfile
sys.path.append('../..')
from gslab_make_dev.dir_mod import zip_dir, unzip

from nostderrout import nostderrout


class testZip(unittest.TestCase):

    def setUp(self):
        self.assertFalse(os.path.isdir('./output_local/'))
        os.makedirs('./output_local/')
        newfile = open('./output_local/text.txt', 'w+')
        newfile.write('test')
        newfile.close()
        newfile2 = open('./output_local/text2.txt', 'w+')
        newfile2.write('test2')
        newfile2.close()
        zipf = zipfile.ZipFile('./output_local/test.zip', 'w', zipfile.ZIP_DEFLATED)
        zipf.write('./output_local/text.txt',arcname='text.txt')
        zipf.write('./output_local/text2.txt',arcname='text2.txt')
        zipf.close()

        
    def test_unzip(self):
        self.assertTrue(os.path.exists('./output_local/'))
        self.assertFalse(os.path.exists('./output_local/unzipped'))
        os.makedirs('./output_local/unzipped')
        unzip('./output_local/test.zip','./output_local/unzipped')
        self.assertTrue(os.path.isfile('./output_local/unzipped/text.txt'))
    
    def test_zip(self):
        self.assertTrue(os.path.exists('./output_local/'))
        self.assertFalse(os.path.isfile('./output_local/zipped.zip'))
        with nostderrout():
            zip_dir('./output_local/', './output_local/zipped.zip')
        self.assertTrue(os.path.isfile('./output_local/zipped.zip'))
        
    def tearDown(self):
        if os.path.isdir('./output_local/'):
            shutil.rmtree('./output_local/')

if __name__ == '__main__':
    os.getcwd()
    unittest.main()
