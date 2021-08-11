"""xmat: extract materials from Electric and Magnetic field data smapled on
        rectangular grid.
"""

import numpy as np
from scipy.constants import epsilon_0

class NormalDielectric(object):
    """Normal Dielectric
       Parameters
       ----------
        f0 : float
            Frequency in MHz
        xdim : array_like
            X- grid points
        ydim : array_like
            Y- grid points
        zdim : array_like
            Z- grid points
        e_field_data : array_like
            E-field data sampled on rectangular grid (xdim)x(ydim)x(zdim)x(3)
        h_field_data : array_like
            H-field data sampled on rectangular grid (xdim)x(ydim)x(zdim)x(3)
    """
    def __init__(self, f0, xdim, ydim, zdim, e_field_data, h_field_data):
        self._frequency = f0*1.0e6
        self._xdim = xdim
        self._ydim = ydim
        self._zdim = zdim
        self._e_field = e_field_data
        self._h_field = h_field_data
        self._sigma_eff_x = None
        self._eps_r_x = None
        # _material_properties_valid: if False, epsilon and sigma not valid
        #  and need to be calculated
        self._material_properties_valid = False

    def _update_materials(self):
        """Update material properties.
        """
        self._extract_materials_x()

    def _extract_materials_x(self):
        """Extract material properties for X-direction.
        """
        omega0 = 2.0 * np.pi * self._frequency
        efxsq = self._e_field[:, :, :, 0]*np.conj(self._e_field[:, :, :, 0])
        deltay = self._ydim[1: -1] - self._ydim[0: -2]
        deltaz = self._zdim[1: -1] - self._zdim[0: -2]

        dy = deltay[0] # meters
        dz = deltaz[0] 

        dhzdy = np.zeros(np.shape(efxsq), dtype=np.complex)
        dhydz = np.zeros(np.shape(efxsq), dtype=np.complex)
        dhzdy[:, 1:-2, :] = 1.0 / (2.0 * dy) * (self._h_field[:, 2:-1, :, 2] -
                                                self._h_field[:, 0:-3, :, 2])
        dhydz[:, :, 1:-2] = 1.0 / (2.0 * dz) * (self._h_field[:, :, 2:-1, 1] -
                                                self._h_field[:, :, 0:-3, 1])
        self._sigma_eff_x = np.zeros(np.shape(self._e_field[:, :, :, 0]), dtype=np.double)
        self._sigma_eff_x = np.real(np.divide(np.conj(self._e_field[:, :, :, 0]) * (dhzdy - dhydz), efxsq))
        self._eps_r_x = np.zeros(np.shape(self._e_field[:, :, :, 0]), dtype=np.double)
        self._eps_r_x = np.imag((1.0 / (omega0 * epsilon_0)) *
                                np.divide(np.conj(self._e_field[:, :, :, 0]) *
                                          (dhzdy - dhydz), efxsq))
        self._material_properties_valid = True

    @property
    def sigma_eff(self):
        """Return the conductivity (S/m) calculated from the uniformly
        gridded electric and magnetic fields.
        """
        if not self._material_properties_valid:
            self._update_materials()

        return self._sigma_eff_x

    @property
    def epsilon_r(self):
        """Return the relative permittivity (unitless) calculatd from uniformly
        gridded electric and magnetic fields.
        """
        if not self._material_properties_valid:
            self._update_materials()

        return self._eps_r_x
