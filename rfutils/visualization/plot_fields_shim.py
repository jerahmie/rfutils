#!/usr/bin/env python
""" plot_fields_shim.py
Plot the shimmed fields for a set of magnitudes and phases.
"""
import os
import sys
import re
if sys.platform == 'win32':
    import fnmatch
else:
    import glob
import numpy as np
import matplotlib.pyplot as plt
try:
    import hdf5storage
    import h5py
except:
    print("This module requires HDF5 support.  Ensure h5py and hdf5storage are installed.")

def apply_shim(field, magnitudes, phases, rot_dir=0):
    """apply_shim 
    Apply the magnitude & phase shim to the vopgen-formatted field array
    Args:
        field: ndarray of field values
        magnitudes: (1,Nchannels) shim magnitudes 
        phases: (1,Nchannels) shim phases (radians)
    Returns:
    Raises
    """
    field_shape = np.shape(field)
    if len(magnitudes) != field_shape[-1]:
        sys.exit("Number of channels in fields does not equal number of magnitudes/phases: "
            + str(len(magnitudes) + "/" + str(len(phases) + "/" + str(field_shape[-1]))))
    fields_component = field[:,:,:,rot_dir,:]

    fields_shimmed = np.zeros(np.shape(fields_component)[0:3], dtype=complex)
    #print('fields_shimmed: ', np.shape(fields_shimmed)[0:2])
    #print('field_component: ', np.shape(fields_component)[0:3])
    for ch in range(field_shape[-1]):
        fields_shimmed += np.multiply(fields_component[:,:,:,ch], np.exp(1.0j*phases[ch]), dtype=np.complex128)
    
    return  fields_shimmed

def slice_indices(xdim, ydim, zdim, point_xyz):
    """Return the indices of the x, y, z data for the given point in space.
    """
    x_ind = np.argmin(np.abs(xdim - point_xyz[0]))
    y_ind = np.argmin(np.abs(ydim - point_xyz[1]))
    z_ind = np.argmin(np.abs(zdim - point_xyz[2]))
    
    return x_ind, y_ind, z_ind
    
def plot_fields_shimmed(field3d, xdim, ydim, zdim, slice_xyz, mask=None, 
                        field_min=0.0, field_max=3.0e-6):
    """plot_fields_shimmed
    Plot the shimmed fields at given slice indices
    """
    x_ind, y_ind, z_ind = slice_indices(xdim, ydim, zdim, slice_xyz)
    fig, axs = plt.subplots(1,3)
    plt.set_cmap('jet')
    XX, YY = np.meshgrid(xdim, ydim)
    if mask is not None:
        if np.shape(mask) == np.shape(field3d):
            field3d = np.multiply(field3d, mask)
        else: 
            print("mask does not have same dimension as fiel3d: ",
                np.shape(field3d), ',', np.shape(mask))
    axs[0].pcolormesh(np.transpose(XX), np.transpose(YY), field3d[:,:,z_ind], vmin=field_min, vmax=field_max)
    axs[0].autoscale(enable=True, axis='both', tight=True)
    axs[0].set_aspect('equal','box')
    axs[0].set_title('Axial')
    XX, YY = np.meshgrid(xdim, zdim)
    axs[1].pcolormesh(np.transpose(XX),np.transpose(YY),field3d[:,y_ind,:], vmin=field_min, vmax=field_max)
    axs[1].autoscale(enable=True, axis='both', tight=True)
    axs[1].set_aspect('equal','box')
    axs[1].set_title('Sagittal')
    XX, YY = np.meshgrid(ydim, zdim)
    im = axs[2].pcolormesh(np.transpose(XX), np.transpose(YY), field3d[x_ind,:,:], vmin=field_min, vmax=field_max)
    axs[2].autoscale(enable=True, axis='both', tight=True)
    axs[2].set_aspect('equal','box')
    axs[2].set_title('Coronal')
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    plt.show()

def plot_mask(mask, xdim, ydim, zdim, slice_xyz):
    """Plot the field mask through given slices"""
    x_ind, y_ind, z_ind = slice_indices(xdim, ydim, zdim, slice_xyz)
    fig, axs = plt.subplots(2,3)
    plt.set_cmap('jet')
    XX,YY = np.meshgrid(xdim, ydim)
    print(np.shape(mask))
    print(np.shape(axs))
    axs[0][0].pcolormesh(mask[:,:,z_ind])
    axs[0][1].pcolormesh(mask[:,y_ind,:])
    axs[0][2].pcolormesh(mask[x_ind,:,:])
    axs[1][0].pcolormesh(mask.max(axis=2))
    axs[1][1].pcolormesh(mask.max(axis=1))
    axs[1][2].pcolormesh(mask.max(axis=0))
    plt.show()

if __name__ == "__main__":
    nchannels = 16
    #field_export_dir = os.path.join("F:", os.sep, "16Tx_7T_LB Phantom_40mm shield_1_4_1","Export","3d","Vopgen")
    field_export_dir = os.path.join(r'D:', os.sep, r'Temp_CST',r'KU_Ten_32_FDA_21Jul2021_4_6',r'Export',r'3d',r'Vopgen')
    field_name = "bfMapArrayN.mat"
    mask_name = "sarmask_aligned.mat"

    # plot SAR mask
    mask_dict = hdf5storage.loadmat(os.path.join(field_export_dir, mask_name))
    #plot_mask(mask_dict['sarmask_new'], mask_dict['XDim'], mask_dict['YDim'], 
    #          mask_dict['ZDim'], (0.0, 0.0, 0.0))    
    
    # plot B1+ 
    #mags = [1.0 if ch%2 == 1 else 0.0 for ch in range(nchannels)]
    mags = [1.0 for ch in range(nchannels)]
    print(mags)
    #cp_phases_top = [1.0*np.pi/nchannels * ch  for ch in range(0,nchannels,2)]
    #cp_phases_bottom = [-2.0*np.pi/nchannels + np.pi/nchannels * ch for ch in range(1,nchannels,2)]
    #cp_phases_top = [-1.0*np.pi/nchannels * ch  for ch in range(0,nchannels,2)]
    #cp_phases_bottom = [2*np.pi/nchannels - np.pi/nchannels * ch for ch in range(1,nchannels,2)]    
    #cp_phases = [None]*(len(cp_phases_top) + len(cp_phases_bottom))
    #cp_phases[::2] = cp_phases_top
    #cp_phases[1::2] = cp_phases_bottom
    #print(np.array(cp_phases) * 180/np.pi)
    #cable_phases = [11.3139, 13.0444, 9.7166, 11.4470, 8.1194, 11.5801, 9.7166, 13.0443, 11.3139,  13.0443, 9.5835, 11.5801, 8.1194, 11.5801, 9.8497, 13.0443]
    #cp_phases = np.array(cp_phases) + np.array(cable_phases)
    cp_phases = np.pi/180*np.array([54.2514, -115.9637, 54.8956, -82.2456, 61.7822, -75.7515, 51.0311, 129.0421, -77.4862,  71.8050, -36.3305, 163.3601, -81.7879, 51.7028, -169.5938, -92.9703])
    
    #sys.exit()
    field_dict = hdf5storage.loadmat(os.path.join(field_export_dir, field_name))
    shimmed_fields = apply_shim(field_dict['bfMapArrayN'], mags, cp_phases)
    print(cp_phases)
    plot_fields_shimmed(np.abs(shimmed_fields), field_dict['XDim'],
                         field_dict['YDim'], field_dict['ZDim'], 
                         (0.0, 0.0, 0.25), mask_dict['sarmask_new'])

