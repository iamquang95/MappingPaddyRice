import os
from osgeo import gdal
import numpy

# Return a ndarray for every pixel in the GeoTIFF image
# e.g.: extractBand('some_dir', 'Blue_2005_DBSH.tif')
# Return format: a[i][x][y]: band i, position (x, y)
def extractBand(dir, filename):
	file = os.path.join(dir, filename)	
	dataset = gdal.Open(file, gdal.GA_ReadOnly)
	nobands = dataset.RasterCount
	firstBand = dataset.GetRasterBand(1)
	firstArray = firstBand.ReadAsArray()
	result = numpy.empty((nobands, firstArray.shape[0], firstArray.shape[1]))
	for i in range(2, nobands + 1):		
		band = dataset.GetRasterBand(i)
		array = band.ReadAsArray()		
	 	for j in range(0, array.shape[0]):
	 		for k in range(0, array.shape[1]):
	 			result[i - 1][j][k] = array[j][k]
	return result

# temp = extractBand('F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images', 'NDVI_2015_DBSH.tif')