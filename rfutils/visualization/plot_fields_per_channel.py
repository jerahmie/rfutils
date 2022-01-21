#!/usr/bin/env python
"""plot_fields_per_channel.py
Plot the fields per channel at a given z-location.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import hdf5storage
from tkinter import Tk
from tkinter.filedialog import askdirectory


def plot_rotating_field(rotating_fields, zval, sarmask=None):
    """Plot the rotating fields file.
    Args:
       rotating_fields - dictionary of field values
                        This expected dimensions of the fields for the rotating
                        frame: [len(XDim), len(YDim), len(ZDim), 2, nchannels]
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
    fig, axs = plt.subplots(nrows, ncols, figsize=(12, 10))
    channel_count = 0
    zind = int(np.argmin(np.abs(zdim - zval)))
    print(zind, type(zind))
    for ix in range(nrows):
        for jy in range(ncols):
            b1mag = np.multiply(np.abs(bfMapArrayN[:, :, zind, 0, channel_count],
                                np.conj(bfMapArrayN[:, :, zind, 0, channel_count])))
            b1slice = np.sqrt(np.abs(np.multiply(bfMapArrayN[:, :, zind, 0, channel_count],
                              np.conj(bfMapArrayN[:, :, zind, 0, channel_count]))))
            if sarmask is not None:
                b1slice = np.multiply(b1slice, sarmask[:, :, zind])
            axs[ix][jy].imshow(b1slice)
            channel_count += 1
            axs[ix][jy].set_title(str(channel_count))
    return axs


def plot_fields_subset(ax, fields_dict, channel, zval=0.0, sarmask = None, vmin=0.0, vmax=3e-6):
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
    b1p = fields_dict['bfMapArrayN'][:, :, zind, 0, channel-1]
    b1p_mag = np.sqrt(np.abs(np.multiply(b1p, np.conjugate(b1p))))
    if sarmask is not None:
        b1p_mag[:, :] = np.multiply(b1p_mag[:, :], sarmask[:, :, zind])

    XX, YY = np.meshgrid(xdim, ydim)
    mesh = ax.pcolormesh(np.transpose(XX), np.transpose(YY), b1p_mag[:, :],
                         vmin=0.0, vmax=vmax)
    ax.set_aspect('equal', 'box')
    ax.set_title(str(channel))

    return mesh

if __name__ == '__main__':
    try:
        vopgen_dir
    except NameError:
        Tk().withdraw()
        vopgen_dir = askdirectory(title="Vopgen Directory")
    #
    # matplotlib settings
    #
    plt.ioff()
    plt.set_cmap('jet')

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
    sarmask_new = hdf5storage.loadmat(sarmask_file)['sarmask_new']

    print("Plotting results...")
    fig1, fig1_axs = plt.subplots(1, round(nchannels/2), constrained_layout=True)
    fig2, fig2_axs = plt.subplots(1, round(nchannels/2), constrained_layout=True)
    channels_top = list(range(1, nchannels, 2))
    channels_bottom = list(range(2, nchannels + 1, 2))
    for i, ch in enumerate(channels_top):
        im1 = plot_fields_subset(fig1_axs[i], bfMapArrayN, ch, zval=0.188,
                           sarmask=sarmask_new, vmax=1e-6)
    fig1.subplots_adjust(right=0.8)
    cbar_ax = fig1.add_axes([0.85, 0.15, 0.02, 0.7])
    fig1.colorbar(im1, cax=cbar_ax)

    for i, ch in enumerate(channels_bottom):
        im2 = plot_fields_subset(fig2_axs[i], bfMapArrayN, ch, zval=0.298,
                           sarmask=sarmask_new, vmax=1e-6)
    fig2.subplots_adjust(right=0.8)
    cbar_ax = fig2.add_axes([0.85, 0.15, 0.02, 0.7])
    fig2.colorbar(im2, cax=cbar_ax)

    plt.show()
