import sys
import numpy as np
import pandas as pd

import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier


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

        # Confusion Matrix
        confusion = confusion_matrix(labels, predictions)
        sns_plot = sns.heatmap(confusion, annot=True, fmt='g', cmap='Blues')
        sns_plot.set(ylabel = 'Valor verdadeiro')
        sns_plot.set(xlabel = 'Valor previsto')
        labels = [ 'Verdadeiro Negativo', 
                   'Falso Positivo', 
                   'Falso Negativo', 
                   'Verdadeiro Positivo' ]
        sns_plot.set(yticklabels = ['Negativo','Positivo'])
        sns_plot.set(xticklabels = ['Negativo','Positivo'])
        count = 0
        bacc = []
        for idx, text in enumerate(sns_plot.texts):
            label = int(text.get_text())
            count += label
            bacc.append(label)

        acc1 = bacc[0] / ( bacc[0] + bacc[2] )
        acc2 = bacc[3] / ( bacc[1] + bacc[3] ) 
        balanced_accuracy = ( acc1 + acc2 ) / 2
        for idx, text in enumerate(sns_plot.texts):
            square = text.get_text()
            percent = int(text.get_text()) / count
            percent = "{0:.0%}".format(percent)
            box_text = "{0}: \n \n {1} \n \n {2}".format(labels[idx], square, percent)
            text.set_text(box_text)
        sns_plot.set_title('Matriz de Confusão')

        figures = {'confusion_matrix': sns_plot}

        return accuracy, figures
