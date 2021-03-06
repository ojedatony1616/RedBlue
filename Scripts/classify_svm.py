import os
import time
import pickle

from bs4 import BeautifulSoup
from sklearn.datasets.base import Bunch
from sklearn import metrics
from sklearn import cross_validation as cv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix
from sklearn.svm import SVC
from sklearn import svm
from sklearn import grid_search
from sklearn.feature_extraction import text
import lxml
import pprint

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split as tts

## For data exploration
import pandas as pd
import numpy as np
import pandas.io.sql as pd_sql
import sqlite3 as sql

# For encoding
import codecs

# For visualization
from sklearn.decomposition import PCA

import string

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag




################################################################################
# This script ingests debate data, vectorizes the data, fits it to three
# different ML models (Logistic Regression, Multinomial Naive Bayes, and Support
#  Vector Machine), truncates the vectorizers to make them leaner,
# Chooses the best model, optimizes its parameters,and saves ("pickles") models
################################################################################

#CONNECTING TO THE DATASET
CORPUS_ROOT = "/Users/Goodgame/desktop/RedBlue/data/debate_data/"

def load_data(root=CORPUS_ROOT):
    """
    Loads the text data into memory using the bundle dataset structure.
    Note that on larger corpora, memory safe CorpusReaders should be used.
    """

    # Open the README and store
    with open(os.path.join(root, 'README'), 'r') as readme:
        DESCR = readme.read()

    # Iterate through all the categories
    # Read the HTML into the data and store the category in target
    data      = []
    target    = []
    filenames = []

    for category in os.listdir(root):
        if category == "README": continue # Skip the README
        if category == ".DS_Store": continue # Skip the .DS_Store file
        for doc in os.listdir(os.path.join(root, category)):
            fname = os.path.join(root, category, doc)

            # Store information about document
            filenames.append(fname)
            target.append(category)
            with codecs.open(fname, 'r', 'ISO-8859-1') as f:
                data.append(f.read())
            # Read data and store in data list
            # with open(fname, 'r') as f:
            #     data.append(f.read())

    return Bunch(
        data=data,
        target=target,
        filenames=filenames,
        target_names=frozenset(target),
        DESCR=DESCR,
    )

dataset = load_data()

#print out the readme file
print dataset.DESCR
#Remember to create a README file and place it inside your CORPUS ROOT directory if you haven't already done so.

#print the number of records in the dataset
print "The number of instances is ", len(dataset.data), "\n"

#Checking out the data
print "Here are the last five instances: ", dataset.data[-5:], "\n"
print "Here are the categories of the last five instances: \n", dataset.target[-5:],
"\n\n"


#FEATURE ENGINEERING
#Creating an augmented stop words list comprised of 'english' words and candidate and moderator names.
candmodnames = ["donald","trump","ted","cruz","john","kasich","marco","rubio","ben","carson",
                "jeb","bush","chris","christie","carly","fiorina","mike","huckabee","rick","perry",
                "scott","walker","rand","paul","bobby","jindal","lindsey","graham","jim","gilmore",
                "george","pataki","rick","santorum","hillary","clinton","bernie","sanders","martin",
                "o'malley","lincoln","chaffe","jim","webb",'hemmer','maccallum','tapper','bash',
                'hewitt','harwood','quick','quintanilla','regan','seib','smith','blitzer','baier',
                'kelly','wallace','baker','bartiromo','cavuto','muir','raddatz','garrett','strassel',
                'arraras','dinan','cooper','lemon','lopez','cordes','cooney','dickerson','obradovich',
                'holt','mitchell','todd','maddow','ifill','woodruff','ramos','salinas','tumulty','louis']

stop_words = text.ENGLISH_STOP_WORDS

custom_stop_words = text.ENGLISH_STOP_WORDS.union(candmodnames)

#TfIdfVectorizer: CountVectorizer and TfIdfTransformer all in one step
tfidf = TfidfVectorizer(stop_words=custom_stop_words)
X_train_tfidf_1 = tfidf.fit_transform(dataset.data)
print "\n Here are the dimensions of our dataset: \n", X_train_tfidf_1.shape, "\n"

# Singular Value Decomposition: Model fit and transform
# This identifies the optimal number of features to select out of all created in the tf-idf vectorizer
# and truncates the vectorizer to make it leaner.

