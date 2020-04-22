import os
import sys
import ast
import json
import luigi
import pickle
import datetime

from sklearn.model_selection import train_test_split
# from sklearn.model_selection import StratifiedKFold

sys.path.append('src')
from features import FeatureExtraction
from models import RandomForestModel, NaiveBayesModel


class TrainModel(luigi.Task):
    # TODO parameters description with 'help' argument
    test_size = luigi.FloatParameter(default = 0.25)
    random_state = luigi.Parameter(default = 'None')
    shuffle = luigi.BoolParameter()
    selected_model = luigi.ChoiceParameter(choices = ['naive_bayes', 'random_forest', 'svm'], default = 'naive_bayes')
    verbose = luigi.IntParameter(default=0)

    # Random forest
    n_estimators = luigi.IntParameter(default = 100)
    max_depth = luigi.Parameter(default = 'None')


    def __init__(self, *args, **kwargs):
        super(TrainModel, self).__init__(*args, **kwargs)

        self.random_state = ast.literal_eval(self.random_state)
        self.max_depth = ast.literal_eval(self.max_depth)

    def requires(self):
        return FeatureExtraction()

    def output(self):
        return None

    def run(self):
        print('---> Spliting data')
        features = pickle.load(open(self.input()['features'].path, 'rb'))
        labels = pickle.load(open(self.input()['labels'].path, 'rb'))

        train_features, test_features, train_labels, test_labels = \
            train_test_split(features, labels, test_size = self.test_size, 
                             random_state = self.random_state, shuffle = self.shuffle)

        # TODO
        # kfold = StratifiedKFold(n_splits=10, shuffle=True)

        if self.selected_model == 'random_forest':
            model = RandomForestModel( n_estimators = self.n_estimators, 
                                       max_depth = self.max_depth,
                                       verbose = self.verbose )
        elif self.selected_model == 'naive_bayes':
            model = NaiveBayesModel()
        elif self.selected_model == 'svm':
            raise NotImplementedError

        print('---> Training model', model.name)
        model.train(train_features, train_labels)
        results, figures = model.score(test_features, test_labels)

        print('---> Saving Model')
        output_name = model.name + '||Accuray=' + str(round(results['accuracy'], 2))
        output_name += '||' + datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        save_folder = os.path.join('models', output_name)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        with open(os.path.join(save_folder, 'results.json'), 'w') as fp:
            json.dump(results, fp)

        for key in figures:
            with open(os.path.join(save_folder, str(key+'.png')), 'w') as fp:
                figures.savefig(fp)

        with open(os.path.join(save_folder, 'model.pickle'), 'wb') as fp:
            pickle.dump(model, fp)



