import preprocessing as pre #my module
import sklearn.neighbors as sknn
import numpy as np
import math
training_set, training_set_predicted, testing_set, testing_set_predicted, training_set_predicted_unlog, testing_set_predicted_unlog = pre.preprocessing()
################################################NN classifier#############################################
tree = sknn.KDTree(training_set)
correct_prediction = 0
dist, nearest_index = tree.query(testing_set, k=2)#other than itself
nearest_index = nearest_index.tolist() #not in place, re-assign
for i in range(len(testing_set)):
    original_class = testing_set_predicted[i]
    predicted_class = training_set_predicted[nearest_index[i][0]]
    if(predicted_class == original_class):
        correct_prediction += 1

print("KNN Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))

################################################NN regressor#############################################
training_set_predicted_unlog = np.array(training_set_predicted_unlog)
regr = sknn.KNeighborsRegressor(n_neighbors = 2) #other than itself
regr.fit(training_set, training_set_predicted_unlog)
correct_prediction = 0
absolute_error = 0.0
predicted_class_set = regr.predict(testing_set)
for i in range(len(testing_set)):
    #consider the continuous data
    original_class_cts = testing_set_predicted_unlog[i]
    predicted_class_cts = predicted_class_set[i]
    #consider the discrete data (transform from cts data back to the discrete one , which is class)
    original_class = testing_set_predicted[i]
    if predicted_class_set[i] != 0.0: #prevent math domain error of log 0
        #print("original",predicted_class_set[i],"log10 tf",math.log10(predicted_class_set[i]))
        predicted_class = int(math.log10(predicted_class_set[i]))
    else:
        predicted_class = int(predicted_class_set[i])

    if(predicted_class == original_class):
        correct_prediction += 1

    #print("original_class ",original_class," predicted_class (by log10 transform) ",predicted_class," original_class_cts ",original_class_cts," predicted_class_cts",predicted_class_cts)
    absolute_error += (original_class_cts - predicted_class_cts)*(original_class_cts - predicted_class_cts)

print("NN Regressor L2-Norm Error:",absolute_error)
print("NN Regressor Accuracy(Converted to class using log10 base conversion):",float(correct_prediction)/float(len(testing_set)))

"""
KDTree api reference
http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree
"""
