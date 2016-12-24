import os
import numpy

folderDir = 'F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images'

def makeFileName(prefix, suffix, ext = "tif"):    
    return prefix + '_' + suffix + '.' + ext

def readPosLabelForYear(year):
	filename = os.path.join(folderDir, makeFileName('NDVI', 'Pos_' + str(year), 'txt'))
	array = numpy.loadtxt(filename, dtype=numpy.int, skiprows=8)
	coords = array[:, [2, 1]]	
	labels = numpy.ones((coords.shape[0], 1), dtype=numpy.int)
	result = numpy.concatenate((coords, labels), axis=1)
	return result

def readNegLabelForYear(year):
	filename = os.path.join(folderDir, makeFileName('NDVI', 'Neg_' + str(year), 'txt'))
	array = numpy.loadtxt(filename, dtype=numpy.int, skiprows=40)
	coords = array[:, [2, 1]]		
	labels = numpy.zeros((coords.shape[0], 1), dtype=numpy.int)
	result = numpy.concatenate((coords, labels), axis=1)	
	return result

def getLabelForYear(year):
    pos = readPosLabelForYear(year)    
    neg = readNegLabelForYear(year)    
    result = numpy.concatenate((pos, neg), axis=0)    
    # x = min([result[i][0] for i in range(0, result.shape[0])])
    # print x
    # y = min([result[i][1] for i in range(0, result.shape[0])])
    # print y
    return result

def evaluate(riceMap, year):
 	data = getLabelForYear(year)
 	total = data.shape[0]
 	correct = 0
	for i in range(0, data.shape[0]):
		if riceMap[data[i][0]][data[i][1]] == data[i][2]:
			correct = correct + 1
	return (correct * 1.0) / total

getLabelForYear(2015)