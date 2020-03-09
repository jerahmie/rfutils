"""CheckVopgen: run a series of checks on the vopgen output files.
"""
import os
import math
import numpy as np
import hdf5storage
import matplotlib.pyplot as plt

def plot_sar_mask(sar_mask_file):
    """
    """
    pass

def plot_bffields(bfield_file):
    """plot the b-fields
    """
    if not os.path.exists(bfield_file):
        print("Could not find bfield file: ", bfield_file)
        raise FileNotFoundError
    bfp  = hdf5storage.loadmat(bfield_file)
    bfMapArrayN = bfp['bfMapArrayN']
    if type(bfMapArrayN[0,0,0,0,0]) != type(np.array([1.0j])[0]):
        print("Wrong type.  Found type: ", type(bfMapArrayN[0,0,0,0,0]))
        raise TypeError
    
    xdim = bfp['XDim']
    ydim = bfp['YDim']
    zdim = bfp['ZDim']
    xx, yy = np.meshgrid(xdim, ydim)

    nchannels = np.shape(bfMapArrayN)[4]

    #uniform distribution
    phases_b1p_cp = np.array([2.0*i*np.pi/nchannels for i in range(nchannels)])
    b1p_cp = np.zeros((len(xdim), len(ydim), len(zdim)), dtype=np.complex)

    for channel in range(nchannels):
        b1p_cp = b1p_cp + np.exp(1.0j*phases_b1p_cp[channel]) * bfMapArrayN[:,:,:,1,channel]

    # make a plot of the results
    nxp, nyp = 3, 3
    
    dz = math.ceil(len(zdim)/(nxp*nyp))
    z_ind = range(0,len(zdim), dz)

    #plt.figure()
    plot_count = 0
    fig, ax = plt.subplots(nxp, nyp)
    for axx in ax:
        for ayy in axx:
            plt.sca(ayy)
            #plt.pcolor(xx, yy, np.abs(b1p_cp[:,:,z_ind[plot_count]]), vmin=0.0, vmax=1e-6)
            plt.pcolor(xx, yy, np.angle(b1p_cp[:,:,z_ind[plot_count]]))            
            plot_count += 1
            plt.colorbar()

    plt.show()



if "__main__" == __name__:
    vopgen_path = os.path.join('/mnt', 'Data', 'CST_Projects', 'Vopgen')
    efield_file = os.path.join(vopgen_path, 'efMapArrayN_remap.mat')
    bfield_file = os.path.join(vopgen_path, 'bfMapArrayN_remap.mat')
    sarmask_file = os.path.join(vopgen_path, 'sarmask_aligned.mat')
    print("Checking B-fields...")
    plot_bffields(bfield_file)
