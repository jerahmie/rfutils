#!/usr/bin/env python
"""
plot s-parameters at f from my ad-hoc s-parameter format.

The s-parameter format is simple.  The format is
( m , n ): |Smn| (dstr,  hhB) , Smn Phase (deg) | Re(Smn), Im(Smn)
lines without this format are ignored

Regex
"""
import sys
import os
#import copy
import re
import numpy as np
import matplotlib.pyplot as plt
from gui_helpers import openfilegui, openfilequick
from load_mask import extract_mask

# useful global functions
spat = re.compile(r"^\( ([0-9]*) , ([0-9]*) \).+\|\s*(-?[0-9.]*)\s*,\s*(-?[0-9.]*)\s*$")
def mag2db(smag):
    """
    Helper function to convert a raw magnitude to dB
    """
    return 20*np.log10(smag)

def rad2deg(sangle):
    """
    Helper function to convert a randian angle to degrees
    """
    return 180.0/np.pi*sangle

def usage():
    """Print usage and exit.
    """
    print("")
    print("Usage: ")
    print("")
    sys.exit()

def s_param_from_file(filename: str) -> np.ndarray :
    """
    Read and parse the s-parameters file at single frequency
    Args:
        filename: the filename containing s-parameters at a given frequency
    Returns:
        nchannel by nchannel numpy array of complex parameter values
    Raises:
        FileNotFoundError
    """
    # pass 1: read data from file
    try:
        with open(filename, 'r') as fh:
            print("Reading data...")
            sdata = fh.readlines()
    except FileNotFoundError:
        print("File: (" , filename, ") could not be found.")

    # pass 2: filter with regular expression
    sdata = [s for s in sdata if spat.match(s)]
    # check that the number of sparameters is equal to nchannels squared
    nchannels = int(np.sqrt(len(sdata)))
    assert len(sdata) == (nchannels * nchannels)

    # pass 3: populate an ndarray with data
    sdata_mat = np.zeros((nchannels, nchannels), dtype=np.complex128)
    for s in sdata:
        m = spat.match(s)
        i = int(m.group(1))
        j = int(m.group(2))
        sre = float(m.group(3))
        sim = float(m.group(4))
        sdata_mat[i-1][j-1] = sre + 1.0j*sim

    return sdata_mat

def plot_s_params(smat: np.ndarray, title: str="",
                  window_title: str="s_parameter_data",
                  data_overlay: bool=True,
                  show_colorbar=True) -> plt.axes:
    """
    Args:
        smat
        data_overlay
        show_colorbar
    Returns:
        matplotlib.pyplot.axes
    Raises:
    """
    fig, axs = plt.subplots(1,2, figsize=(15,6))
    (nx, ny) = np.shape(smat)
    im_abs = axs[0].imshow(mag2db(np.abs(smat)), cmap='jet')
    plt.sca(axs[0])
    plt.title('|S| (dB)')
    plt.xticks(range(nx), [str(x+1) for x in range(nx)])
    plt.yticks(range(ny), [str(y+1) for y in range(ny)])
    if data_overlay:
        for i in range(nx):
            for j in range(ny):
                dbij = mag2db(np.abs(smat[i][j]))
                axs[0].text(i, j, f'{dbij:.0f}',
                            horizontalalignment='center',
                            verticalalignment='center')
    if show_colorbar:
        fig.subplots_adjust(right=0.8)
        box0 = axs[0].get_position()
        axs[0].set_position(box0)
        plt.colorbar(im_abs, cax=fig.add_axes([box0.x1+0.01, box0.y0, 0.01, box0.y1-box0.y0]))

    im_phase = axs[1].imshow(rad2deg(np.angle(smat)), cmap='hsv')
    plt.sca(axs[1])
    plt.title("Phase (deg)")
    plt.xticks(range(nx), [str(x+1) for x in range(nx)])
    plt.yticks(range(ny), [str(y+1) for y in range(ny)])
    if data_overlay:
        for i in range(nx):
            for j in range(ny):
                angleij = rad2deg(np.angle(smat[i][j]))
                axs[1].text(i, j, f'{angleij:.0f}',
                            horizontalalignment='center',
                            verticalalignment='center')
    if show_colorbar:
        box1 = axs[1].get_position()
        box1.x0 += 0.05
        box1.x1 += 0.05
        axs[1].set_position(box1)
        plt.colorbar(im_phase, cax=fig.add_axes([box1.x1+0.01, box0.y0,0.01, box1.y1-box0.y0]))
    fig.suptitle(title)
    fig.canvas.set_window_title(window_title)
    return axs

if __name__ == "__main__":

    s_param_files = []
    s_param_files.append(os.path.join('/home','jerahmie','workspace',
                                 'rfutils','test_data','s_params_original.txt'))
    # use a dialog box for i nteractive file selection.

    # if data_files wasn't hand coded, use the file dialog.
    if not 's_param_files' in locals():
        s_param_files.append(openfilegui(title="Open Touchstone Files (Measured)",
                                  filetypes=(("S-Parameter File","*.txt"), ("all files","*.*"))))

    print(s_param_files)
    # Exit if no files were selected.
    if len(s_param_files) == 0 or s_param_files is None:
        sys.exit("No files to process.  Exiting.")

    #plot the results
    sp = s_param_from_file(s_param_files[0])
    ax0 = plot_s_params(sp, title="S Parameters (Original)",
                        window_title=s_param_files[0],
                        data_overlay=True,
                        show_colorbar=True)
    plt.show()