#Without any truncating of the Logistic Regression model (11,288 features), the f1-score = 0.80 and the accuracy_score = 0.82.
#Without any truncating of the Multinomial Naive Bayes model (11,288 features), the f1-score = 0.73 and the accuracy_score = 0.78.
#Without any truncating of the Support Vector Machine model (11,288 features), the f1-score = 0.83 and the accuracy_score = 0.84.

# tsvd      = TruncatedSVD(n_components=100)
# X_train_tfidf_100 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_100.shape
#LR: f1-score = 0.74 and the accuracy_score = 0.77.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.76 and the accuracy_score = 0.79.

# tsvd      = TruncatedSVD(n_components=1000)
# X_train_tfidf_1000 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_1000.shape
#LR: f1-score = 0.79 and the accuracy_score = 0.81.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.82 and the accuracy_score = 0.83.

# tsvd      = TruncatedSVD(n_components=1500)
# X_train_tfidf_1500 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_1500.shape
#LR: f1-score = 0.80 and the accuracy_score = 0.82.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.83 and the accuracy_score = 0.84.

tsvd = TruncatedSVD(n_components=2000)
X_train_tfidf_2000 = tsvd.fit_transform(X_train_tfidf_1)
print X_train_tfidf_2000.shape
#LR: f1-score = 0.81 and the accuracy_score = 0.83.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.84 and the accuracy_score = 0.84.

# tsvd      = TruncatedSVD(n_components=3000)
# X_train_tfidf_3000 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_3000.shape
#LR: f1-score = 0.81 and the accuracy_score = 0.83.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.83 and the accuracy_score = 0.84.

# tsvd      = TruncatedSVD(n_components=4000)
# X_train_tfidf_4000 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_4000.shape
#LR: f1-score = 0.81 and the accuracy_score = 0.83.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.83 and the accuracy_score = 0.84.

# tsvd      = TruncatedSVD(n_components=5000)
# X_train_tfidf_5000 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_5000.shape
#LR: f1-score = 0.80 and the accuracy_score = 0.82.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.83 and the accuracy_score = 0.84.

# tsvd      = TruncatedSVD(n_components=8000)
# X_train_tfidf_8000 = tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_8000.shape
#LR: f1-score = 0.80 and the accuracy_score = 0.82.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.83 and the accuracy_score = 0.84.

# tsvd      = TruncatedSVD(n_components=11000)
# X_train_tfidf_11000= tsvd.fit_transform(X_train_tfidf_1)
# print X_train_tfidf_11000.shape
#LR: f1-score = 0.81 and the accuracy_score = 0.83.
#MNB: f1-score = xx and the accuracy_score = xx.
#SVM: f1-score = 0.83 and the accuracy_score = 0.84.

#FINAL MODEL GOING FORWARD BASED ON THESE RESULTS (fewest features with the greatest performance):
X_train_tfidf = X_train_tfidf_2000
print X_train_tfidf.shape

##ANALYTICAL MODELING##

#Logistic Regression: Model fit, transform, and testing
splits = cv.train_test_split(X_train_tfidf, dataset.target, test_size=0.2)
X_train, X_test, Y_train, Y_test = splits

model_lr = LogisticRegression()
model_lr.fit(X_train, Y_train)

## Variable "expected" is our actual category, dem or rep.
expected = Y_test

#Variable "predicted" is our model's prediction based on the training data, dem or rep
predicted = model_lr.predict(X_test)

print "\n Logistic Regression classification report (accuracy): \n"
print classification_report(expected, predicted)
print "Logistic Regression confusion matrix. Clockwise from top left, it's"
print "# correct dem classifications, # incorrect dem, # incorrect rep, # correct rep:"
print metrics.confusion_matrix(expected, predicted)
print "\n"
print "Logistic Regression model accuracy score: \n"
print metrics.accuracy_score(expected, predicted)

# Multinomial Naive Bayes: Model fit, transform, and testing
# Note that this model could not operate with the SVD, so it relies on the originally
# fitted tf-idf model with 11,228 features.
splits = cv.train_test_split(X_train_tfidf_1, dataset.target, test_size=0.2)
X_train, X_test, Y_train, Y_test = splits

model_mnb = MultinomialNB()
model_mnb.fit(X_train, Y_train)

expected = Y_test
predicted = model_mnb.predict(X_test)

print "\n Multinomial Naive Bayes classification report (accuracy) \n"
print classification_report(expected, predicted)
print "Here's a matrix showing results. Clockwise from top left, it's"
print " # correct dem classifications, # incorrect dem, # incorrect rep, # correct rep"
print metrics.confusion_matrix(expected, predicted)
print "\n"
print "Multinomial Naive Bayes model accuracy score: \n"
print metrics.accuracy_score(expected, predicted)

