import naive_bayes_classifier as nbc#my module
import sklearn.neighbors as sknn
import numpy as np
training_set, training_set_predicted, testing_set, testing_set_predicted = nbc.preprocessing()
tree = sknn.KDTree(training_set)
correct_prediction = 0
dist, nearest_index = tree.query(testing_set, k=2)#other than itself
nearest_index = nearest_index.tolist() #not in place, re-assign
for i in range(len(testing_set)):
    original_class = testing_set_predicted[i]
    """
    #####################################################################################################################
    NOTE!!! SEGMENTATION FAULT WILL HAPPEN HERE!!!
    THE QUERY RESULT SHOULD ACQUIRE FROM
    training_set_predicted[nearest_index[i][0]]
    RATHER THAN
    testing_setd[nearest_index[i][0]]
    reason is that since the KNN Algorithm search the nearest neighbors,
    we build the KDTree from training_set and validate from testing_set, they are mutually exclusive
    suppose the NN is in training_set rather than the testing_set, acquire the NN using nearest_index from
    training_set, where size is out of that of the testing_set, it definitely triggers SIGSEGV!
    ######################################################################################################################
    """
    predicted_class = training_set_predicted[nearest_index[i][0]]
    #print("testing set",i," ",testing_set[i],"original_class ",original_class,"predicted_class",predicted_class)
    if(predicted_class == original_class):
        correct_prediction += 1

print("KD Tree Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))

"""
KDTree api reference
http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree

"""
