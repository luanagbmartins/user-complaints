import sys
import numpy as np
import pandas as pd

import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB

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
        predictions_conf = self.model.predict_proba(features)

        predictions_conf_df = pd.DataFrame( predictions_conf, 
                                            index = range(predictions_conf.shape[0]),
                                            columns = range(predictions_conf.shape[1]) )

        predictions_conf_df['predicted_conf'] = predictions_conf_df.max(axis = 1)
        
        results = pd.DataFrame(data = {"actual_label": labels, "predicted_label": predictions})
        results = pd.concat([results, predictions_conf_df['predicted_conf']], axis=1)

        results['correctly_predicted'] = np.where(results['actual_label'] == results['predicted_label'], 1, 0)
        accuracy = (results['correctly_predicted'].sum() / results.shape[0]) * 100
        print('---> Accuracy obtained is: {0:.2f}%'.format(accuracy))

        return accuracy
