import numpy as np
import ImageHelper as im_helper
from PaddyRiceClassifier import PaddyRiceClassifier

dataFolderDir = "PaddyRice TIFF"

classifier = PaddyRiceClassifier()


def runAlgoForYear(year):
    data_map = im_helper.extractBandForYear(dataFolderDir, year)
    m, n, k = data_map.shape
    print m, n, k
    result = np.zeros((m, n))
    for x in range(m):
        for y in range(n):
            data_point = data_map[x][y].reshape(1, -1)
            result[x, y] = classifier.predict(data_point)

    return result
