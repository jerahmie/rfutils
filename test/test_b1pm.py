"""Unit tests for converting Cartesian field components to rotating fields.
"""
import os
import unittest
from rfutils.emfield import EMField

class TestB1PM(unittest.TestCase):
    """Unittests for b1pm module.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        test_field_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                           '..', 'test_data', 'AC_Zero_Phase.h5'))

    def test_env_setup(self):
        """This should pass, always.
        """
        self.assertTrue(True)

    def test_EMField(self):
        em1 = EMField()
        self.assertIsInstance(em1, EMField)
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()