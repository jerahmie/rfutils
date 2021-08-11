#!/usr/bin/env python
"""Print routines for scattering matrices from scikit-rf networks.
"""
import os
import sys

import numpy as np
import skrf as rf


def pretty_print_s_parameters(ntwk, f0=447e6):
    """Pretty print the scattering matrix at frequency.
    """
    nn = np.shape(ntwk.s)[1]
    freq = ntwk.f
    f0_ind = np.argmin(np.abs(freq-f0))
    pretty_str = "freq: " + str(freq[f0_ind]) + "\n"
    pretty_str += "   -   |    " + "     |     ".join([str(i+1) for i in range(nn)]) + "     |\n"
    for i in range(nn):
        for j in range(nn):
            #pretty_str +=   "      " + "    |   ".join(str(np.abs(ntwk.s[f0_ind, i, j]))) + "\n"
            print('(', i+1, ',', j+1 ,'): ','{:6.2f} '.format(20*np.log10(np.abs(ntwk.s[f0_ind,i,j]))),
            ', {:7.2f}'.format(180.0/np.pi*np.angle(ntwk.s[f0_ind,i,j])))
    #print(pretty_str)


if __name__ == "__main__":
    #ts_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
    #                          '..', '..', 'test_data',
    #                          '8CH_ELdipole_commongnd-23cmCONE_notraps_cloneELDipole_6-30-2020.s8p')) 
    ts_file = os.path.join('D:\\', 'Temp_CST',
                           '8CH-ELD_KU32insert_Lightbulb_RXtrap-tuned_09-28-20.s8p')              
    print("pretty print s-parameters.")
    ntwk = rf.Network(ts_file)
    pretty_print_s_parameters(ntwk)
