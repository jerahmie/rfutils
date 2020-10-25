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
    fig = plt.figure()
    for file in touchstone_file_list:
        print("file: ", file)
        ntwk = rf.Network(file)
        ntwk.frequency.unit = 'mhz'
        ntwk.plot_s_db(n=0,m=0)
    plt.gca()
    plt.vlines(470e6,-40,0,linestyle='dashed', label='470 MHz')
    plt.vlines(447e6,-40,0,linestyle='dashed', label='447 MHz')
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
    #if len(sys.argv) > 1:
    #    plot_s_parameters(sys.argv[1:])
    #else:
    #    usage()
    data_dir = os.path.join('D:\\','Temp_CST',)
    #data_file_list = ['8CH_ELdipole_commongnd-23cmCONE_notraps_cloneELDipole_6-30-2020.s8p',
    #                  'KU_Ten_32_8CH_RL_Tx_Dipole_Tuned_v2_4_opt1.s8p']
    data_file_list = ['KU_Ten_32_ELD_Dipole_element_v3_with_Rx32_5_28Sept2020.s8p',
                      '8CH-ELD_KU32insert_Lightbulb_RXtrap-tuned_09-28-20.s8p']
    full_data_file_list = [os.path.join(data_dir, file) for file in data_file_list]
    for file in full_data_file_list:
        print(file, ' exists? ', os.path.exists(file))
    #plot_s_parameters(full_data_file_list)
    s_measured = s_matrix_at_freq(full_data_file_list[0], 447e6)
    s_simulation = s_matrix_at_freq(full_data_file_list[1], 447e6)
    rmse_mag, rmse_angle = rms_error_at_freq(s_measured, s_simulation)
    print('RMS Error: Magnitude: ', rmse_mag,', Angle (deg): ', rmse_angle)

    
    #plot the results
    vmin = -30
    vmax = 0
    fig, ax = plt.subplots(1,2)
    plt.sca(ax[0])
    plt.imshow(20*np.log10(np.abs(s_simulation)), cmap='jet', vmin=vmin, vmax=vmax)
    plt.title('|S| Simulation (dB)')
    
    plt.sca(ax[1])
    im = plt.imshow(20*np.log10(np.abs(s_measured)), cmap='jet', vmin=vmin, vmax=vmax)
    plt.title('|S| Measurement (dB)')
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    plt.colorbar(im, cax=cbar_ax)
    #fig.suptitle("RMS Error: " + "{:.4f}".format(rmse_mag))

    fig2, ax2 = plt.subplots(1,2)
    plt.sca(ax2[0])
    plt.imshow(180.0/np.pi*np.angle(s_simulation), cmap='jet')
    plt.title('Phase Simulation (deg)')
    plt.sca(ax2[1])
    im2 = plt.imshow(180.0/np.pi*np.angle(s_measured), cmap='jet')
    plt.title('Phase Measurement (deg)')
    fig2.subplots_adjust(right=0.8)
    cbar_ax2 = fig2.add_axes([0.85, 0.15, 0.05, 0.7])
    plt.colorbar(im2, cax=cbar_ax2)

    
    plt.show()