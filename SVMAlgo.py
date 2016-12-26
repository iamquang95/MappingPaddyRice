import numpy as np
import ImageHelper as im_helper
from PaddyRiceClassifier import PaddyRiceClassifier
import Output
import Config

dataFolderDir = Config.dataFolderDir

classifier = PaddyRiceClassifier()


def runAlgoForYear(year):
    data_map = im_helper.extractBandForYear(dataFolderDir, year)
    m, n, k = data_map.shape
    print m, n, k
    result = np.zeros((m, n), dtype=np.int)
    for x in range(m):
        for y in range(n):
            noData = False
            for z in range(k):
                if data_map[x, y, z] < -9000:
                    noData = True
                    break
            if noData:
                result[x, y] = -1
                continue                    
            data_point = data_map[x][y].reshape(1, -1)
            result[x, y] = classifier.predict(data_point)
    Output.createTiff(result, 'SVM', str(year))
    return result

if __name__ == '__main__':
    runAlgoForYear(2015)