import numpy as np
from sklearn import neighbors

"""
Preprocessing part credit to teammate lincw6666 by turning the discrete data into the continuous one for regressor

"""
MAKER = 0
MODEL = 1
TRANS = 6
FUEL  = 9

discrete_feature_name = ['maker', 'model', 'trans', 'fuel']
discrete_feature_pos = [ MAKER, MODEL, TRANS, FUEL ]
# function: getData
def getData(fp):
    return [ instance.split(',')[:] for instance in fp.read().split('\n')[:-1] ]

# function: getListFeature
def getListFeature(train_data, features):
    return [ list(set([ now[i] for now in train_data ])) for i in features ]

# function: getFeatureAvgPrice
def getFeatureAvgPrice(train_data, list_feature, features):
    # calculate average of price corresponding to maker, model, transmission, fuel type
    # init a 2d list
    print(train_data)
    print(list_feature)
    print(features)
    num_feature = [ [ 0.0 for data in list_feature[i] ] for i in range(len(list_feature)) ]
    avg_feature = [ [ 0.0 for data in list_feature[i] ] for i in range(len(list_feature)) ]
    for data in train_data:
        feature_id = [ list_feature[discrete_feature_pos.index(i)].index(data[i]) for i in features ]
        for i in range(len(num_feature)):
            num_feature[i][feature_id[i]] = num_feature[i][feature_id[i]] + 1.0
        for i in range(len(avg_feature)):
            avg_feature[i][feature_id[i]] = avg_feature[i][feature_id[i]] + float(data[len(data)-1])

    for i in range(len(avg_feature)):
        for j in range(len(avg_feature[i])):
            avg_feature[i][j] = avg_feature[i][j] / num_feature[i][j]

    return avg_feature

# function: sortFeatureAvgPrice
def sortFeatureAvgPrice(avg):
    val = []
    for j in range(len(avg)):
        val.append([ [i, avg[j][i]] for i in range(len(avg[j])) ])
    for i in range(len(val)):
        val[i] = sorted(val[i], key=lambda x: x[1])
    return val

# function: buildDiscreteFeatureVal
def buildDiscreteFeatureVal(train_data):
    # list all possible value of each feature
    list_feature = getListFeature(train_data, discrete_feature_pos)

    # calculate the average price for the corresponding feature
    avg_feature = getFeatureAvgPrice(train_data, list_feature, discrete_feature_pos)

    # the value of maker, transmission, fuel type is the corresponding average price
    tmp_val = sortFeatureAvgPrice(avg_feature)

    list_feature = [ [ list_feature[j][tmp_val[j][i][0]] for i in range(len(tmp_val[j])) ] for j in range(len(tmp_val)) ]
    val_feature = [ [ tmp_val[j][i][1] for i in range(len(tmp_val[j])) ] for j in range(len(tmp_val)) ]

    return list_feature, val_feature

# function: getDiscreteFeatureVal
def getDiscreteFeatureVal(val, list_feature, val_feature):
    if val not in list_feature:
        return float(float(len(list_feature))/2.0)
    return float(list_feature.index(val))

# function: preprocessing
def preprocessing(origin_data, list_feature, val_feature, discrete_features):
    target = []
    for data in origin_data:
        for i in range(len(data)):
            if i in discrete_features:
                feature_id = discrete_features.index(i)
                data[i] = getDiscreteFeatureVal(data[i], list_feature[feature_id], val_feature[feature_id])
            elif i == len(data)-1:
                target.append(float(data[i]))
                data.pop()
            else:
                data[i] = float(data[i])
    return origin_data, target

def KNN_regressor():

if __name__ == '__main__':
    fp_train = open("train.csv", "r")
    fp_test = open("test.csv", "r")
    # get training data
    train_data = getData(fp_train)
    list_feature, val_feature = buildDiscreteFeatureVal(train_data)
    train_data, train_target = preprocessing(train_data, list_feature, val_feature, discrete_feature_pos)
    # get testing data
    test_data = getData(fp_test)
    test_data, test_target = preprocessing(test_data, list_feature, val_feature, discrete_feature_pos)
