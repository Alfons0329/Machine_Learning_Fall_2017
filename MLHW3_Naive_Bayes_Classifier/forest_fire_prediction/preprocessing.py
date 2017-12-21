"""
How to draw PDF?https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv
import sys
import math
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
        for j in range (4,len(training_set[i])):
            training_set[i][j] = float(training_set[i][j])

        if training_set[i][len(training_set[i])-1]: #prevent log(0) math domain exception
            training_set[i][len(training_set[i])-1] = math.log10(training_set[i][len(training_set[i])-1]) #logarithmic transformation of the last data, since it is quite skew

        training_set_predicted.append(training_set[i][len(training_set[i])-1])
        training_set[i] = training_set[i][4:12] #move the class away [4,12)

    for i in range(len(testing_set)):
        for j in range (4,len(testing_set[i])):
            testing_set[i][j] = float(testing_set[i][j])

        if testing_set[i][len(testing_set[i])-1]: #prevent log(0) math domain exception
            testing_set[i][len(testing_set[i])-1] = math.log10(testing_set[i][len(testing_set[i])-1])

        testing_set_predicted.append(testing_set[i][len(training_set[i])-1])
        testing_set[i] = testing_set[i][4:12] #move the class away [4,12)

    return training_set, training_set_predicted, testing_set, testing_set_predicted

def draw_PDF():
    global training_set
    global training_set_predicted
    global testing_set
    global testing_set_predicted
    training_set = np.array(training_set)#temporary convert to numpy array for plotting the pdf

    for i in range(len(training_set))
        train_feature = training_set[:,i]
        plt.title("Forestfire feature "i": FFMC Probability Distribution Function")
        #normalize the data and whoe the data
        train_mean = np.mean(train_feature)
        train_std = np.std()
        sp.stats.pdf #use the scipy pdf function to show it



    train_feature_1 = training_set[:,0]
    print("tf7",len(training_set[1]))

    train_feature_2 = training_set[:,1]
    train_feature_3 = training_set[:,2]
    train_feature_4 = training_set[:,3]
    train_feature_5 = training_set[:,4]
    train_feature_6 = training_set[:,5]
    train_feature_7 = training_set[:,6]
    train_feature_8 = training_set[:,7]
    freq, border = np.histogram(train_feature_1,bins=49)
    freq, border = np.histogram(train_feature_1,bins=49)
    plt.plot(freq,border)
    plt.show()
    input()

if __name__ == '__main__':
    preprocesing()
    draw_PDF()
