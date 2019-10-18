"""
Unit tests for FieldReaderCST2019 classes.
"""
import os
import unittest
from rfutils.xmat import FieldReaderCST2019

class TestFieldReaderCST2019(unittest.TestCase):
    """Unit tests class for FieldReaderCST2019.
    """
    @classmethod
    def setUpClass(cls):
        cls.test_data_dir = os.path.abspath(os.path.join(os.path.basename(__file__),'..', 'test_data'))

    def setUp(self):
        self.fr = FieldReaderCST2019()


    def test_process_file_list(self):
        """Use list of regular expressions to generate input file list.
        """
        
        field_files_pattern = [os.path.join(self.test_data_dir, 'e-field*.h5'),
                               os.path.join(self.test_data_dir, 'h-field*.h5')]

        field_files = [os.path.join(self.test_data_dir, "e-field (f=447) [pw].h5"),
                       os.path.join(self.test_data_dir, "h-field (f=447) [pw].h5")]
        self.assertTrue(os.path.exists(field_files[0]))
        self.assertTrue(os.path.exists(field_files[1]))
        found_field_files = self.fr._process_file_list(field_files_pattern)
        for field_file in found_field_files:
            self.assertTrue(os.path.exists(field_file))
            self.assertTrue(field_file in field_files)

    def test_read_fields(self):
        """Test read_fields method to populate field matrices.
        """
        efields = self.assertFalse(self.fr.read_fields('*[pw].h5'))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if "__main__" == __name__:
    unittest.main()