# #! /usr/bin/env python

# import unittest, sys, os, shutil, contextlib
# sys.path.append('../..')
# from gslab_make_dev.dir_mod import delete_files
# from nostderrout import nostderrout
    

# class testDeleteFiles(unittest.TestCase):

#     def setUp(self):
#         self.assertFalse(os.path.isdir('./output_local/'))
#         os.makedirs('./output_local/')
#         newfile = open('./output_local/text.txt', 'w+')
#         newfile.write('test')
#         newfile.close()
#         newfile2 = open('./output_local/text2.txt', 'w+')
#         newfile2.write('test2')
#         newfile2.close()
#         newfile3 = open('./output_local/other.txt', 'w+')
#         newfile3.write('other')
#         newfile3.close()

#     def test_single_file(self):
#         file_list = os.listdir('./output_local/')
#         file_number = len(file_list)
#         self.assertTrue(os.path.isfile('./output_local/text.txt'))
#         with nostderrout():
#             delete_files('./output_local/text.txt')
#         file_list = os.listdir('./output_local/')
#         self.assertEqual(len(file_list), file_number - 1)
#         self.assertFalse(os.path.isfile('./output_local/text.txt'))
#         self.assertTrue(os.path.isfile('./output_local/text2.txt'))
    
#     def test_wildcards(self):
#         file_list = os.listdir('./output_local/')
#         self.assertEqual(len(file_list), 3)
#         with nostderrout():        
#             delete_files('./output_local/text*')
#         file_list = os.listdir('./output_local/')
#         self.assertEqual(len(file_list), 1)
#         self.assertTrue(os.path.isdir('./output_local/'))
#         self.assertTrue(os.path.isfile('./output_local/other.txt'))
    
#     def test_directory_fails(self):
#         with nostderrout():
#             with self.assertRaises(OSError):
#                 delete_files('./output_local/')
            
#     def tearDown(self):
#         if os.path.isdir('./output_local/'):
#             shutil.rmtree('./output_local/')        

# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()