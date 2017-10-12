"""
Unit tests for colecole.py
"""
import unittest
import colecole

class TestColeCole(unittest.TestCase):
    """Tests for ColeCole4Pole class"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.test_cc = colecole.ColeCole4Pole()

    def test_config(self):
        """
        Test the unittest setup.
        """
        self.assertEqual(1,1)

    def test_colecole(self):
        """
        Make sure the object initializes properly
        """
        self.assertIsInstance(self.test_cc, object)
        self.assertIsInstance(self.test_cc, colecole.ColeCole4Pole)

    def test_sigma_setter_getter(self):
        """
        Test the conductivity setters and getters.
        """
        self.assertEqual(1, self.test_cc.sigma())
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
