import os
import sys
import json
import luigi

import pandas as pd
from sqlalchemy import create_engine

import re
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
 
sys.path.append('src')
from utils import timeit


class PreprocessData(luigi.Task):
    def requires(self):
        return RawData()
    
    def output(self):
        return luigi.LocalTarget('data/interim/preprocessed.pickle')

    def run(self):
        print('Cleaning data...')

        dframe = pd.read_pickle(self.input()['raw'].path)
        dframe = self.preprocess_data(dframe)

        dframe.to_pickle(os.path.join('data/interim', 'preprocessed.pickle'))
        print('Done !')

    def get_wordnet_pos(self, word):
        if word.startswith('N'):
            return wn.NOUN
        elif word.startswith('V'):
            return wn.VERB
        elif word.startswith('J'):
            return wn.ADJ
        elif word.startswith('R'):
            return wn.ADV
        else:
            return wn.NOUN

    def clean_up(self, text):
        lemmatizer = nltk.WordNetLemmatizer().lemmatize
        stop_words = set(stopwords.words('english'))

        text = re.sub(r'[0-9]+', '', text.lower())
        text = re.sub(r'x+', '', text)
        text = re.sub('\W+', ' ', str(text))

        word_pos = nltk.pos_tag(nltk.word_tokenize(text))
        normalized_text = [lemmatizer(x[0], self.get_wordnet_pos(x[1])).lower() for x in word_pos]
        stop_words_free = [i for i in normalized_text if i not in stop_words and len(i) > 3]
        stop_words_free = list(set(stop_words_free))

        return(stop_words_free)

    def preprocess_data(self, dframe):
        dframe = dframe.copy()
        dframe = dframe.loc[:,~dframe.columns.duplicated()]
        dframe = dframe.dropna()

        dframe = dframe.rename(columns={'complaint_text': 'complaint'})

        dframe['complaint'] = dframe['complaint'].apply(self.clean_up)
        dframe = dframe[dframe.astype(str)['complaint'] != '[]']

        return dframe


class RawData(luigi.Task):

    def requires(self):
        None
    
    def output(self):
        return { 'raw': luigi.LocalTarget('data/raw/raw_data.pickle'),
                 'external': luigi.LocalTarget('data/external/external_data.txt') }

    def run(self):
        print('Reading data...')
        dframe = self.read_raw_data()
        dframe, external_data = self.raw_data(dframe)

        dframe.to_pickle(os.path.join('data/raw', 'raw_data.pickle'))

        for key in external_data:
            with open(os.path.join('data/external', str(key+'.json')), 'w') as fp:
                json.dump(external_data[key], fp)

        with open(os.path.join('data/external', 'external_data.txt'), 'a+') as fp:
            fp.write('External data generated:\n')
            for key in external_data:
                fp.write(str(key + '.json\n'))
        

    def read_raw_data(self):
        sql_query = 'select c.product_id, main_product, sub_product,\
            complaint_text from products as p, "complaints-users" as c\
            where p.product_id=c.product_id'

        engine = create_engine(os.environ['DATABASE_URL'])
        dframe = pd.read_sql_query(sql_query, con=engine)

        return dframe

    def raw_data(self, dframe):
        dframe = dframe.copy()
        dframe = dframe.loc[:,~dframe.columns.duplicated()]
        dframe = dframe.dropna()

        dframe['main_product_id'] = dframe['main_product'].factorize()[0]
        dframe['sub_product_id'] = dframe['sub_product'].factorize()[0]
        dframe['product'] = dframe[['main_product_id','sub_product_id']].apply(lambda x : tuple(x), axis=1)

        category_id_df = dframe[['product_id', 'product']].drop_duplicates().sort_values('product_id')
        product_id_to_category = dict(category_id_df.values)

        category_id_df = dframe[['main_product', 'main_product_id']].drop_duplicates().sort_values('main_product_id')
        main_category_to_id = dict(category_id_df.values)
        main_id_to_category = dict(category_id_df[['main_product_id', 'main_product']].values)

        category_id_df = dframe[['sub_product', 'sub_product_id']].drop_duplicates().sort_values('sub_product_id')
        sub_category_to_id = dict(category_id_df.values)
        sub_id_to_category = dict(category_id_df[['sub_product_id', 'sub_product']].values)

        drop_columns = ['main_product', 'sub_product', ]
        dframe.drop(drop_columns, inplace=True, axis=1)

        external_data = {
            'product_id_to_category': product_id_to_category,
            'main_category_to_id': main_category_to_id,
            'main_id_to_category': main_id_to_category,
            'sub_category_to_id': sub_category_to_id,
            'sub_id_to_category': sub_id_to_category
        }

        return dframe, external_data