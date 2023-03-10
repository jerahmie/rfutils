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
from matplotlib import cm
try:
    import hdf5storage
    import h5py
except:
    print("This module requires HDF5 support.  Ensure h5py and hdf5storage are installed.")
from tkinter import Tk
from tkinter.filedialog import askdirectory

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
    if len(magnitudes) != field_shape[-1] or len(phases) != field_shape[-1]:
        sys.exit("Number of channels in fields does not equal number of magnitudes/phases: "
            + str(len(magnitudes)) + "/" + str(len(phases)) + ", expected: " + str(field_shape[-1]))
    fields_component = field[:,:,:,rot_dir,:]

    fields_shimmed = np.zeros(np.shape(fields_component)[0:3], dtype=complex)
    for ch in range(field_shape[-1]):
        fields_shimmed += np.multiply(magnitudes[ch], np.multiply(fields_component[:,:,:,ch], np.exp(1.0j*phases[ch]), dtype=np.complex128))
    
    return fields_shimmed

def slice_indices(xdim, ydim, zdim, point_xyz):
    """Return the indices of the x, y, z data for the given point in space.
    """
    x_ind = np.argmin(np.abs(xdim - point_xyz[0]))
    y_ind = np.argmin(np.abs(ydim - point_xyz[1]))
    z_ind = np.argmin(np.abs(zdim - point_xyz[2]))
    
    return x_ind, y_ind, z_ind
    
def plot_fields_shimmed(field3d, xdim, ydim, zdim, slice_xyz, mask=None, 
                        field_min=0.0, field_max=6.0e-6, figtitle=None):
    """plot_fields_shimmed
    Plot the shimmed fields at given slice indices
    """
    x_ind, y_ind, z_ind = slice_indices(xdim, ydim, zdim, slice_xyz)
    fig, axs = plt.subplots(1, 3, figsize=(14, 5))
    plt.set_cmap('jet')
    XX, YY = np.meshgrid(xdim, ydim)
    if mask is not None:
        if np.shape(mask) == np.shape(field3d):
            field3d = np.multiply(field3d, mask)
        else: 
            print("mask does not have same dimension as fiel3d: ",
                np.shape(field3d), ',', np.shape(mask))
    n_rot = 2
    plot_field3_axial = lambda n_rot, z_ind: np.rot90(field3d[:,:,z_ind], n_rot)
    plot_field3_coronal = lambda n_rot, y_ind: np.rot90(field3d[:,y_ind,:], n_rot)
    plot_field3_sagittal = lambda n_rot, x_ind: np.rot90(field3d[x_ind,:,:], n_rot)
    axs[0].pcolormesh(np.transpose(XX), np.transpose(YY), plot_field3_axial(n_rot, z_ind), vmin=field_min, vmax=field_max)
    axs[0].autoscale(enable=True, axis='both', tight=True)
    axs[0].set_aspect('equal','box')
    axs[0].set_title('Axial')
    XX, YY = np.meshgrid(xdim, zdim)
    axs[1].pcolormesh(np.transpose(XX),np.transpose(YY),plot_field3_coronal(n_rot, y_ind ), vmin=field_min, vmax=field_max)
    axs[1].autoscale(enable=True, axis='both', tight=True)
    axs[1].set_aspect('equal','box')
    axs[1].set_title('Sagittal')
    XX, YY = np.meshgrid(ydim, zdim)
    im = axs[2].pcolormesh(np.transpose(XX), np.transpose(YY), plot_field3_sagittal(n_rot, x_ind), vmin=field_min, vmax=field_max)
    axs[2].autoscale(enable=True, axis='both', tight=True)
    axs[2].set_aspect('equal','box')
    axs[2].set_title('Coronal')
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    if figtitle:
        fig.suptitle(figtitle)
    #plt.show()
    return fig, axs

