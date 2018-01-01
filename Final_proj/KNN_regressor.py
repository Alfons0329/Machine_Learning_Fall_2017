import numpy as np
import sklearn.neighbors as sknn
import matplotlib.pyplot as plt
import scipy.stats as stat
import math
"""
Preprocessing part credit to teammate lincw6666 by turning the discrete data into the continuous one for regressor,
thanks to him for his great work :)
KNN Regressor by myself

Further discussion--> the preprocessed data-->fit into normal distribution and remove +-3stddevc data?
"""
#Define the max neighbor count
neighbor_cnt_arr = [1,2]#,5,10,20,50,100]
MAX_NEIGHBOR_CNT = 5
PERMITTED_ERR_RANGE = 500
#Column pos in the original train dataset for the continuous data
continuous_feature_pos = [2,3,4,5]
x_axis_nei_cnt = [] #The x-axis of the plotting dataset
y_axis_acc_cnt = [] #The y-axis of the plotting dataset
#Column pos in the original train dataset for the discrete data
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
    #Discrete feature pos 0,1,6,9
    #Concanete the each row's row train_data[row][0] [1] [6] [9]--->use the set
    return [ list(set([ now[i] for now in train_data ])) for i in features ]

# function: getFeatureAvgPrice
def getFeatureAvgPrice(train_data, list_feature, features):
    # calculate average of price corresponding to maker, model, transmission, fuel type
    # init a 2d list num_feature calculate how many object in that feature corresponding to each member
    num_feature = [ [ 0.0 for data in list_feature[i] ] for i in range(len(list_feature)) ]
    avg_feature = [ [ 0.0 for data in list_feature[i] ] for i in range(len(list_feature)) ]
    for data in train_data:
        #Get the correspoding feature ID according to discrete_feature_name = ['maker', 'model', 'trans', 'fuel'], which is for i in features
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

def extremity_optimization(train_data, train_target):
    stddev_arr = [0.0 for i in range(10) ]
    mean_arr = [0.0 for i in range(10) ]
    optimized_train_data = []
    optimized_train_target = []
    range_satisfied = 1
    train_data = np.array(train_data)
    for i in continuous_feature_pos:
        stddev_arr[i] = (np.std(train_data[:,i]))
        mean_arr[i] = (np.mean(train_data[:,i]))

    train_data.tolist()
    #only push the data where the cts data all satisfied the normal distribution
    for train_data_iter in range(len(train_data)):
        for i in continuous_feature_pos:
            if train_data[train_data_iter][i] < mean_arr[i] - 3*stddev_arr[i] or train_data[train_data_iter][i] > mean_arr[i] + 3*stddev_arr[i]: #Check the range
                range_satisfied = 0
        if range_satisfied == 1:
            optimized_train_data.append(train_data[train_data_iter])
            optimized_train_target.append(train_target[train_data_iter])

    return optimized_train_data, optimized_train_target

def correlation_optimization(train_data, train_target):
    return optimized_train_data, optimized_train_target

def KNN_core(train_data, train_target, test_data, test_target):
    #Plotting the graph of N-Neighbor vs Accuracy
    tmp_x = []
    tmp_y = []
    global x_axis_nei_cnt
    global y_axis_acc_cnt

    for neighbor_cnt in neighbor_cnt_arr: #range(2,MAX_NEIGHBOR_CNT+1):
        regr = sknn.KNeighborsRegressor(n_neighbors = neighbor_cnt)
        regr.fit(train_data, train_target)
        predicted_result = regr.predict(test_data)
        #Check the absolute error by calculating the abs(real_price eur - predict_price eur)
        #The predicted result is the continuous data
        #print(predicted_result)
        #input()
        tmp_x.append(neighbor_cnt)
        permitted_error_satisfied_cnt = 0
        for i in range(len(predicted_result)):
            absolute_error = abs(predicted_result[i] - test_target[i])
            if absolute_error <= PERMITTED_ERR_RANGE:
                permitted_error_satisfied_cnt+=1

        tmp_y.append(float(permitted_error_satisfied_cnt)/float(len(test_target)))
        print("KNN with K= ",neighbor_cnt," There is ",float(permitted_error_satisfied_cnt)/float(len(test_target))," that the predict price is within 1000 eur of actual price")

    x_axis_nei_cnt.append(tmp_x)
    y_axis_acc_cnt.append(tmp_y)

def plot_all_result():
    global x_axis_nei_cnt
    global y_axis_acc_cnt

    for i in range(len(x_axis_nei_cnt)):
        print(x_axis_nei_cnt[i], y_axis_nei_cnt[i])
        plt.plot(x_axis_nei_cnt[i], y_axis_nei_cnt[i])

    plt.savefig("KNN_result.png",dpi=600)

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
    KNN_core(train_data, train_target, test_data, test_target)
    #Do the optimization~ filter the extermity
    optimized_train_data, optimized_train_target = extremity_optimization(train_data, train_target)
    KNN_core(optimized_train_data, optimized_train_target, test_data, test_target)

    plot_all_result()
    #Do the optimization~ leave the required column only
