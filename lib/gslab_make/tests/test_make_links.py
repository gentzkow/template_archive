# #! /usr/bin/env python

# import unittest, sys, os, shutil, re
# from gslab_make_dev.write_logs import start_makelog, end_makelog
# from gslab_make_dev.make_links import make_links
# from gslab_make_dev.dir_mod import clear_dir
# from nostderrout import nostderrout
    
    
# class testMakeLinks(unittest.TestCase):

#     def setUp(self):
#         log_dir = '../log/'
#         input_dir = '../input/'
#         self.assertFalse(os.path.exists(log_dir))
#         self.assertFalse(os.path.exists(input_dir))
#         with nostderrout():
#             clear_dir([log_dir,input_dir])
#             start_makelog()

#     def test_default(self):
#         with open('../input/links.txt', 'w') as f:
#             f.write('./here_is_a_link/\t./gslab_make_dev/private/')
#         links = make_links(['../input/links.txt'])
#         #Still need to figure out exactly what output is expected in order to write tests

   
#     def tearDown(self):
#         with nostderrout():
#             end_makelog()
#         if os.path.isdir('../input/'):
#             shutil.rmtree('../input/')
#         if os.path.isdir('../log/'):
#             shutil.rmtree('../log/')
    
# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()
    
