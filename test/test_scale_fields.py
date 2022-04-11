"""Unit tests for scale fields.
"""
import unittest
import numpy as np
import rfutils.vopgen as rfvopgen

class TestScaleFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_setup(self):
        """Test the unit test setup.
        """
        # self.assertTrue(True)

    def test_find_scale_fields(self):
        """ Make sure rfutils.vopgen contains the requisite function.
        """
        self.assertTrue(hasattr(rfvopgen, "scale_fields") and 
                                callable(rfvopgen.scale_fields))

    def test_scale_fields(self):
        """ Check return value is dict
        """
        scales = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                           1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        self.assertEqual(np.size(scales), 16)
        vopfield3d = {}
        self.assertIsInstance(rfvopgen.scale_fields(scales, vopfield3d),
                              dict)

    

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
