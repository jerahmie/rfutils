"""
Unit tests for rfutils.MaterialMapper, the mapping utility to estimated 
material from properties.
"""

import unittest
from rfutils.material_mapper import MaterialMapper

class TestMaterialMapper(unittest.TestCase):
    """Unit tests for material mapping.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_unittest_setup(self):
        """Ensure the system is set up correctly.
        """
        self.assertTrue(True)

    def test_materialmapper_object(self):
        """Test that object can be created correctly.
        """
        mapper = MaterialMapper()
        self.assertIsInstance(mapper, MaterialMapper)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
