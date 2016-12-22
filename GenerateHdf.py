from osgeo import gdal
import ExtractData
import os
import numpy
from PIL import Image
import matplotlib.pyplot as plt

def makeFileName(x, suffix, ext = "tif"):
    """
    Generate a new file name by appending a suffix and changing the extension of an input file name 
    :param x: string, input file name
    :param suffix: string, suffix to be placed just before file extension (e.g., 'NDVI')
    :param ext: string, extension. Don't put the period before the extension
    """
    # base = os.path.splitext(os.path.basename(x))[0]
    return x + '_' + suffix + '.' + ext

def getData(filename, band):
	dataset = gdal.Open(filename, gdal.GA_ReadOnly)
	band = dataset.GetRasterBand(band)
	array = band.ReadAsArray()
	return array

def createTiff(band, prefix, suffix, geoT, proj):	
	width = band.shape[1]
	height = band.shape[0]
	driver = gdal.GetDriverByName('GTiff')
	outfile_name = makeFileName(prefix, suffix, 'tif')
	dataset = driver.Create(outfile_name, width, height, 1, gdal.GDT_Float64)
	dataset.SetGeoTransform(geoT)
	dataset.SetProjection(proj)    
	dataset.GetRasterBand(1).WriteArray(band)

def showImage(data):
    plt.imshow ( data, interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth)
    plt.colorbar()
    plt.show()

def processFile(dir, filename):
	prefix = filename[0:(filename.rfind('sur_refl') - 1)]
	vi = gdal.Open(os.path.join(dir, filename))
	geoT = vi.GetGeoTransform()
	proj = vi.GetProjection()
	redTiff = os.path.join(dir, prefix + '.sur_refl_b01.tif')
	nirTiff = os.path.join(dir, prefix + '.sur_refl_b02.tif')
	blueTiff = os.path.join(dir, prefix + '.sur_refl_b03.tif')
	swirTiff = os.path.join(dir, prefix + '.sur_refl_b06.tif')
	redBand = getData(redTiff)	
	nirBand = getData(nirTiff)
	blueBand = getData(blueTiff)
	swirBand = getData(swirTiff)	
	ndviBand = ExtractData.divideIgnoreZero((nirBand - redBand), (nirBand + redBand))	
	eviBand = ExtractData.divideIgnoreZero((2.5*(nirBand - redBand)), (nirBand + 6 * redBand - 7.5 * blueBand + 1))
	lswiBand = ExtractData.divideIgnoreZero((nirBand - swirBand), (nirBand + swirBand))	
	createTiff(ndviBand, os.path.join(dir, prefix), 'NDVI', geoT, proj)
	createTiff(eviBand, os.path.join(dir, prefix), 'EVI', geoT, proj)
	createTiff(lswiBand, os.path.join(dir, prefix), 'LSWI', geoT, proj)

def processDir(dir):	
	files = os.listdir(dir)
	for file in files:
		if file.endswith('sur_refl_b01.tif'):
			print file
			processFile(dir, file)

# filename = "MOD09A1.A2015001.h27v06.006.2015295092734.sur_refl_b01.tif"
# processFile('./', filename)
# processDir('F:/DaiHoc/Images/2005/')
