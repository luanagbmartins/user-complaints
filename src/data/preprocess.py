import os
import json
import click

from sqlalchemy import create_engine
import pandas as pd

import re
import nltk
from nlt.corpus import stopwords
from nltk.corpus import wordnet as wn


def read_raw_data():

    sql_query = 'select c.product_id, main_product, sub_product,\
        complaint_text from products as p, "complaints-users" as c\
        where p.product_id=c.product_id'

    engine = create_engine(os.environ['DATABASE_URL'])
    dframe = pd.read_sql_query(sql_query, con=engine)

    return dframe


def get_wordnet_pos(word):
    """ Function that determines the the Part-of-speech (POS) tag.
    Acts as input to lemmatizer
    """

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

def clean_up(text):
    
    lemmatizer = nltk.WordNetLemmatizer().lemmatize
    stop_words = set(stopwords.words('english'))

    text = re.sub(r'[0-9]+', '', text.lower())
    text = re.sub(r'x+', '', text)
    text = re.sub('\W+', ' ', str(text))

    word_pos = nltk.pos_tag(nltk.word_tokenize(text))
    normalized_text = [lemmatizer(x[0], get_wordnet_pos(x[1])).lower() for x in word_pos]
    stop_words_free = [i for i in normalized_text if i not in english_stopwords and len(i) > 3]
    stop_words_free = list(set(stop_words_free))

    return(stop_words_free)



def preprocess_data(dframe):

    dframe = dframe.copy()
    dframe = dframe.loc[:,~dframe.columns.duplicated()]
    dframe = dframe.dropna()

    dframe = dframe.rename({'complaint_text': 'complaint'})

    dframe['complaint'] = dframe['complaint'].apply(clean_up)
    dframe = dframe[dframe.astype(str)['complaint'] != '[]']

    dframe['main_id'] = dframe['main_product'].factorize()[0]
    dframe['sub_id'] = dframe['sub_product'].factorize()[0]

    category_id_df = dframe[['main_product', 'main_id']].drop_duplicates().sort_values('main_id')
    main_category_to_id = dict(category_id_df.values)
    main_id_to_category = dict(category_id_df[['main_id', 'main_product']].values)

    category_id_df = dframe[['sub_product', 'sub_id']].drop_duplicates().sort_values('sub_id')
    sub_category_to_id = dict(category_id_df.values)
    sub_id_to_category = dict(category_id_df[['sub_id', 'sub_product']].values)

    drop_columns = ['main_product', 'sub_product', ]
    dframe.drop(drop_columns, inplace=True, axis=1)

    external_data = {
        'main_category_to_id': main_category_to_id,
        'main_id_to_category': main_id_to_category,
        'sub_category_to_id': sub_category_to_id,
        'sub_id_to_category': sub_id_to_category
    }

    return dframe, external_data


def read_processed_data(fname='data/interim/preprocessed.pickle'):

    dframe = pd.read_pickle(fname)
    return dframe


@click.command()
def main(sql_query):
    print('Preprocessing data...')

    dframe  = read_raw_data(sql_query)
    dframe, external_data = preprocess_data(dframe)

    dframe.to_pickle(os.path.join('data/interim', 'preprocessed.pickle'))

    for key, value in external_data:
        with open(os.path.join('data/external', str(key+'.json')), 'w') as fp:
            json.dump(value, fp)
    
    print('Complete!')


if __name__ == '__main__':
    main()