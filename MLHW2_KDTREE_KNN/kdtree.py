import csv
import numpy as np

def fileparsing():
    with open('train.csv','r') as opened_file : #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    return all_data_list
    #print(all_data_list)

def append_knnquery_boolean(all_data_list):
    for i in range(0,len(all_data_list)):
        all_data_list[i].append('false')

    print(all_data_list)

def create_kd_tree(root,node_data_set):
     node_data_len = len(node_data_set)

     if node_data_len == 0:
        return

     dimension = len (node_data_set[0]-3)

     max_var = 0

     split_attribute = 0;

     for i in range(2,10):
        column_calculate = [] #empty

        for j in node_data_set:
            column_calculate.append(j[i])

        max_var = calculate_variance ();

     return root

def calculate_variance(node_data_set):
    numpy.list
    return variance


if __name__ == "__main__":
    training_set = fileparsing()
    training_set = training_set[1:len(training_set)] #remove the first one
    append_knnquery_boolean(training_set)
