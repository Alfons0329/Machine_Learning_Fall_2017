from sklearn.naive_bayes import GaussianNB
import sklearn.naive_bayes
import csv
import os
import sys
import math
import numpy as np
import scipy as sp
import random as rn
training_set = []
training_set_predicted = []
testing_set = []
testing_set_predicted = []
def preprocesing():
    train_filename = sys.argv[1]
    #primitive initialization
    with open(train_filename,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    #change data type, make string to float and make the flower class become integer representation for fitting the naive_bayes classifier
    for i in range(len(all_data_list)):
        for j in range(4):
            all_data_list[i][j] = float(all_data_list[i][j])
        #do the type transformation
        if(all_data_list[i][4] == 'Iris-setosa'):
            all_data_list[i][4] = 0
        elif(all_data_list[i][4] == 'Iris-versicolor'):
            all_data_list[i][4] = 1
        elif(all_data_list[i][4] == 'Iris-virginica'):
            all_data_list[i][4] = 2
    #shuffle the dataset
    rn.shuffle(all_data_list)
    for i in range(int(len(all_data_list)*0.7)): #split
        training_set.append(all_data_list[i][0:4])
        training_set_predicted.append(all_data_list[i][4])

    for i in range(len(all_data_list)-1,int(len(all_data_list)*0.7)-1,-1):
        testing_set.append(all_data_list[i][0:4])
        testing_set_predicted.append(all_data_list[i][4])
"""
naive_bayes usage
1.
fit(X, y)	Fit Gaussian Naive Bayes according to X, y where X is the training_set and y is the corresponding result_ftype
such as X=180cm y=tall
2.
predict(X)
Perform classification on an array of test vectors X.

Parameters :
X : array-like, shape = [n_samples, n_features]
Returns :
C : array, shape = [n_samples]
Predicted target values for X

"""
def validate():
    #traing the model using GaussianNB
    gnb = GaussianNB()
    my_naive_bayes_classifier = gnb.fit(testing_set, testing_set_predicted)
    correct_prediction = 0
    predicted_class_set = gnb.predict(testing_set)

    for i in range(len(testing_set)):
        original_class = testing_set_predicted[i]
        predicted_class = predicted_class_set[i]
        print("testing set",i," ",testing_set[i],"original_class ",original_class,"predicted_class",predicted_class)
        if(predicted_class == original_class):
            correct_prediction += 1

    print("Naive Bayes Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))

if __name__ == '__main__':
    preprocesing()
    validate()
