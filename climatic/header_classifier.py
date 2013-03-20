# -*- coding: utf-8 -*-
'''
Header Classifier
-------

Uses the NLTK library to build a Naive Bayes classifier to classify met mast
header input for the "smart_headers" method

'''

from __future__ import print_function
import json
import nltk
import os


def features(word):
    '''Feature extractor. Currently 0.966 accuracy'''
    features = {}
    lowerit = word.lower()
    features['Has std'] = 'std' in lowerit
    features['Has dir'] = 'dir' in lowerit
    features['Has spd'] = 's' in lowerit and 'p' in lowerit and 'd' in lowerit
    features['Has turb'] = 'turb' in lowerit
    features['Has dev'] = 'dev' in lowerit
    features['Has windd'] = 'windd' in lowerit
    features['Has wd'] = 'wd' in lowerit
    features['Has TI'] = 'TI' in word
    return features

if __name__ == '__main__':
    #Read json from pkg
    pkg_dir, filename = os.path.split(__file__)
    json_path = os.path.join(pkg_dir, 'data', 'header_training.json')
    with open(json_path, 'r') as f:
        training_dict = json.load(f)

    header_tuples = [(x, y) for x, y in training_dict.iteritems()]

    #Break into training, test, and devtest data
    train_header = header_tuples[1500:]
    devtest_header = header_tuples[500:1500]
    test_header = header_tuples[:500]
    train_set = [(features(x), y) for (x, y) in train_header]
    test_set = [(features(x), y) for (x, y) in test_header]

    classifier = nltk.NaiveBayesClassifier.train(train_set)

    #Headers that are throwing it off, for the curious...
    errors = []
    for (header, tag) in devtest_header:
        guess = classifier.classify(features(header))
        if guess != tag:
            errors.append((tag, guess, header))

    print('Accuracy on test set is: ',
          nltk.classify.accuracy(classifier, test_set))
    print(classifier.show_most_informative_features(5))
