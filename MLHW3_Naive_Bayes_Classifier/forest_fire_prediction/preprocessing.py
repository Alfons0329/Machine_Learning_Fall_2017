"""
How to draw PDF?https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html
Subplot reference to http://noahsnail.com/2017/05/03/2017-5-3-matplotlib%E7%9A%84%E5%9F%BA%E6%9C%AC%E7%94%A8%E6%B3%95(%E5%8D%81%E4%BA%8C)%E2%80%94%E2%80%94subplot%E7%BB%98%E5%88%B6%E5%A4%9A%E5%9B%BE/

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

    plt.figure() #make an empty canvas

    train_feature_1 = training_set[:,0]
    train_feature_1.sort()
    plt.title(" feature 1: FFMC PDF")
    train_mean = np.mean(train_feature_1)
    train_std = np.std(train_feature_1)
    pdf = stats.norm.pdf(train_feature_1,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,1)
    plt.plot(train_feature_1,pdf) #x axis `y axis

    train_feature_2 = training_set[:,1]
    train_feature_2.sort()
    plt.title(" feature 2: DMC PDF")
    train_mean = np.mean(train_feature_2)
    train_std = np.std(train_feature_2)
    pdf = stats.norm.pdf(train_feature_2,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,2)
    plt.plot(train_feature_2,pdf) #x axis y axis

    train_feature_3 = training_set[:,2]
    train_feature_3.sort()
    plt.title(" feature 3: DC PDF")
    train_mean = np.mean(train_feature_3)
    train_std = np.std(train_feature_3)
    pdf = stats.norm.pdf(train_feature_3,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,3)
    plt.plot(train_feature_3,pdf) #x axis y axis

    train_feature_4 = training_set[:,3]
    train_feature_4.sort()
    plt.title(" feature 4: ISI PDF")
    train_mean = np.mean(train_feature_4)
    train_std = np.std(train_feature_4)
    pdf = stats.norm.pdf(train_feature_4,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,4)
    plt.plot(train_feature_4,pdf) #x axis y axis

    train_feature_5 = training_set[:,4]
    train_feature_5.sort()
    plt.title(" feature 5: temp PDF")
    train_mean = np.mean(train_feature_5)
    train_std = np.std(train_feature_5)
    pdf = stats.norm.pdf(train_feature_5,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,5)
    plt.plot(train_feature_5,pdf) #x axis y axis

    train_feature_6 = training_set[:,5]
    train_feature_6.sort()
    plt.title(" feature6: RH PDF")
    train_mean = np.mean(train_feature_6)
    train_std = np.std(train_feature_6)
    pdf = stats.norm.pdf(train_feature_6,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,6)
    plt.plot(train_feature_6,pdf) #x axis y axis

    train_feature_7 = training_set[:,6]
    train_feature_7.sort()
    plt.title(" feature 7: wind PDF")
    train_mean = np.mean(train_feature_7)
    train_std = np.std(train_feature_7)
    pdf = stats.norm.pdf(train_feature_7,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,7)
    plt.plot(train_feature_7,pdf) #x axis y axis

    train_feature_8 = training_set[:,7]
    train_feature_8.sort()
    plt.title(" feature 8: rain PDF")
    train_mean = np.mean(train_feature_8)
    train_std = np.std(train_feature_8)
    pdf = stats.norm.pdf(train_feature_8,train_mean,train_std) #use the scipy pdf function to show it
    plt.subplot(2,4,8)
    plt.plot(train_feature_8,pdf) #x axis y axis

    plt.show()

if __name__ == '__main__':
    preprocesing()
    draw_PDF()
