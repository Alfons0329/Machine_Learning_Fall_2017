import preprocessing as pre #my module
import numpy as np
import math
from sklearn import tree

training_set, training_set_predicted, testing_set, testing_set_predicted, training_set_predicted_unlog, testing_set_predicted_unlog = pre.preprocessing()
#################################Decision tree classifier for discrete data#############################
dt = tree.DecisionTreeClassifier()
dt.fit(training_set,training_set_predicted)
#################################Decision tree regressor for continuous data#############################
training_set_predicted_unlog = np.array(training_set_predicted_unlog) #prevent unhashable error
dtr = tree.DecisionTreeRegressor() #using the default param setting will be fine
dtr.fit(training_set,training_set_predicted_unlog)
################################################dt classifier#############################################
correct_prediction = 0
predicted_class_set = dt.predict(testing_set)
for i in range(len(testing_set)):
    original_class = testing_set_predicted[i]
    predicted_class = predicted_class_set[i]
    if(predicted_class == original_class):
        correct_prediction += 1
print("Decision Tree Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))

################################################dt regressor#############################################
correct_prediction = 0
absolute_error = 0.0 #using the L2 norm space to calculating the error
predicted_class_set = dtr.predict(testing_set)
for i in range (len(testing_set)): #now the class become the continuous value
    #consider the continuous data
    original_class_cts = testing_set_predicted_unlog[i]
    predicted_class_cts = predicted_class_set[i]
    #consider the discrete data (transform from cts data back to the discrete one , which is class)
    original_class = testing_set_predicted[i]
    if(predicted_class_set[i]): #prevent math domain error of log 0
        predicted_class = int(math.log10(predicted_class_set[i]))
    else:
        predicted_class = predicted_class_set[i]

    if(predicted_class == original_class):
        correct_prediction += 1
    #print("original_class ",original_class_cts," predicted_class ",predicted_class_cts," original_class_cts ",original_class_cts," predicted_class_cts",predicted_class_cts)
    absolute_error += (original_class_cts - predicted_class_cts)*(original_class_cts - predicted_class_cts)

print("Decision Tree Regressor L2 Error:",float(correct_prediction)/float(len(testing_set)))
print("Decision Tree Regressor Accuracy(Converted to class using log10 base conversion):",float(correct_prediction)/float(len(testing_set)))

#############################################My notes here#################################################
"""
reference for criterion of the machine learning model
https://www.zhihu.com/question/21329754
"""
