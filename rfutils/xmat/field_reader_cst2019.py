"""
Implement concrete field reader class for CST 2019.
"""
import os
import re
import glob
try:
    import h5py
except: 
    print("Field reader requires HDF5 support.  Ensure package h5py is installed.")

try:
    import numpy as numpy
except:
    print("Field reader requires Numpy.  Ensure package numpy is installed.")

from rfutils.xmat import FieldReader

class FieldReaderCST2019(FieldReader):
    """Concrete implementation of FieldReader for CST2019 and later that uses
    HDF5 export format.
    """
    def __init__(self):
        self._ex = None
        self._ey = None
        self._ez = None
        self._bx = None
        self._by = None
        self._bz = None
        self._field_file_list = []

    def read_fields(self, file_names, field_channel_dict = None):
        """Read fields from list of files.  If naming rules are observed, an
        attempt is made to automatically populate the field matrices. If 
        field_channel_dict is not None, an attempt will be made to populate the
        field matrices accordingly.
        """
        if not field_channel_dict:
            self._process_file_list(file_names)
            for file_name in self._field_file_list:
                if not os.path.exists(file_name):
                    print("Could not find file: ", file_name)
                    raise FileNotFoundError
                
                
        else:
            raise Exception("Alternative mapping of field files has not been implemented.")

        

    def _process_file_list(self, file_name_patterns):
        """Generate a list of files that matches a provided regular expression.
        """
        file_list = []
        for pattern in file_name_patterns:
            for file_name in glob.glob(pattern):
                file_list.append(file_name)
        # This one-liner generates a list of filenames sorted by the
        # '[ACn]' string portion of the filename.
        self._field_file_list = sorted(file_list, key=lambda fl: int(re.search('\[AC([\d]+)\]', fl).group(1)))

        return self._field_file_list
