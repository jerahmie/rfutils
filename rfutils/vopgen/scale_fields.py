#!/usr/bin/env python
"""
Scale the vopgen format fields by a constant.
"""
import os
import numpy as np
import hdf5storage


def scale_fields(scale: np.ndarray, vopfield3d: np.ndarray) -> dict:
    """
    Args:
    scale:      ndarray     1XN array of scales per channel
    vopfield3d: dict        Dict of Vopgen 3D format field data

    Returns:
    dict                    Result dict of scaled fields.
    """
    print("Scaling vopgen fields...")
    nchannels = np.shape(vopfield3d)[-1]
    new_vopfield3d = np.zeros(np.size(vopfield3d))
    
    for ch in range(nchannels):
        new_vopfield3d[...,ch] = vopfield3d[...,ch]*scale(ch)

    sf = {}
    # pass through dimensions
    sf["XDim"] = vopfield3d["XDim"]
    sf["YDim"] = vopfield3d["YDim"]
    sf["ZDim"] = vopfield3d["ZDim"]

    if "efMapArrayN" in vopfield3d.keys():
        field_key = "efMapArrayN"
    elif "bfMapArrayN" in vopfield3d.keys():
        field_key = "bfMapArrayN"
    else:
        raise KeyError("Valid key not found.")
    sf[field_key] = new_vopfield3d
    
    return sf 


def save_fields(vopfile_name: str, vopfield_dict: dict) -> None:
    """ Save fields to matlab file.
    Args:
    vopfile_name: str 

    """
    hdf5storage.savemat(vopfile_name, vopfield_dict, oned_as='column')

if __name__  == "__main__":
    print("Scaling vopgen fields...")
    export_dir = os.path.join("/export","scratch1",
                              "Self_Decoupled_16tx_64Rx_Duke_Fields_CST2020_3_1",
                              "Export")
    ef_dir = os.path.join(export_dir, "efMapArrayN_no_scale.mat")
    ef_dict = hdf5storage.loadmat(ef_dir)
    scale = (1.0/np.sqrt(50.))*np.ones(np.shape(ef_dict["efMapArrayN"][-1]))
    scaled_field_dict = scale_fields(scale, ef_dict)
    save_fields("efMapArrayN.mat", scaled_field_dict)