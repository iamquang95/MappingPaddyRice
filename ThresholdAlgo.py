import GenerateHdf
import os
import gdal
import numpy as np
import Evaluation
import Output
import Config
import Util

############### config ##############
dataFolderDir = Config.dataFolderDir
fileName = "%s_%d_DBSH.tif"

############### processing ##########

def getDataForYear(bandName, year):
    result = []
    filename = os.path.join(dataFolderDir, fileName % (bandName, year))        
    for layer in xrange(1, 47):
        print layer
        # if not (bandName == 'BLUE'):                    
        #     result.append(Util.normalize(GenerateHdf.getData(filename, layer), bandName))
        # else:
        #     result.append(GenerateHdf.getData(filename, layer))
        result.append(GenerateHdf.getData(filename, layer))
    return result

def thresholdAlgo(ndvi, evi, lswi, blue):
    (n, m) = ndvi[0].shape
    res = np.zeros((n, m), dtype=np.int)
    nLayers = 46

    rejectPixels = np.zeros((n, m))

    # NDVI < LSWI
    cnt1 = np.zeros((n, m))
    # NDVI >= 0.7
    cnt2 = np.zeros((n, m))
    # LSWI >= 0.1
    cnt3 = np.zeros((n, m))

    for x in xrange(0, n):
        for y in xrange(0, m):
            for layer in xrange(0, nLayers):
                # print("%d %d %d" % (layer, x, y))
                if (ndvi[layer][x][y] < lswi[layer][x][y]):
                    cnt1[x][y] += 1
                if (ndvi[layer][x][y] >= 0.7):
                    cnt2[x][y] += 1
                if (lswi[layer][x][y] >= 0.1):
                    cnt3[x][y] += 1

    for layer in xrange(0, nLayers):
        for x in xrange(0, n):
            for y in xrange(0, m):
                # HACK for background 
                if ndvi[layer][x][y] < -9000:
                    res[x][y] = -1
                    continue
                _blue = blue[layer][x][y]*1.0 / 10000
                _ndvi = ndvi[layer][x][y]
                _lswi = lswi[layer][x][y]
                _evi = evi[layer][x][y]

                # Pixel cloud
                if (_blue >= 0.2):
                    continue
                # Water body
                if (_ndvi < 0.1) and (cnt1[x][y] >= 10):
                    continue
                # Green forest
                if (cnt2[x][y] >= 20) and (cnt3[x][y] == nLayers - 1):
                    continue
                # Other land cover
                if not((_lswi + 0.05 >= _evi) or (_lswi + 0.05 >= _ndvi)):
                    continue
                # From now, this pixel is rood areas or sowing paddy field
                eviMax = -1
                for image in xrange(layer, min(layer+8, nLayers)):
                    eviMax = max(eviMax, evi[image][x][y])
                flag = True
                for image in xrange(layer, min(layer+5, nLayers)):
                    if (evi[image][x][y] < eviMax*1.0/2) and (blue[image][x][y] < 0.2):
                        flag = False
                if (flag):
                    res[x][y] = 1
    return res

def createRiceMap(year):
    ndvi = getDataForYear("NDVI", year)
    evi = getDataForYear("EVI", year)
    lswi = getDataForYear("LSWI", year)
    blue = getDataForYear("BLUE", year)

    riceMap = thresholdAlgo(ndvi, evi, lswi, blue)
    
    # vi = gdal.Open(os.path.join(dataFolderDir, "EVI_2005_DBSH.tif")) # HACK
    # geoT = vi.GetGeoTransform()
    # proj = vi.GetProjection()
    Output.createTiff(riceMap, 'Threshold', str(year))    

    print Evaluation.evaluate(riceMap, year)


if __name__ == '__main__':
    # ndvi = getDataForYear("NDVI", 2005)

    createRiceMap(2015)    
    # ndvi = GenerateHdf.getData(os.path.join(dataFolderDir, 'NDVI_2005_DBSH.tif'), 1)
    # print ndvi.shape
    pass
