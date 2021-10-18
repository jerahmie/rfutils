#!/usr/bin/env python
"""Plot list of touchstone files.
"""

import sys
import os
import numpy as np
import skrf as rf
import matplotlib.pyplot as plt

def usage():
    """Print usage and exit.
    """
    print("")
    print("Usage: ")
    print(" plot_s_parameters.py touchstone1.s1p touchstone2.s1p ....")
    print("")
    sys.exit()

def print_s_params_at_freq(ntwk, freq0 = 447e6):
    """Print a set of s-parameter magnitude and phases.
    """
    print(dir(ntwk))

def plot_s_parameters(touchstone_file_list):
    """Plot all values of touchstone file.
    """
    ntwk0 = rf.Network(touchstone_file_list[0])

    # number of channels in touchstone file
    nchannels = np.shape(ntwk0.s)[-1]

    # plot the magnitudes    
    fig1, axs = plt.subplots(np.int(np.ceil(np.sqrt(nchannels))),
                             np.int(np.ceil(np.sqrt(nchannels))))

    for file in touchstone_file_list:
        print("file: ", file)
        ntwk = rf.Network(file)
        ntwk.frequency.unit = 'mhz'
        idx = 0
        for axx in axs:
            for ayy in axx:
                plt.sca(ayy)
                if idx < nchannels:
                    ntwk.plot_s_db(n=idx,m=idx)
                    plt.vlines(447e6,-40,0,linestyle='dashed', label='447 MHz')
                idx += 1

    fig2, axs = plt.subplots(np.int(np.ceil(np.sqrt(nchannels))),
                             np.int(np.ceil(np.sqrt(nchannels))))

    for file in touchstone_file_list:
        print("file: ", file)
        ntwk = rf.Network(file)
        ntwk.frequency.unit = 'mhz'
        idx = 0
        for axx in axs:
            for ayy in axx:
                plt.sca(ayy)
                if idx < nchannels:
                    ntwk.plot_s_deg(n=idx,m=idx)
                    plt.vlines(447e6,-40,0,linestyle='dashed', label='447 MHz')
                idx += 1

    plt.show()

def s_matrix_at_freq(smatrix1_file, freq=447e6):
    """Return the smatrix at the frequency of interest.
    
        Args:

        Returns: NxN numpy matrix.
    """
    #freq1 = rf.Frequency(freq, freq, 1, 'Hz')
    
    smat = rf.Network(smatrix1_file)
    m,n = np.shape(smat.s)[1], np.shape(smat.s)[2]
    if m != n:
        print("S-matrix is malformed.")
        return None
    s_at_freq = np.zeros((m,n), dtype=np.complex)
    freq_ind = np.argmin(np.abs(smat.f - freq))
    for i in range(m):
        for j in range(n):
            s_at_freq[i,j] = smat.s[freq_ind, i, j]

    return s_at_freq

def rms_error_at_freq(s1, s2):
    """Calculate the rms error between two nxn scattering parameter 
        matrices.

        Args:
            param1: s1, numpy matrix representing first NxN array of
                     S-parameters 
            param2: s2, numpy matrix representing second NxN array of 
                     S-parameters
        Returns:
            RMS error between s1, s2
        
    """
    if np.shape(s1) != np.shape(s2):
        print("S-matrix shapes not equal: (",
              np.shape(s1), ") vs (", np.shape(s2) ,")"  )
        return -1

    nn = np.shape(s1)[0]

    sqe = 0  # mean square error

    sqe_angle = 0
    for i in range(nn):
        for j in range(nn):
            if i == j:
                sqe += (np.abs(s1[i,j]) - np.abs(s2[i,j]))**2
                sqe_angle += (np.angle(s1[i,j]) - np.angle(s2[i,j]))**2
            else:
                # off-diagonal elements symmetric are reduced by half to weight
                # appropriately to on-diagonal elements
                sqe += 0.5*(np.abs(s1[i,j]) - np.abs(s2[i,j]))**2
                sqe_angle +=  0.5*(np.angle(s1[i,j]) - np.angle(s2[i,j]))**2

    rmse = np.sqrt(sqe/(nn**2))
    rmse_angle = np.sqrt(sqe_angle/(nn**2))
    return rmse, rmse_angle


#def compare_sparam_at_freq(touchstone_file_list, freq=447e6):
#   """Compare two touchstone files at the frequency of interest.
#        plot the sparameter map 
#        calculate the RMS error between the touchstone files
#    """


if __name__ == "__main__":
    #    usage()
    data_dir = os.path.join('D:\\','Temp_CST',)
    data_file_list = ['8CH-ELD_KU32insert_Lightbulb_rot22p5deg_08-17-2020.s8p',
                      '8CH-ELD_KU32insert_Lightbulb_RXtrap-tuned_09-28-20.s8p']
    full_data_file_list = [os.path.join(data_dir, file) for file in data_file_list]
    for file in full_data_file_list:
        print(file, ' exists? ', os.path.exists(file))
    
    plot_s_parameters(full_data_file_list)
