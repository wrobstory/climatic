  # -*- coding: utf-8 -*-
'''
Header Classifier
-------

Uses the NLTK library to build a Naive Bayes classifier to classify met mast
header input for the "smart_headers" method

'''

from __future__ import print_function
import random
import nltk


def features(word):
    '''Feature extractor. Currently 1.0 accuracy'''
    features = {}
    lowerstrip = word.lower().replace(' ', '')
    features['Has std'] = 'std' in lowerstrip
    features['Has dir'] = 'dir' in lowerstrip
    features['Has w&s'] = 'w' in lowerstrip and 's' in lowerstrip
    features['Has speed'] = 'speed' in lowerstrip
    features['Has turb'] = 'turb' in lowerstrip
    features['Has dev'] = 'dev' in lowerstrip
    features['Has windd'] = 'windd' in lowerstrip
    features['Has wd'] = 'wd' in lowerstrip
    features['Has TI'] = 'TI' in word
    features['Has Max'] = 'max' in lowerstrip
    features['Has Min'] = 'min' in lowerstrip
    features['Has temp'] = 'temp' in lowerstrip
    features['has dens'] = 'dens' in lowerstrip
    features['has rho'] = 'rho' in lowerstrip
    features['has mean'] = 'mean' in lowerstrip
    return features


def combine_all(signals, descriptors):
    '''Combine attributes (WS, Direction, etc), descriptors, and heights'''
    combined_dict = {}
    for sig, sname in signals.iteritems():
        for desc, dname in descriptors.iteritems():
            sig_type = ' '.join([sig, desc])
            desc_att = [' '.join([x, y]) for x in dname for y in sname]
            heights = [''.join([str(x), 'm']) for x in xrange(0, 121, 1)]
            add_height = [' '.join([x, y]) for x in desc_att for y in heights]
            final_dict = {x: sig_type for x in add_height}
            combined_dict.update(final_dict)
    return combined_dict

if __name__ == '__main__':

    signals = {'WS': ['WS', 'WSpd', 'WSpeed', 'WndSpd', 'WndSpeed',
                      'WindSp', 'WindSpd', 'WindSpeed', 'Wind Speed'],
               'TI': ['TI', 'TurbInt', 'TIntensity', 'Turb Intensity',
                      'Turbulence Intensity', 'Turbulence'],
               'WD': ['WD', 'WDir', 'WDirection', 'WndDir',
                      'WindDirection', 'Wind Dir', 'Wnd Direction'],
               'Rho': ['rho', 'Density', 'Air Density'],
               'Temp': ['Air Temperature', 'Temp', 'Temperature']}

    descriptors = {'Mean': ['Average', 'Avg', 'Mean'],
                   'StdDev': ['StdDev', 'StDev', 'StandardDev',
                              'Standard Deviation', 'Std Deviation'],
                   'Max': ['Max', 'Maximum'],
                   'Min': ['Min', 'Minimum']}

    training_dict = combine_all(signals, descriptors)

    keys = training_dict.keys()
    random.shuffle(keys)
    header_tuples = [(x, training_dict[x]) for x in keys]

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
