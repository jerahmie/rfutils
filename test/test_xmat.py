"""
Unit tests for rfutils.xmat (material extraction).

"""
import os
import unittest
import numpy as np
import h5py
import matplotlib.pyplot as plt
from cstmod.field_reader import FieldReaderCST2019
from rfutils import xmat

class TestXmat(unittest.TestCase):
    """Unit test for xmat material extraction."""
    @classmethod
    def setUpClass(cls):

        # load field data
        cls.test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                         '..', 'test_data'))

        cls.emag_image_filename = os.path.join(cls.test_data_dir,
                                               'emag_test.png')

        cls.epsr_image_filename = os.path.join(cls.test_data_dir,
                                               'epsr_test.png')

        cls.sigma_image_filename = os.path.join(cls.test_data_dir,
                                                'sigma_test.png')

        # cleanup previous results
        if os.path.exists(cls.emag_image_filename):
            os.remove(cls.emag_image_filename)

        if os.path.exists(cls.epsr_image_filename):
            os.remove(cls.epsr_image_filename)

        if os.path.exists(cls.sigma_image_filename):
            os.remove(cls.sigma_image_filename)

        # load E-field data
        with h5py.File(os.path.join(cls.test_data_dir,
                                    'e-field (f=447) [pw].h5')) as data_ef:
            print(data_ef.keys())
            cls.xdime = data_ef['Mesh line x'][()]
            cls.ydime = data_ef['Mesh line y'][()]
            cls.zdime = data_ef['Mesh line z'][()]
            exre = np.transpose(data_ef['E-Field']['x']['re'], (2, 1, 0))
            exim = np.transpose(data_ef['E-Field']['x']['im'], (2, 1, 0))
            eyre = np.transpose(data_ef['E-Field']['y']['re'], (2, 1, 0))
            eyim = np.transpose(data_ef['E-Field']['y']['im'], (2, 1, 0))
            ezre = np.transpose(data_ef['E-Field']['z']['re'], (2, 1, 0))
            ezim = np.transpose(data_ef['E-Field']['z']['im'], (2, 1, 0))

            cls.efield_data = np.zeros((np.shape(exre)[0],
                                        np.shape(exre)[1],
                                        np.shape(exre)[2], 3),
                                       dtype=np.complex)
            cls.efield_data[:, :, :, 0] = exre + 1.0j * exim
            cls.efield_data[:, :, :, 1] = eyre + 1.0j * eyim
            cls.efield_data[:, :, :, 2] = ezre + 1.0j * ezim

        with h5py.File(os.path.join(cls.test_data_dir,
                                    'h-field (f=447) [pw].h5')) as data_hf:
            cls.xdimh = data_hf['Mesh line x'][()]
            cls.ydimh = data_hf['Mesh line y'][()]
            cls.zdimh = data_hf['Mesh line z'][()]
            hxre = np.transpose(data_hf['H-Field']['x']['re'], (2, 1, 0))
            hxim = np.transpose(data_hf['H-Field']['x']['im'], (2, 1, 0))
            hyre = np.transpose(data_hf['H-Field']['y']['re'], (2, 1, 0))
            hyim = np.transpose(data_hf['H-Field']['y']['im'], (2, 1, 0))
            hzre = np.transpose(data_hf['H-Field']['z']['re'], (2, 1, 0))
            hzim = np.transpose(data_hf['H-Field']['z']['im'], (2, 1, 0))
            cls.hfield_data = np.zeros((np.shape(hxre)[0],
                                        np.shape(hxre)[1],
                                        np.shape(hzre)[2], 3),
                                       dtype=np.complex)
            cls.hfield_data[:, :, :, 0] = hxre + 1.0j * hxim
            cls.hfield_data[:, :, :, 1] = hyre + 1.0j * hyim
            cls.hfield_data[:, :, :, 2] = hzre + 1.0j * hzim

    def setUp(self):
        """Load data required for tests.
        """
        self.frequency_0 = 447e6 # Center frequency, Hz
        self.normal_dielectric = xmat.NormalDielectric(self.frequency_0,
                                                       self.xdime,
                                                       self.ydime,
                                                       self.zdime,
                                                       self.efield_data,
                                                       self.hfield_data)

    def test_framework_setup(self):
        """Test the Unittest class is setup correctly and all modules are
            present.
        """
        self.assertTrue(True)

    def test_normal_dielectric_object(self):
        """Test normal dielectric class.
        """
        self.assertIsInstance(self.normal_dielectric, xmat.NormalDielectric)

    def test_normal_dielectric_materials(self):
        """Test material extraction for plane waves.
        """
        emag = np.abs(np.sqrt(self.efield_data[:, :, :, 0] *
                              np.conj(self.efield_data[:, :, :, 0]) +
                              self.efield_data[:, :, :, 1] *
                              np.conj(self.efield_data[:, :, :, 1]) +
                              self.efield_data[:, :, :, 2] *
                              np.conj(self.efield_data[:, :, :, 2])))
        xx, yy = np.meshgrid(self.xdime, self.ydime)
        nrow = 3
        ncol = 3
        fig, axs = plt.subplots(nrow, ncol, figsize=(18, 16))
        delta_zslice = round(len(self.zdime)/(nrow * ncol + 1))
        kz_slice = delta_zslice  # ignore the top boundary
        for ax in axs.reshape(-1):
            plt.sca(ax)
            plt.pcolor(np.transpose(xx), np.transpose(yy),
                       emag[:, :, kz_slice])
            plt.colorbar()
            kz_slice += delta_zslice
            ax.set_aspect('equal')
        plt.savefig(self.emag_image_filename)

    def test_material_extraction(self):
        """Test extraction of material properties from field values.
        """
        print(self.normal_dielectric.__dict__.keys())
        self.assertTrue(hasattr(self.normal_dielectric, 'epsilon_r'))
        self.assertTrue(hasattr(self.normal_dielectric, 'sigma_eff'))
        epsr = self.normal_dielectric.epsilon_r
        self.assertEqual(len(np.shape(epsr)), 3)
        sigma = self.normal_dielectric.sigma_eff
        self.assertEqual(len(np.shape(sigma)), 3)

        # save figure snapshots
        # plot epsilon_r
        xx, yy = np.meshgrid(self.xdime, self.ydime)
        nrow = 3
        ncol = 3
        save_snapshots_3D(ncol, nrow, self.xdime, self.ydime, epsr, 
                          os.path.join(self.test_data_dir, 'epsr_test.png'))

        # plot negative epsilon_r values (should be very few, if any)
        negative_epsr_ind = np.where(epsr < 0.0)
        negative_epsr = np.zeros(np.shape(epsr), dtype = np.double)
        negative_epsr[negative_epsr_ind] = epsr[negative_epsr_ind]
        
        save_snapshots_3D(ncol, nrow, self.xdime, self.ydime, negative_epsr,
                          os.path.join(self.test_data_dir, 'negative_epsr.png'))
        # plot conductivity
        save_snapshots_3D(ncol, nrow, self.xdime, self.ydime, sigma,
                          os.path.join(self.test_data_dir, 'sigma_test.png'))
        
        negative_sigma_ind = np.where( sigma < 0.0)
        negative_sigma  = np.zeros(np.shape(sigma), dtype = np.double)
        negative_sigma[negative_sigma_ind] = sigma[negative_sigma_ind]

        save_snapshots_3D(ncol, nrow, self.xdime, self.ydime, negative_sigma,
                          os.path.join(self.test_data_dir, 'negative_sigma.png'))
        
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

def save_snapshots_3D(nrow, ncol, xdim, ydim, data, filename):
    """Helper plot routine for material property data.
    """
    xx, yy = np.meshgrid(xdim, ydim)
    delta_zslice = round(np.shape(data)[2] / (nrow * ncol + 1))
    kz_slice = delta_zslice
    fig, axs = plt.subplots(nrow, ncol, figsize=(18,16))
    for ax in axs.reshape(-1):
        plt.sca(ax)
        plt.pcolor(np.transpose(xx), np.transpose(yy), data[:,:,kz_slice])
        plt.colorbar()
        kz_slice += delta_zslice
        ax.set_aspect('equal')
    plt.savefig(filename)
    
if __name__ == "__main__":
    unittest.main()
