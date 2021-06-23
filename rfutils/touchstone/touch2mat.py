"""Read Touchstone file and convert to mat file.
"""
import os
import numpy as np
import skrf as rf
import hdf5storage
import matplotlib.pyplot as plt

def touch2mat(touchstone_file, matlab_file):
    """Read touchstone file and convert to mat file.
    """
    ntwk = rf.Network(touchstone_file)
    export_dict = dict()
    export_dict['s'] = ntwk.s
    export_dict['frequency'] = ntwk.f
    hdf5storage.savemat(matlab_file, export_dict)

def plot_smat(mat_file):
    """plot the mat file.
    """
    import_dict = hdf5storage.loadmat(mat_file)
    f = import_dict['frequency']
    s = import_dict['s']
    (nsamples, ns, ms) = np.shape(s)
    # plot the on-diagonal s-parameters (s11, s22, ... snn)
    for i in range(ns):
        plt.plot(f, 10*np.log10(np.abs(s[:,i,i])))  # not sure if db power or voltage 
    plt.show()

if __name__ == "__main__":
    ts_file = os.path.join("D:\\","workspace","ipython_notebooks",
                           "S-Parameter Evaluation", 
                           "KU-10_TX-2x8_TXonly_lightbulbC_2-19-2020.s16p")
    mat_file = "KU-10_TX-2x8_TXonly_lightbulbC_2-19-2020.mat"

    #ts_file = os.path.join("C:\\", "Users","Jerahmie","Downloads","KU_ten_32_Tx_MRT_23Jul2019.s96p")
    #mat_file = "KU_ten_32_Tx_MRT_23Jul2019.mat"
    touch2mat(ts_file, mat_file)
    plot_smat(mat_file)
