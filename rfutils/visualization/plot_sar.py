"""plot_sar.py
"""
import os
import sys
import numpy as np
import hdf5storage
import matplotlib.pyplot as plt
import matplotlib
from cstmod.field_reader import ResultReader3D

def plot_sar(plot_filename, xdim, ydim, zdim, sar, xcenter=(0,0,0), mask=None, dims=None):
    """plot sar results as subplots: axial, coronal, sagittal
    
    Args:
        plot_filename: String, filename of the plot file
        xdim: x-dimmensions, 1d ndarray
        ydim: y-dimensions, 1d ndarray
        sar: SAR data ndarray(xdim, ydim, zdim)
        xcenter: centered plot point (x0, y0, z0)
        mask: sarmask ndarray (xdim, ydim, zdim)
        dims: tuple representing the dimensions to plot (native units)
    """
    if mask is not None:
        sar = np.multiply(sar, mask)

    if dims is not None:
        print('dims: ', dims)
        xind1 = np.argmin(np.abs(xdim-dims[0]))
        xind2 = np.argmin(np.abs(xdim-dims[1]))
        yind1 = np.argmin(np.abs(ydim-dims[2]))
        yind2 = np.argmin(np.abs(ydim-dims[3]))
        zind1 = np.argmin(np.abs(zdim-dims[4]))
        zind2 = np.argmin(np.abs(zdim-dims[5]))
    else:
        xind1 = xdim[0]
        xind2 = xdim[-1]
        yind1 = ydim[0]
        yind2 = ydim[-1]
        zind1 = zdim[0]
        zdin2 = zdim[-1]

    print('indices: ')
    print(xind1, xind2)
    print(yind1, yind2)
    print(zind1, zind2)

    xind0 = np.argmin(np.abs(xdim-xcenter[0]))
    yind0 = np.argmin(np.abs(ydim-xcenter[1]))
    zind0 = np.argmin(np.abs(zdim-xcenter[2]))

    # create the subplots
    plt.figure(figsize=(4,2), dpi=400)
    fig, ax = plt.subplots(1,3)
    fig.set_size_inches(5,3)
    sar_cmap = matplotlib.cm.get_cmap('jet')
    sar_cmap.set_under('w')

    # axial slice
    XX,YY = np.meshgrid(xdim[xind1:xind2], ydim[yind1:yind2])
    ax[0].pcolormesh(np.transpose(XX), np.transpose(YY), sar[xind1:xind2,yind1:yind2,zind0], cmap=sar_cmap, vmin=0.00001, vmax=0.6)
    ax[0].set_aspect('equal','box')
    XX,ZZ = np.meshgrid(xdim[xind1:xind2], zdim[zind1:zind2])
    ax[1].pcolormesh(np.transpose(XX), np.transpose(ZZ), np.rot90(sar[xind1:xind2,yind0,zind1:zind2],2), cmap=sar_cmap, vmin=0.00001, vmax=0.6)
    ax[1].set_aspect('equal','box')
    YY,ZZ = np.meshgrid(ydim[yind1:yind2], zdim[zind1:zind2])
    im = ax[2].pcolormesh(ZZ,YY, np.fliplr(np.rot90(sar[xind0,yind1:yind2,zind1:zind2],3)), cmap=sar_cmap, vmin=0.00001, vmax=0.6)
    ax[2].set_aspect('equal','box')
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.35, 0.01, 0.3])
    fig.colorbar(im, cax=cbar_ax)
    plt.savefig(plot_filename, dpi=100)

if __name__ == "__main__":
    if sys.platform == 'win32':
        base_dir = os.path.join(r'D:', os.sep, r'Temp_CST',
                                    r'KU_Ten_32_FDA_21Jul2021_4_6',
                                    r'Export',  r'3d',)
        sar_file_dir = os.path.join(base_dir, r'Vopgen', r'Output')
    
    sarmask_dict = hdf5storage.loadmat(os.path.join(base_dir, r'Vopgen', r'sarmask_aligned.mat'))
     
    xdim = np.array([x[0] for x in sarmask_dict['XDim']])
    ydim = np.array([y[0] for y in sarmask_dict['YDim']])
    zdim = np.array([z[0] for z in sarmask_dict['ZDim']])
    xmin = xdim[0]
    xmax = xdim[-1]
    ymin = ydim[0]
    ymax = ydim[-1]
    zmin = 0.1
    zmax = zdim[-1]
    sarmask = sarmask_dict['sarmask_new']
    sarfiles = []
    for i in range(16):
        sarfiles.append(os.path.join(sar_file_dir,r'KU_Ten_32_FDA_SAR_ch_' + str(i+1) + r'.mat'))

    for sf in sarfiles:
        sarfile = np.transpose(hdf5storage.loadmat(sf)['SAR'], (2,1,0))
        plot_sar(os.path.basename(sf)+'_plot.png', xdim, ydim, zdim, sarfile, (0.0, 0.0, 0.25), mask = sarmask, dims=(xmin, xmax, ymin, ymax, zmin, zmax))

    #
    #for i in range(16):
    #    sarfiles.append(os.path.join(base_dir, r'SAR (f=447) [AC'+str(i+1)+r'] (10g).h5'))

    
    #for sf in sarfiles:
    #    rr = ResultReader3D(sf, 'sar')
    #    xdim = rr.xdim
    #    ydim = rr.ydim
    #    zdim = rr.zdim
    #    xmin = xdim[0]
    #    xmax = xdim[-1]
    #    ymin = ydim[0]
    #    ymax = ydim[-1]
    #    zmin = 0.1
    #    zmax = zdim[-1]
    #    plot_sar(os.path.basename(sf)+'_plot.png', rr.xdim, rr.ydim, rr.zdim, rr.fields3d, (0.0, 0.0, 0.25), dims=(xmin, xmax, ymin, ymax, zmin, zmax))

