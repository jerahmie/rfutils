#!/usr/bin/env python
"""load mask for s-parameter plotting
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from gui_helpers import openfilegui


def extract_mask(maskfile):
    """Read mask text file and generate the mask.
    Args:
        maskfile: Filename of TSV s
    Returns:
        ndarray: N-by-N mask file of ones and zeros for multiplication with 
                 N-by-N data array. 
    Raises: 
        FileNotFoundError: If file is not found
    """
    
    with open(maskfile,'r') as file:
        lines = file.readlines()

    masklist = []
    for line in lines:
        if not line.startswith("#"):
            masklist.append(line.split("#")[0].split())
    
    return np.array(masklist, dtype='double')


def plot_gridmask(gridmask):
    """plot the grid mask
    gridmask: n-by-n mask
    """
    return plt.imshow(gridmask)
    

if __name__ == "__main__":
    try:
        spmask
    except NameError:
        spmaskfile = openfilegui(title="Select S-Parameter Mask",
                             filetypes=(("Tab Separated Values","*.tsv"),("all files","*.*")))

        spmask = extract_mask(spmaskfile)
        ax = plot_gridmask(spmask)
        plt.show()