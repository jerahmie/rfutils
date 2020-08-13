#!/bin/env python
"""Construct a dictionary of materials from a materials file.
"""

import os
import sys
import csv
import re
import pandas as pd
from abc import ABC


class MaterialsDB(ABC):
    """Base class to construct database of materials.
    """
    def _load_materials(self):
        pass

class MaterialsDBVirtualFamily(MaterialsDB):
    """MaterialsDB constructed from Virtual Family materials file.
    """ 
    def __init__(self, vmat_filename):
        if os.path.exists(vmat_filename):
            self._vmat_filename = vmat_filename
        else:
            self._vmat_filename = None

    def _load_materials(self):
        """Load materials from file and create a materials dictionary
        """
        #csv.register_dialect('skip_space', skipinitialspace=True)
        #with open(self._vmat_filename, 'r') as csvfile:
        #    material_reader = csv.reader(csvfile, delimiter='\t', dialect='skip_space')
        #    next(material_reader)
        #    next(material_reader)
        #    for row in material_reader:
        #        print('|'.join(row))
        df = pd.read_csv(self._vmat_filename, sep='\t|[ ]*', engine='python')
        print(df)