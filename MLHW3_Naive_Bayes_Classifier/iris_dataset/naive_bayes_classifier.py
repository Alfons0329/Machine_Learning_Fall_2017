from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_iris
import csv
import os
import sys
import numpy as np
import scipy as sp
import random as rn

def preprocesing():
    train_filename = sys.argv[1]
    testing_set = []
    training_set = [] #primitive initialization
    with open(train_filename,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    #rn.shuffle(all_data_list)
    for i in range(int(len(all_data_list)*0.7)): #split
        print(i,all_data_list[i])
        training_set.append(all_data_list[i])

    print('Testing set \n')
    for i in range(len(all_data_list)-1,int(len(all_data_list)*0.7),-1):
        print(i,all_data_list[i])
        testing_set.append(all_data_list[i])

    return training_set, testing_set;
if __name__ == '__main__':
    preprocesing();
