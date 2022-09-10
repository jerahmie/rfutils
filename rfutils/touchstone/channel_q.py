#!/usr/bin/env python
import os
import sys

import numpy as np
import skrf as rf
import matplotlib.pyplot as plt

def channel_q(ntwk: rf.network.Network, i: int) -> (float, float):
    """Get the -1 dB point, -7 dB point, and center frequencies
    """
    sb1 = -1
    sb2 = -7
    sii = 10.0*np.log10(np.abs(ntwk.s[:,i,i]))
    i0 = np.argmin(sii)
    sii = sii[:i0]
    f = ntwk.f[:i0]
    i0 = np.argmin(sii)
    i1 = np.argmin(np.abs(sii-sb1))
    i2 = np.argmin(np.abs(sii-sb2))
    return (f[i2] - f[i1], f[i0])

if __name__ == "__main__":
    ts_file = sys.argv[1]
    if not os.path.exists(ts_file):
        sys.exit("could not find file")
    ntwk = rf.Network(ts_file)
    for i in range(8):
        f = channel_q(ntwk, i)
        print(f[1]/f[0])