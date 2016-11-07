import os

from ExtractData import getAllLayers

def getFileExtension(filename):
	(_name, _extension) = os.path.splitext(filename)
	return _extension

def getAllHdfFilesPath(folderPath):
	allFiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	allHdfFiles = [f for f in allFiles if getFileExtension(f) == ".hdf"]
	fullPathHdfFiles = ['/%s/%s' % (folderPath, f) for f in allHdfFiles]

	return fullPathHdfFiles

# Test

folderPath = "HdfFiles"
print(getAllHdfFilesPath(folderPath))
print(getAllLayers(getAllHdfFilesPath(folderPath)[0]["redLayer"]))
