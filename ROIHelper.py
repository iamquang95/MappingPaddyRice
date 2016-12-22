import os
import numpy

def makeFileName(band, type, year):
	return band + '_' + type + '_' + str(year) + '.txt'

def readROI(filename, type):
	# Skip first 40 rows 
	if (type == 'Neg'):
		array = numpy.loadtxt(filename, skiprows=40)	
	# Skip first 8 rows
	else: 
		array = numpy.loadtxt(filename, skiprows=8)
	result = numpy.delete(array, numpy.s_[:5], axis=1)		
	return result

# Return a ndarray containing band values for a list of training data
# Example: readSample('some_dir', 'NDVI', 'Pos')
def readSample(dir, band, type, year):		
	if isinstance(year, basestring):
		filename = os.path.join(dir, makeFileName(band, type, year))
	else:
		filename = os.path.join(dir, makeFileName(band, type, str(year)))
	return readROI(filename, type)

# Return a ndarray containing band values (NDVI, EVI, LSWI) 
# for a list of training data and their corresponding label
# Order: 1 column label - 46 columns ndvi - 46 columns evi - 46 columns lswi
def readPosSample(dir, year):
	ndvi = readSample(dir, 'NDVI', 'Pos', year)	
	evi = readSample(dir, 'EVI', 'Pos', year)
	lswi = readSample(dir, 'LSWI', 'Pos', year)
	labels = numpy.ones((ndvi.shape[0], 1), dtype=numpy.int)	
	result = numpy.concatenate((labels, ndvi, evi, lswi), axis=1)			
	return result

# Return a ndarray containing band values (NDVI, EVI, LSWI) 
# for a list of training data and their corresponding label
# Order: 1 column label - 46 columns ndvi - 46 columns evi - 46 columns lswi
def readNegSample(dir, year):
	ndvi = readSample(dir, 'NDVI', 'Neg', year)
	evi = readSample(dir, 'EVI', 'Neg', year)
	lswi = readSample(dir, 'LSWI', 'Neg', year)
	labels = numpy.zeros((ndvi.shape[0], 1), dtype=numpy.int)
	result = numpy.concatenate((labels, ndvi, evi, lswi), axis=1)
	return result

# temp = readNegSample('F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images/', 2005)