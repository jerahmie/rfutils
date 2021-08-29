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
    def __init__(self, f0, xdim, ydim, zdim, e_field_data, h_field_data, current_density=None):
        self._frequency = f0*1.0e6
        self._xdim = xdim
        self._ydim = ydim
        self._zdim = zdim
        self._e_field = e_field_data
        self._h_field = h_field_data
        self._j_density = current_density
        self._sigma_eff_x = None
        self._sigma_eff_y = None
        self._sigma_eff_z = None
        self._sigma_eff_from_j = None
        self._eps_r_x = None
        self._eps_r_y = None
        self._eps_r_z = None
        # _material_properties_valid: if False, epsilon and sigma not valid
        #  and need to be calculated
        #self._material_properties_valid = False
        #self._sigma_properties_valid = False
        #self._eps_properties_valid = False

    def _update_materials(self):
        """Update material properties.
        """
        self._extract_materials_x()
        if self._j_density is not None:
            self._extract_conductivity_from_currents()

    def _extract_conductivity_from_currents(self):
        """Extract material properties from currents and electric fields.
        """
        self._sigma_eff_from_j = np.zeros(np.shape(self._j_density))
        self._sigma_eff_from_j[:,:,:,0] = np.abs(np.divide(self._j_density[:,:,:,0],
                                                           self._e_field[:,:,:,0]))
        self._sigma_eff_from_j[:,:,:,1] = np.abs(np.divide(self._j_density[:,:,:,1],
                                                           self._e_field[:,:,:,1]))
        self._sigma_eff_from_j[:,:,:,2] = np.abs(np.divide(self._j_density[:,:,:,2],
                                                           self._e_field[:,:,:,2]))

    def _extract_materials_x(self):
        """Extract material properties for X-direction.
        """
        omega0 = 2.0 * np.pi * self._frequency
        efxsq = np.abs(self._e_field[:, :, :, 0]*np.conj(self._e_field[:, :, :, 0]))
        deltay = self._ydim[1: -1] - self._ydim[0: -2]
        deltaz = self._zdim[1: -1] - self._zdim[0: -2]

        dy = deltay[0]
        dz = deltaz[0]
        print('omega0: ', omega0)

        print('_extract_materials_x: ', dy, ', ', dz)
        dhzdy = np.zeros(np.shape(efxsq), dtype=np.complex128)
        dhydz = np.zeros(np.shape(efxsq), dtype=np.complex128)
        dhzdy[:, 1:-2, :] = 1.0 / (2.0 * dy) * (self._h_field[:, 2:-1, :, 2] -
                                                self._h_field[:, 0:-3, :, 2])
        dhydz[:, :, 1:-2] = 1.0 / (2.0 * dz) * (self._h_field[:, :, 2:-1, 1] -
                                                self._h_field[:, :, 0:-3, 1])
        self._sigma_eff_x = np.zeros(np.shape(self._e_field[:, :, :, 0]), dtype=np.float64)
        self._sigma_eff_x = np.real(np.divide(np.conj(self._e_field[:, :, :, 0]) * (dhzdy - dhydz), efxsq))
        self._eps_r_x = np.zeros(np.shape(self._e_field[:, :, :, 0]), dtype=np.float64)
        self._eps_r_x = (1.0 / (omega0 * epsilon_0))* np.imag(np.divide(np.conj(self._e_field[:, :, :, 0]) * (dhzdy - dhydz), efxsq))
        #self._material_properties_valid = True

    @property
    def sigma_eff(self):
        """Return the conductivity (S/m) calculated from the uniformly
        gridded electric and magnetic fields.
        """
        self._update_materials()

        return self._sigma_eff_x

    @property
    def epsilon_r(self):
        """Return the relative permittivity (unitless) calculatd from uniformly
        gridded electric and magnetic fields.
        """
        #if not self._material_properties_valid:
        self._update_materials()

        return self._eps_r_x

    @property
    def sigma_eff_from_currents(self):
        """Return the effective conductivity derived from conduction current
        density.
        """
        self._extract_conductivity_from_currents()

        return self._sigma_eff_from_j