def plot_bmag_axis(xdim, ydim, data2d, pos=0.0, axis='x', vmax=6e-6):
    """Plot the axial |B1+| cross-section map and |B1+| through a section of the 
    plot.
    Args:
        xdim:    (ndarray) x indices
        ydim:    (ndarray) y indices
        data2d:  (ndarray), real: 2-dimensional, real data array to be plotted.
        axis:    (string): 'x' or 'y', for line through data
        pos:     (real):  x- or y- position of the line through the data.
    Returns:
        handle to matplotlib figure
    Raises:
        Exception if axis not valid
    """
    if axis == 'y':
        xind = np.argmin(np.abs(xdim - pos))
        # hard-coded limits
        y1 = -0.11
        y1_ind = np.argmin(np.abs(ydim-y1))
        y2 = 0.09
        y2_ind = np.argmin(np.abs(ydim-y2))
        data1d = data2d[xind,y1_ind:y2_ind]
        x1d = ydim[y1_ind:y2_ind]
        xaxis_label = "Position along y-axis (m)"
        def line_plot(ax):
            ax.vlines(pos, ydim[y1_ind], ydim[y2_ind], colors='w', linestyle='dashed')
    elif axis == 'x':
        yind = np.argmin(np.abs(ydim - pos))
        # hard-coded limits
        x1 = -0.075
        x1_ind = np.argmin(np.abs(xdim-x1))
        x2 = 0.075
        x2_ind = np.argmin(np.abs(xdim-x2))
        data1d = data2d[x1_ind:x2_ind,yind]
        x1d = xdim[x1_ind:x2_ind]
        xaxis_label = "Position along x-axis (m)"
        def line_plot(ax):
            ax.hlines(pos, xdim[x1_ind], xdim[x2_ind], colors='w', linestyle='dashed')
    else:
        raise Exception('Bad Axis selected: must be "x", or "y"')

    fig, axs = plt.subplots(1,2)
    plt.set_cmap('jet')
    XX,YY = np.meshgrid(xdim, ydim)
    p1 = axs[0].pcolormesh(np.transpose(XX), np.transpose(YY), data2d, vmin=0.0, vmax=vmax)
    axs[0].autoscale(enable=True, axis='both', tight=True)
    axs[0].set_aspect('equal','box')
    axs[0].set_title('|B1+| Midplane (T)')
    axs[0].set_xlabel('x (m)')
    axs[0].set_ylabel('y (m)')
    line_plot(axs[0])
    plt.colorbar(p1, ax=axs[0])
    plt.ylim=vmax
    axs[1].set_title('|B1+| Along Axis (T)')
    axs[1].plot(x1d, data1d)
    axs[1].set_xlabel(xaxis_label)
    return axs

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
    #field_export_dir = "D:/CST_Projects/Self_Decoupled/Self_Decoupled_10r5t_16tx_Cosim_Tune_Match_2/Export/Vopgen"
    try:
        field_export_dir
    except NameError:
        Tk().withdraw()
        field_export_dir = askdirectory(title="Vopgen Directory")
        print("field_export_dir: ", field_export_dir)

    field_name = "bfMapArrayN.mat"
    mask_name = "sarmask_aligned.mat"
    nchannels = 16

    # plot SAR mask
    mask_dict = hdf5storage.loadmat(os.path.join(field_export_dir, mask_name))
    #plot_mask(mask_dict['sarmask_new'], mask_dict['XDim'], mask_dict['YDim'], 
    #          mask_dict['ZDim'], (0.0, 0.0, 0.0))    
 
    # plot B1+ 
    #mags = [1.0 if ch%2 == 1 else 0.0 for ch in range(nchannels)]
    mags = [1.0 for ch in range(nchannels)]

    mod360 = lambda a: a % 360
    deg2rad = lambda deg: np.pi/180 * deg

    # top ring = odd channels
    phases_top = np.pi/180*np.linspace(0, 360, num=int(nchannels/2), endpoint=False)
    phase_offset = 360 # degrees
    # bottom ring = even channels
    phases_bottom = deg2rad(phase_offset) + deg2rad(mod360(np.linspace(0, 360, num=int(nchannels/2), endpoint=False)))

    # merge phases_top and phases_bottom
    phases = np.ravel([phases_top, phases_bottom], order='F')

    print('mags: ', mags)
    print('phases: ', phases*180/np.pi)

    field_dict = hdf5storage.loadmat(os.path.join(field_export_dir, field_name))
    
    shimmed_fields = apply_shim(field_dict['bfMapArrayN'], mags, phases)

    #zpos = 0.0
    #zpos = 0.188       # center top ring
    #zpos = 0.216       # top position
    zpos = 0.259       # center of flat
    #zpos = 0.298       # center of lower ring
    figtitle = 'phase_' + str(phase_offset).replace(".","_")
    fig, axs = plot_fields_shimmed(np.abs(shimmed_fields), field_dict['XDim'],
                            field_dict['YDim'], field_dict['ZDim'], 
                            (0.0, 0.0, zpos), mask=mask_dict['sarmask_new'],
                            field_max=3e-6, figtitle=figtitle)

    zind = np.argmin(np.abs(field_dict['ZDim']-zpos))
    #ax = plot_bmag_axis(field_dict['XDim'], field_dict['YDim'], 
    #                    np.abs(shimmed_fields[:,:,zind]), pos=0, axis='y')
    fig_save_path = os.path.join(field_export_dir, 'images')
    if not (os.path.exists(fig_save_path)):
        os.mkdir(fig_save_path)

    fig.savefig(os.path.join(fig_save_path, figtitle))
    plt.show()
