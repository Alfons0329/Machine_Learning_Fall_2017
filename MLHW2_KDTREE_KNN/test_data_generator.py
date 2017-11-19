import sys
import random
import numpy as np
from sklearn.tree import DecisionTreeRegressor

TRAIN_DATA_SIZE = 300
GEN_DATA_NUM = 36  	# the numbers of data we generate
DIMENSION = 9


# function: turnClass
def turnClass(num):
	return {
		0: 'cp',
		1: 'im',
		2: 'pp',
		3: 'imU',
		4: 'om',
		5: 'omL',
		6: 'imL',
		7: 'imS'
	}[num]


# function: getClass
def getClass(string):
	return {
		'cp': 0,
		'im': 1,
		'pp': 2,
		'imU': 3,
		'om': 4,
		'omL': 5,
		'imL': 6,
		'imS': 7
	}[string]


# function: getData
def getData(fp):
	# get instances
	data = [instance.split(',')[2:] for instance in fp.read().split('\n')[1:-1]]
	# convert values in data from string to float
	for i in range(len(data)):
		for j in range(DIMENSION):
			data[i][j] = float(data[i][j])
		# data[i].insert(0, i)	# id of data
		data[i][-1] = getClass(data[i][-1])
	return data


# get trainning data
try:
	fp_train = open("train.csv", "r")
except(IOError):
	print('Error: "train.csv" not found!!\n')
	sys.exit()

tmp = getData(fp_train)
train_data = []
train_result = []
for i in range(len(tmp)):
	train_data.append(tmp[i][:-1])
	train_result.append([tmp[i][-1]])

if not fp_train.closed:
	fp_train.close()

# generate 36 instances with 9 dimension random data
rand_data = []
for i in range(GEN_DATA_NUM):
	tmp = []
	for dim in range(DIMENSION):
		tmp.append(train_data[random.randint(0, TRAIN_DATA_SIZE-1)][dim])
	rand_data.append(tmp)

# predict rand_data belongs to which class
decision_tree = DecisionTreeRegressor()
decision_tree.fit(train_data, train_result)
result = decision_tree.predict(rand_data)

# output the test data to test.csv
try:
	fp_test = open("test.csv", "w")
except(IOError):
	print('Error: can\'t open "test.csv"!!\n')
	sys.exit()

for i in range(len(rand_data)):
	rand_data[i].insert(0, i)
	rand_data[i].insert(1, 'asdf')
	for j in range(len(rand_data[i])):
		fp_test.write(str(rand_data[i][j]))
		fp_test.write(',')
	fp_test.write(turnClass(result[i]))
	fp_test.write('\n')
