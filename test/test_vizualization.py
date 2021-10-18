"""Unit tests for visualization routines.
"""
import os
import sys
from io import StringIO
#import logging
import unittest
import skrf as rf
from rfutils import visualization as viz


class TestViz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ts_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      '..','test_data',
                                      '8CH_ELdipole_commongnd-23cmCONE_notraps_cloneELDipole_6-30-2020.s8p'))

    def setUp(self):
        # https://stackoverflow.com/questions/9534245/python-logging-to-stringio-handler
        #self.handler = logging.StreamHandler(self.stream)
        #self.log = logging.getLogger('mylogger')
        #self.log.setLevel(lo)
        pass

    def test_viz(self):
        self.assertIn('s_matrix_at_freq', dir(viz))

    def test_pretty_print(self):
        self.assertIn('pretty_print_s_parameters', dir(viz))

    def test_pretty_s_matrix(self):
        """Test the display of the pretty print function.
        """
        # https://www.devdungeon.com/content/python-use-stringio-capture-stdout-and-stderr
        captured_output = StringIO()
        # capture standard output
        sys.stdout = captured_output
        self.assertTrue(os.path.exists(self.ts_file))
        ntwk = rf.Network(self.ts_file)
        viz.pretty_print_s_parameters(ntwk)
        captured_output.seek(0)
        self.assertEqual("|    1     |     2     |     3     |     4     |     5     |     6     |     7     |     8     |\n",
                         captured_output.readline())
        # reset standard output
        sys.stdout = sys.__stdout__
        print(self.ts_file)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
