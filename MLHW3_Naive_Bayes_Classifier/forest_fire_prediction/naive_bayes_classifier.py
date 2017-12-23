import preprocessing as pre
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
import scipy.stats as stats
import matplotlib.pyplot as plt
import random as rn
import numpy as np
import sklearn.naive_bayes
import csv
import sys
training_set = []
training_set_predicted = []
testing_set = []
testing_set_predicted = []
training_set, training_set_predicted, testing_set, testing_set_predicted, training_set_predicted_unlog, testing_set_predicted_unlog  = pre.preprocessing()
def validate():
    #traing the model using GaussianNB
    global training_set
    global training_set_predicted
    global testing_set
    global testing_set_predicted

    #print(testing_set_predicted)
    gnb = GaussianNB()
    my_naive_bayes_classifier = gnb.fit(training_set, training_set_predicted)
    correct_prediction = 0
    predicted_class_set = gnb.predict(testing_set)

    for i in range(len(testing_set)):
        original_class = testing_set_predicted[i]
        predicted_class = predicted_class_set[i]
        #print("testing set",i," ",testing_set[i],"original_class ",original_class,"predicted_class",predicted_class)
        if(predicted_class == original_class):
            correct_prediction += 1
    print("Gaussian Naive Bayes Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))
############################################################################################################################################
    predicted_class_set = []

    gnb = MultinomialNB(alpha=1) #using the "alpha = 1" param setting to set the laplacian smoothing
    my_naive_bayes_classifier = gnb.fit(training_set, training_set_predicted)
    correct_prediction = 0
    predicted_class_set = gnb.predict(testing_set)

    for i in range(len(testing_set)):
        original_class = testing_set_predicted[i]
        predicted_class = predicted_class_set[i]
        #print("testing set",i," ",testing_set[i],"original_class ",original_class,"predicted_class",predicted_class)
        if(predicted_class == original_class):
            correct_prediction += 1
    print("Multinomial Naive Bayes Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))
############################################################################################################################################
    predicted_class_set = []

    gnb = BernoulliNB(alpha = 1) #using the "alpha = 1" param setting to set the laplacian smoothing
    my_naive_bayes_classifier = gnb.fit(training_set, training_set_predicted)
    correct_prediction = 0
    predicted_class_set = gnb.predict(testing_set)

    for i in range(len(testing_set)):
        original_class = testing_set_predicted[i]
        predicted_class = predicted_class_set[i]
        #print("testing set",i," ",testing_set[i],"original_class ",original_class,"predicted_class",predicted_class)
        if(predicted_class == original_class):
            correct_prediction += 1
    print("Bernoulli Naive Bayes Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))

if __name__ == '__main__':
    validate()
    pre.draw_PDF()
