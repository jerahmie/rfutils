"""Calculate Rotating B1 field (B1+, B1-) from B1-field.
"""
import os
import hdf5storage
import numpy as np

class EMField(object):
    """A class to hold electromagnetic field data.
    """
    def __init__(self, field_file=None):
        self._field_file = field_file

    @property
    def field_file(self):
        return self._field_file

if __name__ == "__main__":
    field_cartesian_file = os.path.join('/mnt','e','CST_Backup','AC_Zero_Phase.h5')
