import ROIHelper
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import os.path
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

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
        test_size = 0

        C_range = np.logspace(-4, 4, 9)
        gamma_range = np.logspace(-4, 4, 9)
        param_grid = dict(gamma=gamma_range, C=C_range)
        param_grid['kernel'] = ['rbf']

        # Testing with features: only 2 index per month
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
        grid = GridSearchCV(SVC(), param_grid=param_grid, cv=10)
        grid.fit(X_train, y_train)
        print "Best parameters:", grid.best_params_
        print "Best score:", grid.best_score_

        clf = grid.best_estimator_
        clf.fit(X_train, y_train)
        joblib.dump(clf, "svm_model.pkl")
        if (X_test.shape[0] > 0):
            y_pred = clf.predict(X_test)
            print(classification_report(y_test, y_pred))
            print "Accuracy:", accuracy_score(y_test, y_pred)

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



