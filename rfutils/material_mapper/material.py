"""MaterialMapper: find material that maps to given parameters
"""

import numpy as np

class Material(object):
    """Material Object: contains material info.
    """
    def __init__(self, frequency=300.0e6, name="", epsr=1.0, sigma=0.0,
                 density=0.0):
        self._frequency = frequency
        self._name = name
        self._epsr = epsr
        self._sigma = sigma
        self._density = density

    def __str__(self):
        matstr = "Material: " + self._name + "\n" + \
                 "\t - Permittivity: " + str(self._epsr) + "\n" + \
                 "\t - Conductivity: " + str(self._sigma) + " (S/m) \n" + \
                 "\t -      Density: " + str(self._density) + " (m^-3) \n"
        return matstr
        
    @property
    def frequency(self):
        """Return the material frequency.
        """
        return self._frequency
    
    @frequency.setter
    def frequency(self, frequency):
        """Update the material frequency.
        """
        self._frequency = frequency
    
    @property
    def name(self):
        """Return the name of the material.
        """
        return self._name

    @name.setter
    def name(self, name):
        """Update the material name.
        """
        self._name = name

    @property
    def sigma(self):
        """Return the material conductivity (S/m)
        """
        return self._sigma
    
    @sigma.setter
    def sigma(self, sigma):
        """Update the material conductivity (S/m)
        """
        self._sigma = sigma

    @property
    def epsr(self):
        """Return the relative permittivity of the material.
        """
        return self._epsr

    @epsr.setter
    def epsr(self, epsr):
        """Update the material relative permittivity.
        """
        self._epsr = epsr
