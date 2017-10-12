"""
Complex permittivity calculation using 4-pole Cole-Cole method.
Method and variable names follow the official material database:
http://niremf.ifac.cnr.it/docs/DIELECTRIC/AppendixC.html
"""

import numpy as np
import scipy.constants as sp_consts

class ColeCole4Pole(object):
    def __init__(self, ef=0, sig=0, dels=[], taus=[], alfs=[]):
        self._ef = ef
        self._sigma = sig
        self._dels = dels
        self._taus = taus
        self._alfs = alfs
        self._epsilon = None
        self._frequency = None

    def _epsilon_complex(self):
        """
        Calculate complex electric permittivity over given frequencies.
        """
        pass

    @property
    def ef(self):
        """Return the infinite frequency relative permittivity."""
        return self._ef

    @property
    def sigma(self):
        """Return the conductivity."""
        return self._sigma

    @sigma.setter
    def sigma(self, sig):
        """Setter for the conductivity."""
        self._sigma = sigma

    @property
    def dels(self):
        """Return the Static relative permittivities (Deltas)."""
        return self._dels
        
    @property
    def alfs(self):
        """Return the pole broadness values (alphas)."""
        return self._alfs

    @property
    def taus(self):
        """Return the relaxation times (taus)."""
        return self._taus
    

        
        
