#####################################################################
# Find KNN by calculating all distance from test data to train data #
#####################################################################
import sys
import time
DIMENSION = 9

# function: getClass
start_time = time.time()
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
		data[i].insert(0, i)	# id of data
		data[i][-1] = getClass(data[i][-1])
	return data


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

train_data = getData(fp_train)
test_data = getData(fp_test)
for K in [1, 5, 10, 100]:
	knn = [[], [], []]
	fp_ans.write('KNN K = ')
	fp_ans.write(str(K))
	fp_ans.write(':\n')
	for i in range(3):
		for data in train_data:
			dist = 0
			for j in range(1, DIMENSION+1):
				tmp = test_data[i][j] - data[j]
				dist  = dist + tmp*tmp
			knn[i].append([data[0], dist])
		knn[i] = sorted(knn[i], key = lambda x: x[1])[:100]
		for j in range(K):
			fp_ans.write(str(knn[i][j][0]))
			fp_ans.write(' ')
		fp_ans.write('\n')
	fp_ans.write('\n')



print("--- %s seconds ---" % (time.time() - start_time))
