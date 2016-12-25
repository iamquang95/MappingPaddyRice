import numpy 

def getMinValue(band):
	shape = band.shape
	minVal = 10000
	xx = 0
	yy = 0
	if len(shape) == 2:
		for x in range(shape[0]):
			for y in range(shape[1]):
				if band[x][y] > -9000:
					if band[x][y] < minVal:
						minVal = min(minVal, band[x][y])
						xx = x
						yy = y
	else:
		if len(shape) == 3:
			for x in range(shape[0]):
				for y in range(shape[1]):
					for z in range(shape[2]):
						if band[x][y][z] > -9000:
							minVal = min(minVal, band[x][y][z])
		else:
			raise Exception('Dimension not supported')
	return (minVal, xx, yy)

def getMaxValue(band):
	shape = band.shape
	maxVal = -10000
	if len(shape) == 2:
		for x in range(shape[0]):
			for y in range(shape[1]):
				if band[x][y] > -9000:
					maxVal = max(maxVal, band[x][y])
	else:
		if len(shape) == 3:
			for x in range(shape[0]):
				for y in range(shape[1]):
					for z in range(shape[2]):
						if band[x][y][z] > -9000:
							maxVal = max(maxVal, band[x][y][z])
		else:
			raise Exception('Dimension not supported')
	return maxVal

def getOutOfRange(band):
	shape = band.shape
	count = 0
	if len(shape) == 2:
		for x in range(shape[0]):
			for y in range(shape[1]):
				if band[x][y] < -1 or band[x][y] > 1:
					count = count + 1
	return (shape[0] * shape[1], count)

def outOfRange(value, t):	
	if t == 'NDVI':
		return (value > -9990 and value < 1.0) or value > 1.0
	if t == 'EVI':
		return (value > -9990 and value < 0.0) or value > 1.0
	if t == 'LSWI':
		return (value > -9990 and value < 1.0) or value > 1.0
	return false

def normalize(band, type):
	shape = band.shape
	result = numpy.zeros_like(band)			
	if len(shape) == 2:		
		for x in range(shape[0]):
			for y in range(shape[1]):					
				if outOfRange(band[x, y], type):
					result[x, y] = 0
				else:
					result[x, y] = band[x, y]
	if len(shape) == 3:
		for x in range(shape[0]):
			for y in range(shape[1]):
				for z in range(shape[2]):
					if outOfRange(band[x, y, z], type):
						result[x, y, z] = 0
					else:
						result[x, y, z] = band[x, y, z]
	return result
	