import csv
import numpy
try:
	fp_train = open("train.csv", "r")
except(IOError):
	print('Error: "train.csv" not found!!\n')
	sys.exit()
try:
	fp_test = open("test.csv", "r")
except(IOError):
	print('Error: "test.csv" not found!!\n')
	sys.exit()
try:
	fp_ans = open("answer.txt", "w")
except(IOError):
	print('Error: can\'t open "answer.txt"!!\n')
	sys.exit()


def fileparsing():
    with open('train.csv','r') as opened_file : #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    for i in range(1,len(all_data_list)):
        for j in range(2,11):
            all_data_list[i][j]=float(all_data_list[i][j])
            print(type(all_data_list[i][j]))

    return all_data_list
    #print(all_data_list)
def
