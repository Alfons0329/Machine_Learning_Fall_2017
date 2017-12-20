import sys

# define value
DIMENSION = 9
CLASS_NUM = 8
TRAIN_DATA_SIZE = 300
TEST_DATA_SIZE = 36
KNN_NEED_TO_PRINT = 3

"""**************************************************************************
* 			 					 Structure									*
**************************************************************************"""
# structure: Node -> Node in the KDtree
class Node:
	def __init__(self, split_dim, value, node_id):
		self.split_dim = split_dim	# use which dimension to split the data
		self.value = value			# if >= value, then goto right child; else, goto left child
		self.id = node_id			# id of the instance
		self.parent = None
		self.left = None
		self.right = None

# structure: NearestNeighbor
class NearestNeighbot:
	def __init__(self, nn_id, distance):
		self.id = nn_id
		self.distance = distance


"""**************************************************************************
* 			 					 Function									*
**************************************************************************"""
# function: buildTree -> Build a KDtree
def buildTree(node, data, now_dim):
	# sort data by dimension 'now_dim'
	data = sorted(data, key = lambda x : x[now_dim])
	# find the middle instance to be a node
	middle = int(len(data)/2)
	node = Node(now_dim, data[middle][now_dim], data[middle][0])
	# split data, create child
	print(node.id)
	#input()
	if len(data) == 1:
		return node
	if now_dim == DIMENSION:
		now_dim = 1
	else:
		now_dim = now_dim + 1
	if middle > 0:
		node.left = buildTree(None, data[:middle], now_dim)
		node.left.parent = node
	if middle < len(data)-1:
		node.right = buildTree(None, data[middle+1:], now_dim)
		node.right.parent = node
	return node

def tree_traverse_check(current_kd_node,cnt):
    print ("Current point ",current_kd_node.id,"Split with ",current_kd_node.split_dim)

    if current_kd_node.left:
        tree_traverse_check(current_kd_node.left,cnt+1)
    if current_kd_node.right:
        tree_traverse_check(current_kd_node.right,cnt+1)

# function: descendTree -> put the data into the KDtree
def descendTree(node, data):
	if data[node.split_dim] < node.value:
		if node.left == None:
			return node
		else:
			return descendTree(node.left, data)
	else:
		if node.right == None:
			return node
		else:
			return descendTree(node.right, data)


# function:	updateKnn
def updateKnn(knn, distance, now_node):
	if [now_node.id, distance] in knn:
		return knn
	elif len(knn) == 0:
		knn.append([now_node.id, distance])
	elif len(knn) < K:
		knn.append([now_node.id, distance])
		knn = sorted(knn, key = lambda x: x[1])
	elif distance < knn[-1][1]:
		knn.append([now_node.id, distance])
		knn = sorted(knn, key = lambda x: x[1])
		# delete nodes that are not K nearest neighbors
		tmp = len(knn)
		if tmp-K > 0:
			for i in range(tmp-K):
				if knn[tmp-i-1][1] > knn[K-1][1]:
					del knn[tmp-i-1]
	elif distance == knn[-1][1]:
		knn.append([now_node.id, distance])
	return knn


# function: euclidDist
def euclidDist(a, b):
	tmp = [a[i]-b[i] for i in range(1, DIMENSION+1)]
	dist = 0
	for x in tmp:
		dist = dist + x*x
	return dist


# function: innerProduct
def innerProduct(a, b):
	tmp = 0
	for i in range(1, DIMENSION+1):
		tmp = tmp + a[i]*b[i]
	return tmp


# function: boundaryDist -> the distance between the query and the hyperplane of now_node
def boundaryDist(a, b, split_dim):
	return (a[split_dim]-b[split_dim]) * (a[split_dim]-b[split_dim])

# function: predictTestData -> put the test data into KDtree, return the list of nearest neighbors
def predictTestData(root, data, K):
	knn = []		# knn[0] for id, knn[1] for distance
	pre_node = Node(1, 2, 3)
	now_node = descendTree(root, data)
	while now_node != None:
		distance = euclidDist(data, train_data[now_node.id])
		# update knn
		knn = updateKnn(knn, distance, now_node)
		# decide next node to go
		if now_node.left == None and now_node.right == None:	# leaf node
			pre_node = now_node
			now_node = now_node.parent
		elif boundaryDist(data, train_data[now_node.id], now_node.split_dim) < knn[-1][1] or len(knn) < K:
			if data[now_node.split_dim] < now_node.value:
				if now_node.right == None or now_node.right == pre_node:
					pre_node = now_node
					now_node = now_node.parent
				else:
					pre_node = now_node
					now_node = descendTree(now_node.right, data)
			else:
				if now_node.left == None or now_node.left == pre_node:
					pre_node = now_node
					now_node = now_node.parent
				else:
					pre_node = now_node
					now_node = descendTree(now_node.left, data)
		else:
			pre_node = now_node
			now_node = now_node.parent
	return knn


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
		data[i].insert(0, i)	# id of data
		data[i][-1] = getClass(data[i][-1])
	return data

"""**************************************************************************
*																			*
* 			 				  	    Main 								    *
*																			*
**************************************************************************"""
############################## Get Data #####################################
# open file
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
	fp_out = open("output.txt", "w")
except(IOError):
	print('Error: can\'t open "output.txt"!!\n')
	sys.exit()

train_data = getData(fp_train)
test_data = getData(fp_test)

if not fp_train.closed:
	fp_train.close()
if not fp_test.closed:
	fp_test.close()

############################# Build Tree ####################################
root = buildTree(None, train_data, 1)
tree_traverse_check(root,0)
############################# Test Data #####################################
# KNN-classifier, K = 1, 5, 10, 100
best_k = 0
best_accu = 0
for K in [1, 5, 10, 100]:
	accuracy = 0
	knn_output = []
	for now in range(len(test_data)):
		knn = predictTestData(root, test_data[now], K)
		# add knn for the first three test data
		if now < KNN_NEED_TO_PRINT:
			knn_output.append([i[0] for i in knn])
		# check the prediction is correct or not
		predict = [0 for i in range(CLASS_NUM)]
		for i in range(len(knn)):
			predict[train_data[knn[i][0]][-1]] = predict[train_data[knn[i][0]][-1]] + 1
		if test_data[now][-1] == predict.index(max(predict)):
			accuracy = accuracy + 1

	if float(accuracy)/float(len(test_data)) > best_accu:
		best_accu = float(accuracy)/float(len(test_data))
		best_k = K
	# print result and K nearest neighbots
	fp_out.write('KNN accuracy: ')
	fp_out.write('%.6f'%(float(accuracy)/float(len(test_data))))
	fp_out.write('\n')
	for i in range(KNN_NEED_TO_PRINT):
		for j in range(K):
			fp_out.write(str(knn_output[i][j]))
			fp_out.write(' ')
		fp_out.write('\n')
	fp_out.write('\n')

print(best_k, best_accu)
