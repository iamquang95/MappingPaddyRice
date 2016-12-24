import os
import numpy
from osgeo import gdal

dataFolderDir = 'F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images'

def makeFileName(prefix, suffix, ext = "tif"):    
    return prefix + '_' + suffix + '.' + ext

def createTiff(band, prefix, suffix):		
	width = band.shape[1]
	height = band.shape[0]
	r_band = numpy.zeros((height, width), dtype=numpy.int)
	g_band = numpy.zeros((height, width), dtype=numpy.int)
	b_band = numpy.zeros((height, width), dtype=numpy.int)
	for x in range(0, height):
		for y in range(0, width):
			if band[x][y] == 0:
				r_band[x][y] = 196
				g_band[x][y] = 118
				b_band[x][y] = 8
			if band[x][y] == 1:
				# print x + ' ' + y 
				r_band[x][y] = 122
				g_band[x][y] = 214
				b_band[x][y] = 9
			if band[x][y] == -1:
				print str(x) + ' ' + str(y)

	driver = gdal.GetDriverByName('GTiff')
	outfile_name = makeFileName(prefix, suffix, 'tif')
	dataset = driver.Create(outfile_name, width, height, 3, gdal.GDT_Byte)
	vi = gdal.Open(os.path.join(dataFolderDir, "EVI_2005_DBSH.tif")) # HACK
	geoT = vi.GetGeoTransform()
	proj = vi.GetProjection()
	dataset.SetGeoTransform(geoT)
	dataset.SetProjection(proj)    
	dataset.GetRasterBand(1).WriteArray(r_band)
	dataset.GetRasterBand(2).WriteArray(g_band)
	dataset.GetRasterBand(3).WriteArray(b_band)