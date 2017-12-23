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
training_set_predicted_unlog = []
testing_set = []
testing_set_predicted = []
testing_set_predicted_unlog = []
def preprocessing():
    train_filename = sys.argv[1]
    testing_filename = sys.argv[2]
    global training_set
    global training_set_predicted
    global testing_set
    global testing_set_predicted
    global training_set_predicted_unlog
    global testing_set_predicted_unlog
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

        training_set_predicted_unlog.append(training_set[i][len(training_set[i])-1])
        if training_set[i][len(training_set[i])-1] != 0.0: #prevent log(0) math domain exception
            training_set[i][len(training_set[i])-1] = int(math.log10(training_set[i][len(training_set[i])-1]))
        else:
            training_set[i][len(training_set[i])-1] = int(training_set[i][len(training_set[i])-1])
            #logarithmic transformation of the last data, since it is quite skew

        training_set_predicted.append(training_set[i][len(training_set[i])-1])
        training_set[i] = training_set[i][4:12] #move the class away [4,12)

    for i in range(len(testing_set)):
        for j in range (4,len(testing_set[i])):
            testing_set[i][j] = float(testing_set[i][j])

        testing_set_predicted_unlog.append(testing_set[i][len(testing_set[i])-1])
        if testing_set[i][len(testing_set[i])-1] != 0.0: #prevent log(0) math domain exception
            testing_set[i][len(testing_set[i])-1] = int(math.log10(testing_set[i][len(testing_set[i])-1]))
        else:
            testing_set[i][len(testing_set[i])-1] = int(testing_set[i][len(testing_set[i])-1])
            #logarithmic transformation of the last data, since it is quite skew

        testing_set_predicted.append(testing_set[i][len(testing_set[i])-1])
        testing_set[i] = testing_set[i][4:12] #move the class away [4,12)

    return training_set, training_set_predicted, testing_set, testing_set_predicted, training_set_predicted_unlog, testing_set_predicted_unlog

def draw_PDF():
    global training_set
    #global training_set_predicted
    #global testing_set
    #global testing_set_predicted
    training_set = np.array(training_set)#temporary convert to numpy array for plotting the pdf

    plt.figure() #make an empty canvas
    #print(training_set_predicted)
    for i in range(0,8):
        tf = training_set[:,i]
        tf.sort()
        plt.subplot(2,4,i+1)
        weight_percent = np.ones_like(tf)/float(len(tf))
        if i == 7:
            plt.hist(tf, weights = weight_percent)
        else:
            plt.hist(tf, weights = weight_percent)

        plt.title(f' feature {i+1}: PDF')

    plt.tight_layout()
    plt.savefig("PDF.png",dpi=600)
    #plt.show()

if __name__ == '__main__':
    preprocessing()
    draw_PDF()
