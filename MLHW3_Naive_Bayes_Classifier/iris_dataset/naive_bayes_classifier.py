from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
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
def preprocesing():
    train_filename = sys.argv[1]
    testing_filename = sys.argv[2]
    global training_set
    global training_set_predicted
    global testing_set
    global testing_set_predicted

    with open(train_filename,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        training_set = list(parsed_data)

    with open(testing_filename,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        testing_set = list(parsed_data)

    #change data type, make string to float and make the flower class become integer representation for fitting the naive_bayes classifier
    for i in range(len(training_set)):
        for j in range (len(training_set[i])-1):
            training_set[i][j] = float(training_set[i][j])

        if(training_set[i][4] == 'Iris-setosa'):
            training_set[i][4] = 0
        elif(training_set[i][4] == 'Iris-versicolor'):
            training_set[i][4] = 1
        elif(training_set[i][4] == 'Iris-virginica'):
            training_set[i][4] = 2

        training_set_predicted.append(training_set[i][4])
        training_set[i] = training_set[i][0:4] #move the class away

    for i in range(len(testing_set)):
        for j in range (len(testing_set[i])-1):
            testing_set[i][j] = float(testing_set[i][j])

        if(testing_set[i][4] == 'Iris-setosa'):
            testing_set[i][4] = 0
        elif(testing_set[i][4] == 'Iris-versicolor'):
            testing_set[i][4] = 1
        elif(testing_set[i][4] == 'Iris-virginica'):
            testing_set[i][4] = 2

        testing_set_predicted.append(testing_set[i][4])
        testing_set[i] = testing_set[i][0:4] #move the class away

    return training_set, training_set_predicted, testing_set, testing_set_predicted
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
http://blog.csdn.net/jinping_shi/article/details/51771867
"""
def draw_PDF():
    global training_set
    global training_set_predicted
    global testing_set
    global testing_set_predicted
    training_set = np.array(training_set)
    plt.figure() #make an empty canvas

    for i in range(0,4):
        tf = training_set[:,i]
        tf.sort()
        plt.title(f' feature {i+1}: PDF')
        mean = np.mean(tf)
        std = np.std(tf)
        pdf = stats.norm.pdf(tf,mean,std)
        plt.subplot(2,2,i+1)
        plt.plot(tf,pdf)

    plt.tight_layout()
    plt.savefig("PDF.png",dpi=600)
    plt.show()

def validate():
    #traing the model using GaussianNB
    global training_set
    global training_set_predicted
    global testing_set
    global testing_set_predicted

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

if __name__ == '__main__':
    preprocesing()
    validate()
    draw_PDF()
