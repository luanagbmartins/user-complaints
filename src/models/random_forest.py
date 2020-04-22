import sys
import pickle
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score


class RandomForestModel(object):

    def __init__(self, n_estimators, max_depth, verbose=1):
        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, verbose=verbose)
        self.name = 'RandomForest'

    def get_params(self):
        return self.model.get_params()

    def train(self, features, labels):
        self.model.fit(features, labels)

    def predict(self, feature):
        label_pred = self.model.predict(feature)
        return label_pred

    def score(self, features, labels):
        predictions = self.model.predict(features)

        accuracy = accuracy_score(labels, predictions)
        precision = precision_score(labels, predictions, average='macro')
        recall = recall_score(labels, predictions, average='macro')

        results = {
            'params': self.get_params(),
            'model': self.name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall
        }

        print('---> Accuracy obtained is: {0:.2f}%'.format(accuracy*100))

        figures = {}
        return results, figures

    def save(self, filename):
        with open(filename, 'wb') as fp:
            pickle.dump(self.model, fp)