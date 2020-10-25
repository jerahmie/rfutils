#!/usr/bin/env python
"""plot_fields_mag.py
Plot the fields of the electromagnetic field solution.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import hdf5storage
import h5py

def plot_fields_mag(field_file):
    bf = h5py.File(field_file,'r')
    xdim = bf['Mesh line x']
    ydim = bf['Mesh line y']
    zdim = bf['Mesh line z']
    field_keys = bf.keys()
    if 'E-Field' in field_keys:
        field_type = 'E-Field'
        field_max = None
        field_min = None
    elif 'H-Field' in field_keys:
        field_type = 'H-Field'
        field_max = None
        field_min = None
    elif 'B-Field' in field_keys:
        field_type = 'B-Field'
        field_max = 1.5e-6
        field_min = 0.0
    else:
        raise('Unknown field type.  Available types: ' + str(field_type))

    print("Found field type: ", field_type)
    fpxre = bf[field_type]['x']['re']
    fpxim = bf[field_type]['x']['im']
    fpyre = bf[field_type]['y']['re']
    fpyim = bf[field_type]['y']['im']
    fpzre = bf[field_type]['z']['re']
    fpzim = bf[field_type]['z']['im']

    fp = np.zeros((len(xdim), len(ydim), len(zdim), 3), dtype=np.complex)
    fp[:,:,:,0] = fpxre + 1.0j*fpxim
    fp[:,:,:,1] = fpyre + 1.0j*fpyim
    fp[:,:,:,2] = fpzre + 1.0j*fpzim
    fp_abs = np.abs(fp[:,:,:,0]*np.conj(fp[:,:,:,0]) +
                    fp[:,:,:,1]*np.conj(fp[:,:,:,1]) +
                    fp[:,:,:,2]*np.conj(fp[:,:,:,2]))

    
    fig, ax = plt.subplots(1,3)
    plt.set_cmap('jet')
    i_ind = 80
    j_ind = 90
    k_ind = 100
    plt.sca(ax[0])
    ax[0].autoscale(enable=True, axis='both',tight=True)
    XX,YY = np.meshgrid(xdim, ydim)
    plt.pcolor(XX, YY, 1e6*np.rot90(fp_abs[:,:,k_ind],2), vmin=field_min, vmax=field_max)
    plt.colorbar()
    plt.sca(ax[1])
    ax[1].autoscale(enable=True, axis='both',tight=True)
    XX,YY = np.meshgrid(xdim, zdim)
    plt.pcolor(XX, YY, 1e6*np.rot90(fp_abs[:,j_ind,:],2), vmin=field_min, vmax=field_max)
    plt.colorbar()
    plt.sca(ax[2])
    ax[2].autoscale(enable=True, axis='both',tight=True)
    XX,YY = np.meshgrid(ydim, zdim)
    plt.pcolor(XX, YY, 1e6*np.rot90(fp_abs[i_ind,:,:],3), vmin=field_min, vmax=field_max)
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    field_file = os.path.join('D:\\', 'Temp_CST', 
    'KU_Ten_32_ELD_Dipole_element_v3_with_Rx32_feeds', 'Export','3d',
    'B1+ (f=447) [AC9].h5')
    print(os.path.exists(field_file))
    plot_fields_mag(field_file)