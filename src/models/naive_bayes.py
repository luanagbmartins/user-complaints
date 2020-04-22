import sys
import numpy as np
import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score


class NaiveBayesModel(object):

    def __init__(self):
        self.model = MultinomialNB()
        self.name = 'NaiveBayes'

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

        print('---> Accuracy obtained is: {0:.2f}%'.format(accuracy))

        figures = {}
        return results, figures
