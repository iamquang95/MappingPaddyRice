import ROIHelper
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import os.path
from sklearn.externals import joblib

class PaddyRiceClassifier:

    def __init__(self, create_new=False):
        if not create_new and os.path.exists("svm_model.pkl"):
            print "Loading model..."
            self.model = joblib.load("svm_model.pkl")
            print "Model is successfully loaded."
        else:
            print "Training classifier..."
            self.model = self.train()

    def prepare_data(self):
        dir = "PaddyRice ROI"
        pos_data = np.array([])
        neg_data = np.array([])
        for year in [2005, 2010, 2015]:
            new_pos_data = ROIHelper.readPosSample(dir, year)
            pos_data = np.vstack((pos_data, new_pos_data)) if pos_data.size else new_pos_data
            new_neg_data = ROIHelper.readNegSample(dir, year)
            neg_data = np.vstack((neg_data, new_neg_data)) if neg_data.size else new_neg_data

        n_data = pos_data.shape[0] + neg_data.shape[0]
        labels = np.vstack((pos_data[:, 0:1], neg_data[:, 0:1])).reshape(n_data)
        data = np.vstack((pos_data[:, 1:], neg_data[:, 1:]))
        return data, labels

    def train(self):
        data, labels = self.prepare_data()
        original_data = data.copy()
        test_size = 0
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=113)

        # print "Number of training data: %d" % X_train.shape[0]
        # print "Number of feature: %d" % X_train.shape[1]
        # clf = svm.SVC()
        # clf.fit(X_train, y_train)
        # joblib.dump(clf, "svm_model.pkl")
        # scores = cross_val_score(clf, data, labels, cv=4)
        # print scores, np.mean(scores)
        # if (X_test.shape[0] > 0):
        #     y_pred = clf.predict(X_test)
        #     print(classification_report(y_test, y_pred))
        #     print "Accuracy:", accuracy_score(y_test, y_pred)

        # Testing with other features: only 1 index per month
        feature_month_index = [0]
        curr_day = 1
        curr_month = 1
        for i in range(1, 46):
            curr_day += 8
            if (curr_day > curr_month*60):
                curr_month += 1
                feature_month_index.append(i)
        final_index = feature_month_index
        next_index = feature_month_index
        for i in range(2):
            next_index = [x+46 for x in next_index]
            final_index.extend(next_index)

        data = data[:, final_index]
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=113)
        print "\nNumber of feature: %d" % X_train.shape[1]
        clf = svm.SVC()
        clf.fit(X_train, y_train)
        joblib.dump(clf, "svm_model.pkl")
        scores = cross_val_score(clf, data, labels, cv=4)
        print scores, np.mean(scores)
        if (X_test.shape[0] > 0):
            y_pred = clf.predict(X_test)
            print(classification_report(y_test, y_pred))
            print "Accuracy:", accuracy_score(y_test, y_pred)

        #Testing using avg of each index
        # tmp = original_data
        # xx = np.amin(tmp[:, 46*(i-1):46*i], axis=1, keepdims=True)
        # for i in range(1, 4):
        #     index_data_min = np.amin(tmp[:, 46*(i-1):46*i], axis=1, keepdims=True)
        #     index_data_max = np.amax(tmp[:, 46*(i-1):46*i], axis=1, keepdims=True)
        #     index_data_avg = np.mean(tmp[:, 46*(i-1):46*i], axis=1, keepdims=True)
        #     index_data = np.hstack((index_data_min, index_data_max, index_data_avg))
        #     data = np.hstack((data, index_data)) if i > 1 else index_data
        # # print "Size:", np.sum(data[:, 0:46], axis=1, keepdims=True).shape
        # X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=113)
        # print "\nNumber of feature: %d" % X_train.shape[1]
        # clf3 = svm.SVC()
        # clf3.fit(X_train, y_train)
        # joblib.dump(clf, "svm_model.pkl")
        # scores = cross_val_score(clf3, data, labels, cv=4)
        # print scores, np.mean(scores)
        # if (X_test.shape[0] > 0):
        #     y_pred = clf3.predict(X_test)
        #     print(classification_report(y_test, y_pred))
        #     print "Accuracy:", accuracy_score(y_test, y_pred)
        return clf

    def predict(self, X):
        feature_month_index = [0]
        curr_day = 1
        curr_month = 1
        for i in range(1, 46):
            curr_day += 8
            if (curr_day > curr_month*60):
                curr_month += 1
                feature_month_index.append(i)
        final_index = feature_month_index
        next_index = feature_month_index
        for i in range(2):
            next_index = [x+46 for x in next_index]
            final_index.extend(next_index)

        x = X[:, final_index]
        result = self.model.predict(x.reshape(1, -1))
        return int(result[0])



