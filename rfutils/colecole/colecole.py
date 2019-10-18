"""
Complex permittivity calculation using 4-pole Cole-Cole method.
Method and variable names follow the official material database:
http://niremf.ifac.cnr.it/docs/DIELECTRIC/AppendixC.html
"""

import sys
import numpy as np
from math import pi
from scipy.constants import epsilon_0

class ColeCole(object):
    def __init__(self, ef=0, sig=0, deltas=[], taus=[], alphas=[], freq=300e6):
        self._ef = ef
        self._sigma = sig
        if isinstance(deltas, list):
            self._deltas = deltas
        else:
            self._deltas = []
            self._deltas.append(deltas)
        if isinstance(taus, list):
            self._taus = taus
        else:
            self._taus = []
            self._taus.append(taus)

        if isinstance(alphas, list):
            self._alphas = alphas
        else:
            self._alphas = []
            self._alphas.append(alphas)

        self._epsilon = None
        self._frequency = freq

    def _update_epsilon(self):
        """
        Calculate complex electric permittivity over given frequencies.
        """
        omega = self._frequency*2.0*pi
        self._epsilon = self._ef + self._sigma/(1j*omega*epsilon_0)
        for i in range(len(self._deltas)):
            self._epsilon += self._deltas[i]/(1+(1j*omega*self._taus[i])**(1-self._alphas[i]))

    @property
    def ef(self):
        """Return the infinite frequency relative permittivity."""
        return self._ef

    @property
    def sigma(self):
        """Return the conductivity."""
        return self._sigma

    @sigma.setter
    def sigma(self, sigma):
        """Setter for the conductivity."""
        self._sigma = sigma

    @property
    def deltas(self):
        """Return the Static relative permittivities (Deltas)."""
        return self._deltas

    @deltas.setter
    def deltas(self, dels):
        """Set the relative permittivities."""
        if isinstance(dels, list):
            self._deltas = dels
        else:
            self._deltas = []
            self._deltas.append(dels)

    @property
    def alphas(self):
        """Return the pole broadness values (alphas)."""
        return self._alphas
        
    @alphas.setter
    def alphas(self, alphas):
        """Setter for the broadness values (alphas)."""
        if isinstance(alphas, list):
            self._alphas = alphas
        else:
            self._alphas = []
            self._alphas.append(alphas)

    @property
    def taus(self):
        """Return the relaxation times (taus)."""
        return self._taus

    @taus.setter
    def taus(self, taus):
        """Setter for relaxation times."""
        if isinstance(taus, list):
            self._taus = taus
        else:
            self._taus = []
            self._taus.append(taus)

    @property
    def epsilon(self):
        """Return the complex permittivity."""
        if self._epsilon is None:
            self._update_epsilon()
        return self._epsilon
    
def usage(process):
    """
    Display colecole usage and exit.
    """
    print("")
    print("Usage: ", process, " [ef] [sig] [deltas] [taus] [alphas] [freq] ")
    print("")
    sys.exit()

def colecole_main(args):
    """
    Calculate the complex permittivity from the command line.
    """
    if len(args) != 7:
        usage(args[0])
    cc1 = ColeCole(args[1], args[2], args[3], args[4], args[5], args[6])
    print("")
    print(" Inf. freq. rel. permittivity: ", args[1])
    print(" Conductivity: ", args[2])
    print(" Delta(s): ", args[3])
    print(" Tau(s): ", args[4])
    print(" Alpha(s): ", args[5])
    print("")
    print(self._epsilon)

if __name__ == "__main__":
    """
    Run colecole as a command line utility.
    """
    args = sys.argv
    colecole_main(args)
