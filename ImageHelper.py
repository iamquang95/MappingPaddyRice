import os
from osgeo import gdal
import numpy

def makeFileName(prefix, suffix, ext = "tif"):
    """
    Generate a new file name by appending a suffix and changing the extension of an input file name 
    :param prefix: string, input file name
    :param suffix: string, suffix to be placed just before file extension (e.g., 'NDVI')
    :param ext: string, extension. Don't put the period before the extension
    """    
    return prefix + '_' + suffix + '.' + ext

# Return a ndarray for every pixel in the GeoTIFF image
# e.g.: extractBand('some_dir', 'Blue_2005_DBSH.tif')
# Return format: a[i][x][y]: band i, position (x, y)
def extractBand(dir, filename):
	file = os.path.join(dir, filename)	
	dataset = gdal.Open(file, gdal.GA_ReadOnly)
	nobands = dataset.RasterCount
	firstBand = dataset.GetRasterBand(1)
	firstArray = firstBand.ReadAsArray()
	result = numpy.empty((firstArray.shape[0], firstArray.shape[1], nobands))
	for j in range(0, firstArray.shape[0]):
		for k in range(0, firstArray.shape[1]):
			result[j][k][0] = firstArray[j][k]

	for i in range(2, nobands + 1):		
		band = dataset.GetRasterBand(i)
		array = band.ReadAsArray()		
	 	for j in range(0, array.shape[0]):
	 		for k in range(0, array.shape[1]):
	 			result[j][k][i - 1] = array[j][k]
	return result

def extractBandForYear(dir, _year):
	year = ''
	if not isinstance(_year, basestring):
		year = str(_year)
	else:
		year = str(_year)
	ndvi = extractBand(dir, makeFileName('NDVI', year + '_DBSH', 'tif'))
	evi = extractBand(dir, makeFileName('EVI', year + '_DBSH', 'tif'))
	lswi = extractBand(dir, makeFileName('LSWI', year + '_DBSH', 'tif'))	
	result = numpy.empty((ndvi.shape[0], ndvi.shape[1], ndvi.shape[2] + evi.shape[2] + lswi.shape[2]))
	for i in range(0, result.shape[0]):
		for j in range(0, result.shape[1]):
			for k in range(0, ndvi.shape[2]):
				result[i][j][k] = ndvi[i][j][k]
			for k in range(0, evi.shape[2]):
				result[i][j][ndvi.shape[2] + k] = evi[i][j][k]
			for k in range(0, lswi.shape[2]):
				result[i][j][ndvi.shape[2] + evi.shape[2] + k] = lswi[i][j][k]	
	return result

# temp = extractBand('F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images', 'NDVI_2015_DBSH.tif')
temp = extractBandForYear('F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images', 2005)