# Support Vector Machine: Model fit, transform, and testing

splits = cv.train_test_split(X_train_tfidf, dataset.target, test_size=0.2)
X_train, X_test, Y_train, Y_test = splits

model_svm = svm.LinearSVC()
model_svm.fit(X_train, Y_train)

expected = Y_test
predicted = model_svm.predict(X_test)

print "\n Support Vector Machine classification report (accuracy): \n"
print classification_report(expected, predicted)
print "Here's a matrix showing results. Clockwise from top left, it's"
print " # correct dem classifications, # incorrect dem, # incorrect rep, # correct rep"
print metrics.confusion_matrix(expected, predicted)
print "\n"
print "Support Vector Machine model accuracy score: \n"
print metrics.accuracy_score(expected, predicted)

# GRID SEARCH FOR SVM MODEL, OPTIMIZING PARAMETER 'C'
# Code commented out; the results of the grid search are applied to the SVM
# model below.

    #GRID SEARCH - Searching for optimal parameter values
    # parameters = {'C':[1, 10, 100, 1000]}
    # grid_search = grid_search.GridSearchCV(model_svm, parameters)
    # grid_search.fit(X_train, Y_train)
    # print grid_search.grid_scores_
    # print grid_search.best_estimator_
    #Best estimator was C=1.

    #Narrowing down by order of magnitude.
    # parameters = {'C':[1,2,3,4,5,6,7,8,9]}
    # grid_search_1 = grid_search.GridSearchCV(model_svm, parameters)
    # grid_search_1.fit(X_train, Y_train)
    # print grid_search_1.grid_scores_
    # print grid_search_1.best_estimator_
    #Best estimator was C=1.

    #Narrowing down by order of magnitude.
    # parameters = {'C':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]}
    # grid_search = grid_search.GridSearchCV(model_svm, parameters)
    # grid_search.fit(X_train, Y_train)
    # print grid_search.grid_scores_
    # print grid_search.best_estimator_
    #Best estimator was C=0.5.

    #Re-centering search.
    # parameters = {'C':[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}
    # grid_search = grid_search.GridSearchCV(model_svm, parameters)
    # grid_search.fit(X_train, Y_train)
    # print grid_search.grid_scores_
    # print grid_search.best_estimator_
    #Best estimator was C=0.5.

#Narrowing down by order of magnitude.
parameters = {'C':[0.45, 0.46, 0.47, 0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55]}
grid_search = grid_search.GridSearchCV(model_svm, parameters)
grid_search.fit(X_train, Y_train)
print grid_search.grid_scores_
print grid_search.best_estimator_
#Best estimator was C=0.45. Because we already compared 0.4 to 0.5 two searches above, and 0.5 was selected, we induce that 0.45 is the optimal value without searching between 0.40 and 0.45.

#Returning model results with optimal 'C' value.
expected = Y_test
predicted = grid_search.predict(X_test)

print classification_report(expected, predicted)
print metrics.confusion_matrix(expected, predicted)
print metrics.accuracy_score(expected, predicted)

#Support Vector Machine: Model fit, transform, and testing with optimized 'C' value
splits = cv.train_test_split(X_train_tfidf, dataset.target, test_size=0.2)
X_train, X_test, Y_train, Y_test = splits

model_svm = svm.LinearSVC(C=0.45, class_weight=None, dual=True, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
     verbose=0)
model_svm.fit(X_train, Y_train)

expected   = Y_test
predicted  = model_svm.predict(X_test)

print classification_report(expected, predicted)
print metrics.confusion_matrix(expected, predicted)
print metrics.accuracy_score(expected, predicted)

# Saving/Picking Models

## Pickle TFIDF
modelpath = '/Users/Goodgame/desktop/RedBlue/models/' #This should be customized.

