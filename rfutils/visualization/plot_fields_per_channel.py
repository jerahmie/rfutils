#!/usr/bin/env python
"""plot_fields_per_channel.py
Plot the fields per channel at a given z-location.
"""

import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import hdf5storage
import h5py

def plot_rotating_field(rotating_fields, zval, sarmask = None):
    """Plot the rotating fields file.  
    Args:
       rotating_fields - dictionary of field values 
                        This expected dimensions of the fields for the rotating 
                        frame are: [len(XDim), len(YDim), len(ZDim), 2, nchannels] 
       zval - z-value of slice location

    Returns:
        axs - plot axis handle
    """
    xdim = rotating_fields['XDim']
    ydim = rotating_fields['YDim']
    zdim = rotating_fields['ZDim']

    #
    # load the bfield data matrix from the field dictionary
    #
    bfMapArrayN = rotating_fields['bfMapArrayN']
    bfMapArrayN_shape = np.shape(bfMapArrayN)
    nchannels = bfMapArrayN_shape[-1]
    ncols = int(np.floor(np.sqrt(nchannels)))
    nrows = int(np.ceil(nchannels/ncols))
    fig, axs = plt.subplots(nrows, ncols, figsize=(12,10))
    channel_count = 0
    zind = int(np.argmin(np.abs(zdim - zval)))
    print(zind, type(zind))
    for ix in range(nrows):
        for jy in range(ncols):
            b1mag = np.multiply(np.abs(bfMapArrayN[:,:,zind,0,channel_count], np.conj(bfMapArrayN[:,:,zind, 0, channel_count])))
            b1slice = np.sqrt(np.abs(np.multiply(bfMapArrayN[:,:,zind,0,channel_count], \
                        np.conj(bfMapArrayN[:,:,zind,0,channel_count]))))
            if sarmask is not None:
                b1slice = np.multiply(b1slice, sarmask[:,:,zind])
            axs[ix][jy].imshow(b1slice)
            channel_count += 1
            axs[ix][jy].set_title(str(channel_count))
    return axs

def plot_fields_subset(ax, fields_dict, channel, zval=0.0, sarmask = None):
    """Plot a subset of the channels.  
    Args:
        fields_dict - fields dictionary
        channels - list of channels to plot
        zval - plane to plot
        sarmask - mask of results
    Returns:
        axs - plot axis handle
    """
    xdim = fields_dict['XDim']
    ydim = fields_dict['YDim']
    zdim = fields_dict['ZDim']
    zind = np.argmin(np.abs(zdim-zval))
    # plot the results
    b1p = fields_dict['bfMapArrayN'][:,:,zind,0,channel-1]
    b1p_mag = np.sqrt(np.abs(np.multiply(b1p, np.conjugate(b1p))))
    if sarmask is not None:
        b1p_mag[:,:] = np.multiply(b1p_mag[:,:], sarmask[:,:,zind])

    XX,YY = np.meshgrid(xdim, ydim)
    mesh = ax.pcolormesh(np.transpose(XX),np.transpose(YY),b1p_mag[:,:], vmin=0.0, vmax=1e-6)
    ax.set_aspect('equal','box')
    ax.set_title(str(channel))

    return mesh

if __name__ == '__main__':
    if sys.platform == "win32":
        vopgen_dir = os.path.join('D:\\','Temp_CST','Vopgen','KU_ten_32_Tx_MRT_23Jul2019','Vopgen')
    elif sys.platform == "linux":
        #matplotlib.use('Qt5Agg')
        #vopgen_dir = os.path.join('/mnt','Data','Temp_CST','Vopgen','KU_ten_32_Tx_MRT_23Jul2019','Vopgen')
        vopgen_dir = os.path.join('/mnt','Data','Temp_CST','KU_Ten_32_FDA_21Jul2021_4_6','Export','3d','Vopgen')

    else:
        sys.exit('Could not identify OS.')

    #
    # matplotlib settings
    #
    plt.ioff() 
    
    #
    # load the bfield data for the given channels
    #
    print("Reading data...")
    b1map_array_file = os.path.join(vopgen_dir, 'bfMapArrayN.mat')
    bfMapArrayN = hdf5storage.loadmat(b1map_array_file)
    bf_shape = np.shape(bfMapArrayN['bfMapArrayN'])
    nchannels = bf_shape[-1]

    #
    # load the sarmask
    #
    sarmask_file = os.path.join(vopgen_dir, 'sarmask_aligned.mat')
    sarmask_new =  hdf5storage.loadmat(sarmask_file)['sarmask_new']
    

    print("Plotting results...")
    fig1, fig1_axs = plt.subplots(1, round(nchannels/2), constrained_layout=True)
    fig2, fig2_axs = plt.subplots(1, round(nchannels/2), constrained_layout=True)
    channels_top = list(range(1,nchannels,2))
    channels_bottom = list(range(2,nchannels+1,2))
    for i, ch in enumerate(channels_top):
        plot_fields_subset(fig1_axs[i], bfMapArrayN, ch, zval=0.2, sarmask=sarmask_new)

    for i, ch in enumerate(channels_bottom):
        plot_fields_subset(fig2_axs[i], bfMapArrayN, ch, zval=0.4, sarmask=sarmask_new)
    plt.show()