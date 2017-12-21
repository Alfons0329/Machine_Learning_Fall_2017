"""
How to draw PDF?https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html
"""
import numpy as np
import scipy as sp
import scipy.stats as stats
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

    fid = plt.figure()
    train_feature_1 = training_set[:,0]
    train_feature_1.sort()
    plt.title("Forestfire feature 1: FFMC Probability Distribution Function")
    train_mean = np.mean(train_feature_1)
    train_std = np.std(train_feature_1)
    pdf = stats.norm.pdf(train_feature_1,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_1,pdf) #x axis `y axis
    plt.show()
    input()
    train_feature_2 = training_set[:,1]
    plt.title("Forestfire feature 2: DMC Probability Distribution Function")
    train_mean = np.mean(train_feature_2)
    train_std = np.std(train_feature_2)
    pdf = stats.norm.pdf(train_feature_2,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_2,pdf) #x axis y axis

    train_feature_3 = training_set[:,2]
    plt.title("Forestfire feature 2: DC Probability Distribution Function")
    train_mean = np.mean(train_feature_3)
    train_std = np.std(train_feature_3)
    pdf = stats.norm.pdf(train_feature_3,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_3,pdf) #x axis y axis

    train_feature_4 = training_set[:,3]
    plt.title("Forestfire feature 3: ISI Probability Distribution Function")
    train_mean = np.mean(train_feature_4)
    train_std = np.std(train_feature_4)
    pdf = stats.norm.pdf(train_feature_4,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_4,pdf) #x axis y axis

    train_feature_5 = training_set[:,4]
    plt.title("Forestfire feature 4: temp Probability Distribution Function")
    train_mean = np.mean(train_feature_5)
    train_std = np.std(train_feature_5)
    pdf = stats.norm.pdf(train_feature_5,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_5,pdf) #x axis y axis

    train_feature_6 = training_set[:,5]
    plt.title("Forestfire feature 5: RH Probability Distribution Function")
    train_mean = np.mean(train_feature_6)
    train_std = np.std(train_feature_6)
    pdf = stats.norm.pdf(train_feature_6,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_6,pdf) #x axis y axis

    train_feature_7 = training_set[:,6]
    plt.title("Forestfire feature 6: wind Probability Distribution Function")
    train_mean = np.mean(train_feature_7)
    train_std = np.std(train_feature_7)
    pdf = stats.norm.pdf(train_feature_7,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_7,pdf) #x axis y axis

    train_feature_8 = training_set[:,7]
    plt.title("Forestfire feature 8: rain Probability Distribution Function")
    train_mean = np.mean(train_feature_8)
    train_std = np.std(train_feature_8)
    pdf = stats.norm.pdf(train_feature_8,train_mean,train_std) #use the scipy pdf function to show it
    plt.plot(train_feature_8,pdf) #x axis y axis

    plt.show()
    input()

if __name__ == '__main__':
    preprocesing()
    draw_PDF()