with open (modelpath + 'tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

## Pickle TSVD, Truncated Singlular Value Decomposition
## (The model that removed less predictive features from dataset)

modelpath = '/Users/Goodgame/desktop/RedBlue/models/' #This should be customized.

with open (modelpath + 'tsvd.pkl', 'wb') as f:
    pickle.dump(tsvd, f)

# Pickle Support Vector Machine
modelpath = '/Users/Goodgame/desktop/RedBlue/models/' #This should be customized.

with open (modelpath + 'model_svm.pkl', 'wb') as f:
    pickle.dump(model_svm, f)
#
#
# #informative features
# classifier = SGDClassifier
# # Label encode the targets
# labels = LabelEncoder()
# y = labels.fit_transform(dataset.target)
# X_train, X_test, Y_train, Y_test = cv.train_test_split(dataset.data, y, test_size=0.2)
# def identity(arg):
#     """
#     Simple identity function works as a passthrough.
#     """
#     return arg
# class NLTKPreprocessor(BaseEstimator, TransformerMixin):
#     def __init__(self, stopwords=None, punct=None,
#                  lower=True, strip=True):
#         self.lower      = lower
#         self.strip      = strip
#         self.stopwords  = custom_stop_words
#         self.punct      = punct or set(string.punctuation)
#         self.lemmatizer = WordNetLemmatizer()
#     def fit(self, X, y=None):
#         return self
#     def inverse_transform(self, X):
#         return [" ".join(doc) for doc in X]
#     def transform(self, X):
#         return [
#             list(self.tokenize(doc)) for doc in X
#         ]
#     def tokenize(self, document):
#         # Break the document into sentences
#         document = document.decode('ascii', 'ignore')
#         for sent in sent_tokenize(document):
#             # Break the sentence into part of speech tagged tokens
#             for token, tag in pos_tag(wordpunct_tokenize(sent)):
#                 # Apply preprocessing to the token
#                 token = token.lower() if self.lower else token
#                 token = token.strip() if self.strip else token
#                 token = token.strip('_') if self.strip else token
#                 token = token.strip('*') if self.strip else token
#                 # If stopword, ignore token and continue
#                 if token in self.stopwords:
#                     continue
#                 # If punctuation, ignore token and continue
#                 if all(char in self.punct for char in token):
#                     continue
#                 # Lemmatize the token and yield
#                 lemma = self.lemmatize(token, tag)
#                 yield lemma
#     def lemmatize(self, token, tag):
#         tag = {
#             'N': wn.NOUN,
#             'V': wn.VERB,
#             'R': wn.ADV,
#             'J': wn.ADJ
#         }.get(tag[0], wn.NOUN)
#         return self.lemmatizer.lemmatize(token, tag)
# def build(classifier, X, y=None):
#     if isinstance(classifier, type):
#         classifier = classifier()
#     model = Pipeline([
#         ('preprocessor', NLTKPreprocessor()),
#         ('vectorizer', TfidfVectorizer(
#             tokenizer=identity, preprocessor=None, lowercase=False
#         )),
#         ('classifier', classifier),
#     ])
#     model.fit_transform(X, y)
#     return model
# feature_model = build(classifier, X_train, Y_train)
# Y_pred = feature_model.predict(X_test)
# print(classification_report(Y_test, Y_pred, target_names=labels.classes_))
# feature_model = build(classifier, X_train_tfidf, y)
# feature_model.labels_ = labels
# def show_most_informative_features(model, text=None, n=20):
#     # Extract the vectorizer and the classifier from the pipeline
#     vectorizer = model.named_steps['vectorizer']
#     classifier = model.named_steps['classifier']
#     # Check to make sure that we can perform this computation
#     if not hasattr(classifier, 'coef_'):
#         raise TypeError(
#             "Cannot compute most informative features on {}.".format(
#                 classifier.__class__.__name__
#             )
#         )
#     if text is not None:
#         # Compute the coefficients for the text
#         tvec = model.transform([text]).toarray()
#     else:
#         # Otherwise simply use the coefficients
#         tvec = classifier.coef_
#     # Zip the feature names with the coefs and sort
#     coefs = sorted(
#         zip(tvec[0], vectorizer.get_feature_names()),
#         key=itemgetter(0), reverse=True
#     )
#     # Get the top n and bottom n coef, name pairs
#     topn  = zip(coefs[:n], coefs[:-(n+1):-1])
#     # Create the output string to return
#     output = []
#     # If text, add the predicted value to the output.
#     if text is not None:
#         output.append("\"{}\"".format(text))
#         output.append(
#             "Classified as: {}".format(model.predict([text]))
#         )
#         output.append("")
#     # Create two columns with most negative and most positive features.
#     for (cp, fnp), (cn, fnn) in topn:
#         output.append(
#             "{:0.4f}{: >15}    {:0.4f}{: >15}".format(
#                 cp, fnp, cn, fnn
#             )
#         )
#     return "\n".join(output)
# print show_most_informative_features(feature_model)
