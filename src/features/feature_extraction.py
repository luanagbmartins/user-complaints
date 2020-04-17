import sys
import luigi
import pickle

import ast
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append('src')
from data import PreprocessData


class FeatureExtraction(luigi.Task):

    lowercase = luigi.BoolParameter()
    tokenizer = luigi.OptionalParameter(default = None)
    stop_words = luigi.OptionalParameter(default = None)
    ngram_range = luigi.TupleParameter(default = (1,1))
    max_df = luigi.Parameter(default = '1.0')
    min_df = luigi.Parameter(default = '1')
    max_features = luigi.OptionalParameter(default = None)
    vocabulary = luigi.OptionalParameter(default = None)
    binary = luigi.BoolParameter()
    norm = luigi.ChoiceParameter(choices = ['l1', 'l2', 'none'], default = 'l2')
    use_idf = luigi.BoolParameter()
    smooth_idf = luigi.BoolParameter()
    sublinear_tf = luigi.BoolParameter()

    def __init__(self, *args, **kwargs):
        super(FeatureExtraction, self).__init__(*args, **kwargs)

        if self.norm == 'none':
            self.norm = None

        self.max_df = ast.literal_eval(self.max_df)
        self.min_df = ast.literal_eval(self.min_df)

    def requires(self):
        return PreprocessData()
    
    def output(self):
        return { 'features': luigi.LocalTarget('data/processed/features.pickle'),
                 'labels': luigi.LocalTarget('data/processed/labels.pickle') }

    def run(self):
        print('---> Extracting features...')
        data = pd.read_pickle(self.input().path)
        features, labels = self.feature_extraction(data)

        pickle.dump(features, open('data/processed/features.pickle', 'wb'))
        pickle.dump(labels, open('data/processed/labels.pickle', 'wb'))
        
        print('Done!')

    def feature_extraction(self, data):
        print('---> Converting a collection of raw documents to a matrix of TF-IDF features...')

        products_count_df = data.groupby('product_id').complaint.count().to_frame()
        products_count_df.reset_index(level=0, inplace=True)
        labels = np.array(products_count_df['product_id'].unique())

        data['complaints_untokenized'] = data['complaint'].apply(lambda x: ' '.join(x))
        tfidf_converter = TfidfVectorizer( lowercase = self.lowercase, 
                                           tokenizer = self.tokenizer,
                                           stop_words = self.stop_words,
                                           ngram_range = self.ngram_range,
                                           max_df = self.max_df,
                                           min_df = self.min_df,
                                           max_features = self.max_features,
                                           vocabulary = self.vocabulary,
                                           binary = self.binary,
                                           norm = self.norm,
                                           use_idf = self.use_idf,
                                           smooth_idf = self.smooth_idf,
                                           sublinear_tf = self.sublinear_tf )
        features = tfidf_converter.fit_transform(data.complaints_untokenized)
        print('---> Each of the %d complaints is represented by %d features (TF-IDF score of unigrams and bigrams)' %(features.shape))

        return features, labels
