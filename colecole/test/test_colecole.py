"""
Unit tests for colecole.py
"""
import unittest
import numpy as np
import colecole

class TestColeCole(unittest.TestCase):
    """Tests for ColeCole class"""
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.test_cc = colecole.ColeCole()

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
        self.assertIsInstance(self.test_cc, colecole.ColeCole)

    def test_colecole_init(self):
        """
        Test valid colecole inits
        """
        cc1 = colecole.ColeCole(1, 2, 3, 4, 5)
        self.assertEqual(1, cc1.ef)
        self.assertEqual(2, cc1.sigma)
        self.assertEqual([3], cc1.deltas)
        self.assertEqual([4], cc1.taus)
        self.assertEqual([5], cc1.alphas)
        cc2 = colecole.ColeCole(8, 9,
                                [1.1, 2.2, 3.3, 4.4],
                                [5.5, 6.6, 7.7, 8.8],
                                [9.9, 1.2, 2.3, 3.4])
        self.assertEqual(8, cc2.ef)
        self.assertEqual(9, cc2.sigma)
        self.assertEqual([1.1, 2.2, 3.3, 4.4], cc2.deltas)
        self.assertEqual([5.5, 6.6, 7.7, 8.8], cc2.taus)
        self.assertEqual([9.9, 1.2, 2.3, 3.4], cc2.alphas)

    def test_sigma_setter_getter(self):
        """
        Test the conductivity setters and getters.
        """
        self.assertEqual(0, self.test_cc.sigma)
        self.test_cc.sigma = 1.1
        self.assertEqual(1.1, self.test_cc.sigma)
        
    def test_dels_setter_getter(self):
        """
        Test the static relative permittivity (Deltas) setters and getters
        """
        self.assertEqual([], self.test_cc.deltas)
        self.test_cc.deltas = 1
        self.assertEqual([1], self.test_cc.deltas)
        self.assertEqual(1, len(self.test_cc.deltas))
        self.test_cc.deltas = [1.1,2.2,3.3,4.4]
        self.assertEqual([1.1,2.2,3.3,4.4], self.test_cc.deltas)
        self.assertEqual(4, len(self.test_cc.deltas))
        
    def test_alphas_setter_getter(self):
        """
        Test the broadness parameter setters and getters.
        """
        self.assertEqual([], self.test_cc.alphas)
        self.test_cc.alphas = 1
        self.assertEqual([1], self.test_cc.alphas)
        new_alphas = [1.2, 2.3, 3.4, 4.5]
        self.test_cc.alphas = new_alphas
        self.assertEqual(new_alphas, self.test_cc.alphas)
        self.assertEqual(4, len(self.test_cc.alphas))

    def test_taus_setter_getter(self):
        """
        Test the relaxation time parameter setters and getters.
        """
        self.assertEqual([], self.test_cc.taus)
        self.test_cc.taus = 1
        self.assertEqual([1], self.test_cc.taus)

    def test_epsilon_calc(self):
        """
        Test the calculation of relative permittivity.
        """
        # Aorta material at 300 MHz
        cc1 = colecole.ColeCole(4, 0.25, 40, 8.842e-12, 0.1, 300e6)
        self.assertTrue(np.isclose(43.819275919-15.962534469j, cc1.epsilon))
        cc2 = colecole.ColeCole(4.0, 0.25,
                                 [40.0, 50.0],
                                 [8.843e-12, 3.183e-9],
                                 [0.1, 0.1])
        self.assertTrue(np.isclose(47.0376277802 -24.896267623j,
                                   cc2.epsilon))
        cc3 = colecole.ColeCole(4.0, 0.25,
                                 [40.0, 50.0, 1.0e5],
                                 [8.843e-12, 3.183e-9, 159.155e-6],
                                 [0.1, 0.1, 0.2])
        self.assertTrue(np.isclose(48.3209403398-28.8453668977j,
                                   cc3.epsilon))
        cc4 =  colecole.ColeCole(4.0, 0.25,
                                 [40.0, 50.0, 1.0e5, 1.0e7],
                                 [8.843e-12, 3.183e-9, 159.155e-6, 1.592e-3],
                                 [0.1, 0.1, 0.2, 0.0])
        self.assertTrue(np.isclose(48.3209414503-32.17775682845j,
                                   cc4.epsilon))
        
    def test_colecole_main(self):
        """
        Test the main routine (for command line).
        """
        args1 = ['colecole.py', '4', '0.25', '40', '8.842e-12', '0.1', '300e6']
        self.assertEqual("43.819275919-15.962534469j",
                         colecole.colecole_main(args1))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
