"""
How to draw PDF?https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv
import sys
import math

def draw_PDF():
    all_data_name = sys.argv[1]
    with open(all_data_name,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    all_data_list = np.array(all_data_list)#temporary convert to numpy array for plotting the pdf
    feature_1 = all_data_list[:,4]
    feature_2 = all_data_list[:,5]
    feature_3 = all_data_list[:,6]
    feature_4 = all_data_list[:,7]
    feature_5 = all_data_list[:,8]
    feature_6 = all_data_list[:,9]
    feature_7 = all_data_list[:,10]
    feature_8 = all_data_list[:,11]

    predicted = all_data_list[:,12]
    print("feqture1 ",feature_1)
    freq, border = np.histogram(feature_1,bins=50)

    plt.title("Forestfire feature1: FFMC PDF")
    plt.plot(freq,border)
    plt.show()
    input()

if __name__ == '__main__':
    draw_PDF()
