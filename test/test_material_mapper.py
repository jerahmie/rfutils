"""
Unit tests for rfutils.MaterialMapper, the mapping utility to estimated 
material from properties.
"""
import os
import unittest
from rfutils.material_mapper import Material, MaterialsDB, \
                                    MaterialsDBVirtualFamily, MaterialMapper

class TestMaterialMapper(unittest.TestCase):
    """Unit tests for material mapping.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.vmat_filename = os.path.join(os.path.dirname(__file__),
                                          r'..',
                                          r'test_data',
                                          r'Duke_34y_V5_5mm_0_Duke_34y_V5_5mm.vmat')

    def test_unittest_setup(self):
        """Ensure the system is set up correctly.
        """
        self.assertTrue(True)

    def test_material_object(self):
        """Test the material object.
        """
        mat = Material()
        self.assertIsInstance(mat, Material)

    def test_materialmapper_object(self):
        """Test that object can be created correctly.
        """
        mapper = MaterialMapper()
        self.assertIsInstance(mapper, MaterialMapper)

    def test_material(self):
        """Exercise material properties.
        """
        mat = Material(name="Test_Material")
        self.assertIsInstance(mat, Material)
        self.assertEqual(mat.name, "Test_Material")
        mat.name="New Material"
        self.assertEqual(mat.name, "New Material")
        self.assertEqual(mat.frequency, 300e6)
        mat.frequency = 447e6
        self.assertEqual(mat.frequency, 447.0e6)
        self.assertEqual(mat.sigma, 0.0)
        mat.sigma = 0.8
        self.assertEqual(mat.sigma, 0.8)
        self.assertEqual(mat.epsr, 1.0)
        mat.epsr = 2.5
        self.assertEqual(mat.epsr, 2.5)

    def test_materialsdb(self):
        """Run tests for materials db.
        """
        matdb = MaterialsDB()
        matdb_vmat = MaterialsDBVirtualFamily(self.vmat_filename)
        self.assertIsInstance(matdb, MaterialsDB)
        self.assertIsInstance(matdb_vmat, MaterialsDB)
        self.assertIsInstance(matdb_vmat, MaterialsDBVirtualFamily)
        self.assertEqual(matdb_vmat._vmat_filename, self.vmat_filename)

    def test_materialsdb_reader(self):
        """Test the ability to load a materials file and create a dictionary
        """
        matdb_vmat = MaterialsDBVirtualFamily(self.vmat_filename)
        matdb_vmat._load_materials()



    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
