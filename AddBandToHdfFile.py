import h5py
import numpy as np

import ExtractData
import DataMap

filename = "HdfFiles/quang.h5" 

f = h5py.File(filename,'r+')
allLayers = ExtractData.getAllLayers("HdfFiles/MOD09A1.A2015017.h27v06.005.2015028030040.hdf")
layer  = f.create_dataset("test/ndviLayer", data=allLayers["ndviLayer"])

f.close()

def saveBandsToHdfFile(filename):
    hdf4Filename = DataMap.getFileName(filename) + ".hdf"
    h5Filename = DataMap.getFileName(filename) + ".h5"

    f = h5py.File(h5Filename, 'r+')
    allLayers = ExtractData.getAllLayers(hdf4Filename)

    for (layer, _data) in allLayers.iteritems():
        f.create_dataset("fimo/"+layer, data=_data)

    f.close()



