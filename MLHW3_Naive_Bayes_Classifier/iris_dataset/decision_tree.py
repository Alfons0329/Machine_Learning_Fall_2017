import naive_bayes_classifier as nbc#my module
from sklearn import tree
import csv
import os
import sys
import math
import numpy as np
import scipy as sp
import random as rn

def validate():
    #traing the model using GaussianNB
    training_set, training_set_predicted, testing_set, testing_set_predicted = nbc.preprocesing()
    dt = tree.DecisionTreeClassifier()
    decision_tree_classfier = dt.fit(training_set,training_set_predicted)

    correct_prediction = 0
    predicted_class_set = dt.predict(testing_set)

    for i in range(len(testing_set)):
        original_class = testing_set_predicted[i]
        predicted_class = predicted_class_set[i]
        print("testing set",i," ",testing_set[i],"original_class ",original_class,"predicted_class",predicted_class)
        if(predicted_class == original_class):
            correct_prediction += 1

    print("Decision Tree Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))
if __name__ == '__main__':

    validate()
