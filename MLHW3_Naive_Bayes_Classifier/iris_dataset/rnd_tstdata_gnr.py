import csv
import os
import sys
import math
import numpy as np
import random as rn
training_set = []
testing_set = []

def random_testdata_generator():
    all_data_name = sys.argv[1]
    output_train_filename = sys.argv[2]
    output_testing_filename = sys.argv[3]

    output_training_set = open(output_train_filename,'w')
    output_testing_set = open(output_testing_filename,'w')

    with open(all_data_name,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    rn.shuffle(all_data_list)
    for i in range(int(len(all_data_list)*0.7)): #split
        for j in range(len(all_data_list[i])):
            output_training_set.write(all_data_list[i][j])
            if(j != len(all_data_list[i])-1):
                output_training_set.write(',')
        output_training_set.write('\n')

    for i in range(len(all_data_list)-1,int(len(all_data_list)*0.7)-1,-1):
        for j in range(len(all_data_list[i])):
            output_testing_set.write(all_data_list[i][j])
            if(j != len(all_data_list[i])-1):
                output_testing_set.write(',')
        output_testing_set.write('\n')

    output_training_set.close()
    output_testing_set.close()

if __name__ == '__main__':
    random_testdata_generator()
