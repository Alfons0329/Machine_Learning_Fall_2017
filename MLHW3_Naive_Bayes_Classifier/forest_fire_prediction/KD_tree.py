import preprocessing as pre #my module
import sklearn.neighbors as sknn
import numpy as np
training_set, training_set_predicted, testing_set, testing_set_predicted, training_set_predicted_unlog, testing_set_predicted_unlog = pre.preprocessing()
tree = sknn.KDTree(training_set)
correct_prediction = 0
dist, nearest_index = tree.query(testing_set, k=2)#other than itself
nearest_index = nearest_index.tolist() #not in place, re-assign
for i in range(len(testing_set)):
    original_class = testing_set_predicted[i]
    predicted_class = training_set_predicted[nearest_index[i][0]]
    if(predicted_class == original_class):
        correct_prediction += 1

print("KD Tree Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))

"""
KDTree api reference
http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree

"""
