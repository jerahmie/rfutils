"""Reorder vopgen fields from channel map file.
A channel map file has a header with zero or more lines of comments.

Mapping file format:
# Comment
original_channel_1 remapped_channel_1
...
original_channel_n remapped_channel_n

ex:
# Remap 4 tx 
1 4
2 3
3 2
4 1

"""
import os
import sys
import csv
import hdf5storage
import numpy as np

def reorder_vopgen_channels(remap_file, field_file_old, field_file_new):
    """Reorder the field channels according to provided mapping file.
    """
    print('Reordering channels...')
    # read remap file and ignore comments
    with open(remap_file, 'r') as csv_file:
        rdr = csv.reader(filter(lambda row: row[0]!='#', csv_file), delimiter=' ', quotechar='|')
        coil_map = list(rdr)

    # read the original field 
    print("Reading field maps...")
    fields_old_dict = hdf5storage.loadmat(field_file_old)
    
    field_keys = fields_old_dict.keys()
    if 'efMapArrayN' in field_keys:
        field_key = 'efMapArrayN'
        print('Found efMapArrayN.  Converting E-fields...')
    else:
        field_key = 'bfMapArrayN'
        print('Found bfMapArrayN.  Converting B-fields...')

    fmap_arrayn_old = fields_old_dict[field_key]
    nchannels =  np.shape(fmap_arrayn_old)[4]
    
    # create new remap fields
    print("Remapping and saving fields...")
    fmap_arrayn_new = np.zeros(np.shape(fmap_arrayn_old), dtype=np.complex)
    for channel in range(nchannels):
        print(coil_map[channel][0], ' -> ', coil_map[channel][1])
        fmap_arrayn_new[:,:,:,:,int(coil_map[channel][1])-1] = fmap_arrayn_old[:,:,:,:,int(coil_map[channel][0])-1 ]

    fields_new_dict = dict()
    fields_new_dict['XDim'] = fields_old_dict['XDim']
    fields_new_dict['YDim'] = fields_old_dict['YDim']
    fields_new_dict['ZDim'] = fields_old_dict['ZDim']
    fields_new_dict[field_key] = fmap_arrayn_new
    
    # write remapped fields
    print("Writing remapped_fields")
    hdf5storage.savemat(field_file_new, fields_new_dict, oned_as='column')

if "__main__" == __name__:
    if 'win32' == sys.platform:
        vopgen_prefix=os.path.join('E:',os.sep,'CST_Field_Post', 'KU_Ten_32_16CH_Tx','KU_ten_32_Tx_MRT_23Jul2019','Export','Vopgen')
        print("[DEBUG] Platform = win32")
        print("[DEBUG] vopgen_prefix: ", vopgen_prefix)

    #elif 'linux' == sys.platform:
        #vopgen_prefix = os.path.join('/mnt','e','CST_Field_Post','KU_ten_32_Tx_MRT_23Jul2019', 'Vopgen')
    orig_prefix = os.path.join(vopgen_prefix, 'orig') 
    efield_file_orig = os.path.join(orig_prefix, 'efMapArrayN.mat')
    efield_file_remap = os.path.join(vopgen_prefix, 'efMapArrayN.mat')
    bfield_file_orig = os.path.join(orig_prefix, 'bfMapArrayN.mat')
    bfield_file_remap = os.path.join(vopgen_prefix, 'bfMapArrayN.mat')
    channel_remap_file = os.path.join(vopgen_prefix,
                                      'KU_ten_32_channel_renumbering_9Jan2019.txt')          
    
    reorder_vopgen_channels(channel_remap_file, efield_file_orig, efield_file_remap)
    reorder_vopgen_channels(channel_remap_file, bfield_file_orig, bfield_file_remap)
