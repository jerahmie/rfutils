#!/usr/bin/env python
"""Plot list of touchstone files.
"""

import sys
import os
import copy
import numpy as np
import skrf as rf
import matplotlib.pyplot as plt
from gui_helpers import openfilegui, openfilequick
from load_mask import extract_mask

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
    #plt.vlines(470e6,-40,0,linestyle='dashed', label='470 MHz')
    plt.vlines(447e6,-40,0,linestyle='dashed', label='447 MHz')
    plot.colorbar()
    plt.show()

def s_matrix_at_freq(smatrix1_file, freq=447e6):
    """Return the smatrix at the frequency of interest.
    
        Args:

        Returns: NxN numpy matrix.
    """
    #freq1 = rf.Frequency(freq, freq, 1, 'Hz')
    print(smatrix1_file)
    smat = rf.Network(smatrix1_file)
    m,n = np.shape(smat.s)[1], np.shape(smat.s)[2]
    if m != n:
        print("S-matrix is malformed.")
        return None
    s_at_freq = np.zeros((m,n), dtype=complex)
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


if __name__ == "__main__":

    # use a dialog box for i nteractive file selection.

    # if data_files wasn't hand coded, use the file dialog.
    try:
        data_files  # check if data_file has been defined
    except NameError:
        data_files = []
        data_files.append(openfilegui(title="Open Touchstone Files (Measured)",
                                  filetypes=(("Touchstone Files","*.s*p"), ("all files","*.*"))))
        data_files.append(openfilegui(title="Open Touchstone Files (Simulation)",
                                  filetypes=(("Touchstone Files","*.s*p"), ("all files","*.*"))))
    # Exit if no files were selected.
    if data_files == '' or data_files == None:
        sys.exit("No files to process.  Exiting.")

    s_measured = s_matrix_at_freq(data_files[0], 447e6)
    s_simulation = s_matrix_at_freq(data_files[1], 447e6)
    rmse_mag, rmse_angle = rms_error_at_freq(s_measured, s_simulation)
    print('RMS Error: Magnitude: ', rmse_mag,', Angle (deg): ', rmse_angle)

    try:
        spmaskfile
    except NameError:
        spmaskfile = openfilegui(title="Select S-Parameter Mask",
                                filetypes=(("Tab Separated Values","*.tsv"),
                                ("all files", "*.*")))
        if os.path.exists(spmaskfile):
            spmask = extract_mask(spmaskfile)
            if np.shape(spmask) != np.shape(s_measured):
                print("Shape of Mask {} != Shape of S-Parameter array {}".format(np.shape(spmask), np.shape(np.shape(s_measured))))            
        else:
            spmask = np.ones(np.shape(s_measured))
    
    #plot the results
    vmin = -30
    vmax = -0.1
    cmap1 = copy.copy(plt.cm.jet)
    fig, ax = plt.subplots(1,2)
    plt.sca(ax[0])
    im1 = plt.imshow(np.multiply(spmask, 20*np.log10(np.abs(s_simulation))), cmap=cmap1, vmin=vmin, vmax=vmax)
    im1.cmap.set_over('navy')
    plt.title('|S| Simulation (dB)')
    
    plt.sca(ax[1])
    im = plt.imshow(np.multiply(spmask, 20*np.log10(np.abs(s_measured))), cmap=cmap1, vmin=vmin, vmax=vmax)
    im.cmap.set_over('navy')
    plt.title('|S| Measurement (dB)')
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    plt.colorbar(im, cax=cbar_ax)
    #fig.suptitle("RMS Error: " + "{:.4f}".format(rmse_mag))

    fig2, ax2 = plt.subplots(1,2)
    plt.sca(ax2[0])
    plt.imshow(np.multiply(spmask, np.angle(s_simulation)), cmap='jet')
    plt.title('Phase Simulation (deg)')
    plt.sca(ax2[1])
    im2 = plt.imshow(np.multiply(spmask, np.angle(s_measured)), cmap='hsv')
    plt.title('Phase Measurement (deg)')
    fig2.subplots_adjust(right=0.8)
    cbar_ax2 = fig2.add_axes([0.85, 0.15, 0.05, 0.7])
    plt.colorbar(im2, cax=cbar_ax2)

    # Just plot s-parameters
    #plt.imshow(20*np.log10(np.abs(s_simulation)), cmap='jet', vmin=vmin, vmax=vmax)
    #plt.title('|S| Simulation (dB)')
    #plt.show()
    #plt.imshow(20*np.log10(np.abs(s_simulation)), cmap='jet', vmin=-40, vmax=0)
    plt.show()
