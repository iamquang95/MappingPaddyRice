import gdal

import numpy as np
import matplotlib.pyplot as plt

# Print all layer of a hdf file to choose what layer you want to extract
def printAllSubData(filename):
    dataset = gdal.Open(filename)
    print(dataset.GetSubDatasets())

# Extract a layer form image
def getArrayLayer(filename, layer):
    layerPath = 'HDF4_EOS:EOS_GRID:"%s":%s' % (filename, layer)
    lc_data = gdal.Open(layerPath, gdal.GA_ReadOnly)
    lc = lc_data.ReadAsArray()
    return lc

# Using matplotlib to show data
def showImage(data):
    plt.imshow ( data, interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth)
    plt.colorbar()
    plt.show()

# calculate arg1/arg2, if arg2 == 0, return 0
def devideIgnoreZero(arg1, arg2):
    with np.errstate(divide='ignore', invalid='ignore'):
        res = np.true_divide(arg1, arg2)
        res[res == np.inf] = 0
        res = np.nan_to_num(res)
    return res

def getLayerAsFloatArray(filename, layerStr):
    return np.array(getArrayLayer(filename, layerStr)).astype(float)

# This function can only extract layer from 500m MODIS 8 dayus
def getAllLayers(filename):
    redLayerStr = "MOD_Grid_500m_Surface_Reflectance:sur_refl_b01"
    nirLayerStr = "MOD_Grid_500m_Surface_Reflectance:sur_refl_b02"
    blueLayerStr = "MOD_Grid_500m_Surface_Reflectance:sur_refl_b03"
    swirLayerStr = "MOD_Grid_500m_Surface_Reflectance:sur_refl_b06"

    redLayer = getLayerAsFloatArray(filename, redLayerStr)
    nirLayer = getLayerAsFloatArray(filename, nirLayerStr)
    blueLayer = getLayerAsFloatArray(filename, blueLayerStr)
    swirLayer = getLayerAsFloatArray(filename, swirLayerStr)

    ndviLayer = devideIgnoreZero((nirLayer - redLayer), (nirLayer + redLayer))
    eviLayer = devideIgnoreZero((2.5*(nirLayer-redLayer)), (nirLayer + 6*redLayer - 7.5*blueLayer + 1))
    lswiLayer = devideIgnoreZero((nirLayer - swirLayer), (nirLayer + swirLayer))

    return {
        "redLayer": redLayer,
        "nirlayer": nirLayer,
        "blueLayer": blueLayer,
        "swirLayer": swirLayer,
        "ndviLayer": ndviLayer,
        "eviLayer": eviLayer,
        "lswiLayer": lswiLayer
    }

# Test with one image

filename = "HdfFiles/MOD09A1.A2015017.h27v06.005.2015028030040.hdf"
x = getAllLayers(filename)
print(x["ndviLayer"])
showImage(x["ndviLayer"])

