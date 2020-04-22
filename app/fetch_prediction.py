import os
import json
import pickle

import re
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

import sys
sys.path.append('..')

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB


def get_wordnet_pos(word):
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
    stop_words_free = [i for i in normalized_text if i not in stop_words and len(i) > 3]
    stop_words_free = list(set(stop_words_free))

    return(stop_words_free)

def process_text(complaint):

    cleaned_complaint = clean_up(complaint)

    with open('data/processed/tfidf/vectorizer.pickle', 'rb') as file:
        vectorizer = pickle.load(file)
    with open('models/model.pickle', 'rb') as file:
        model = pickle.load(file)

    in_ = vectorizer.transform(cleaned_complaint)
    prediction = model.predict(in_)

    with open('data/external/product_id_to_category.json', 'r') as file:
        product_id_to_category = json.load(file)
    with open('data/external/main_id_to_category.json', 'r') as file:
        main_id_to_category = json.load(file)
    with open('data/external/sub_id_to_category.json', 'r') as file:
        sub_id_to_category = json.load(file)

    category = product_id_to_category[str(prediction[0])]
    main_product = main_id_to_category[str(category[0])]
    sub_product = sub_id_to_category[str(category[1])]

    return main_product, sub_product