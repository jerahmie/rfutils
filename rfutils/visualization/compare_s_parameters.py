#!/usr/bin/env python
"""Compare two S-Parameters for FDA submisson.
"""
import os
import sys
import numpy as np
import hdf5storage
import matplotlib.pyplot as plt
import skrf as rf


def plot_s_params(s1, s2, mask=None):
    """plot_s_params
    Params:
        s1: s1 matrix
        s2: s2 matrix
        mask: mask array
    """
    fig, axs = plt.subplots(1,2)

    sparam_masked = lambda x, y: np.multiply(x,y) if y is not None else x
    to_decibels = lambda s: 20*np.log10(np.abs(s))
        
    axs[0].imshow(20*np.log10(np.abs(sparam_masked(s1,mask))))
    axs[0].set_aspect('equal','box')
    axs[0].set_title('HFSS')
    im = axs[1].imshow(to_decibels(sparam_masked(s2,mask)))
    axs[1].set_aspect('equal','box')
    axs[1].set_title('CST')
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax)

def s_params_from_mat(s_params_file)->np.array:
    """s_params_from_mat
        s_params_file: mat file that contains s-parameters
    """
    s_params_dict = hdf5storage.loadmat(s_params_file)
    return s_params_dict['Smatrix']

def mask_from_mat(s_params_file)->np.array:
    """s_params_from_mat
        s_params_file: mat file that contains s-parameters
    """
    s_params_dict = hdf5storage.loadmat(s_params_file)
    return s_params_dict['Mask_S']

if __name__ == "__main__":
    s_param_prefix = os.path.join('C:\\', 'Users','jerahmie','Downloads',)
    s_params_orig_file = os.path.join(s_param_prefix, 'Smatrix.mat')
    s_params1_file = os.path.join(s_param_prefix, 'KU_Ten_32_FDA_21Jul2021_4_6.s16p')
    #s_params1_file = os.path.join(s_param_prefix, 'KU_Ten_32_FDA_21Jul2021_4_6_coupling.s16p')
    s_params1 = rf.Network(s_params1_file)

    # lambda to get frequency index
    freq_ind = lambda f, f0: np.argmin(np.abs(f-f0))

    plot_s_params(s_params_from_mat(s_params_orig_file),
                  s_params1.s[freq_ind(s_params1.f, 447e6),:,:])
    
    
    plt.show()
    