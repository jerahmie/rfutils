"""MaterialMapper: find material that maps to given parameters
"""
import os
import re
import numpy as np
import hdf5storage
import numpy as np
from numpy import linalg 

class MaterialMapper(object):
    """Material Mapper 
    material_dict = 2-dimensional materials
    """
    value_index = {'Material':0, 'Eps':2, 'Mu':3, 'Kappa':4, 'Rho':5, 'K':6, 
                    'HeatCap':7, 'BloodFlow':8, 'Metabolic':9}
    def __init__(self, materials_file=None):
        self.mat = []
        self.kappa = []
        if materials_file is not None:
            self._read_materials(materials_file)

    def _read_materials(self, material_file):
        """_read_materialsn
        Read materials and assembly dictionary.
        """
        with open(material_file) as fh:
            for line in fh.readlines():
                if not (re.match('^(?:#.*|//.*)', line)):
                    self.mat.append(line.split())
        self.kappa = np.array([sublist[self.value_index['Kappa']] for sublist in self.mat], dtype=np.float64)
            
    def print_materials(self):
        """Print the materials in database.
        """
        print(self.value_index['Material'])
        for i in range(len(self.mat)):
            print(self.mat[i][self.value_index['Material']], ' ', 
                  self.mat[i][self.value_index['Eps']], ' ', 
                  self.mat[i][self.value_index['Kappa']], ' ', 
                  self.mat[i][self.value_index['Rho']])
        

    def map_materials(self, exp_Kappa):
        """map_materials
        Do the mapping between derived materials and material map.
        """
        exp_kappa_shape = np.shape(exp_Kappa)
        nkappa = np.size(exp_Kappa)
        flat_kappa = np.reshape(exp_Kappa, nkappa)
        mapped_eps = np.empty((nkappa), dtype=np.float64)
        mapped_kappa = np.empty((nkappa), dtype=np.float64)
        mapped_rho = np.empty((nkappa), dtype=np.float64)
        print('flat_kappa: ', flat_kappa)
        print(np.shape(flat_kappa))
        for i,k in enumerate(flat_kappa):
            if i%1000 == 0:
                    print(i,'/',nkappa)
            map_ind = np.argmin(np.sqrt(np.square(self.kappa - k)))
            mapped_kappa[i] = self.mat[map_ind][self.value_index['Kappa']]
            mapped_eps[i] = self.mat[map_ind][self.value_index['Eps']]
            mapped_rho[i] = self.mat[map_ind][self.value_index['Rho']]

        mapped_kappa = np.reshape(mapped_kappa, exp_kappa_shape)
        mapped_eps = np.reshape(mapped_eps, exp_kappa_shape)
        mapped_rho = np.reshape(mapped_rho, exp_kappa_shape)
        
        return mapped_kappa, mapped_eps, mapped_rho

if __name__ == "__main__":
    materials_file = os.path.join(r'D:', os.path.sep, r'Temp_CST',r'KU_Ten_32_FDA_21Jul2021_4_6',r'Duke_34y_V5_2mm_0_Duke_34y_V5_2mm.vmat')
    print(materials_file, '? ', os.path.exists(materials_file))
    mm = MaterialMapper(materials_file)
    mm.print_materials()
    