import numpy as np
import ImageHelper as im_helper
from PaddyRiceClassifier import PaddyRiceClassifier
import Output

dataFolderDir = "F:/DaiHoc/2016-2017 ki 1/Advanced Topics in Computer Science/Images"

classifier = PaddyRiceClassifier()


def runAlgoForYear(year):
    data_map = im_helper.extractBandForYear(dataFolderDir, year)
    m, n, k = data_map.shape
    print m, n, k
    result = np.zeros((m, n), dtype=np.int)
    for x in range(m):
        for y in range(n):
            data_point = data_map[x][y].reshape(1, -1)
            result[x, y] = classifier.predict(data_point)
    Output.createTiff(result, 'SVM', str(year))
    return result

# runAlgoForYear(2005)