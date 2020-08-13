"""MaterialMapper: find material that maps to given parameters
"""

import numpy as np

class MaterialMapper(object):
    """Material Mapper 
    """
    def __init__(self, material_dict=None):
        self.mat = material_dict
