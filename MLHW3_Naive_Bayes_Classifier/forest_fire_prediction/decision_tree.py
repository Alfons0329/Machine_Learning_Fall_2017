import preprocessing as pre #my module
from sklearn import tree

training_set, training_set_predicted, testing_set, testing_set_predicted = pre.preprocessing()
dt = tree.DecisionTreeClassifier()
decision_tree_classfier = dt.fit(training_set,training_set_predicted)

correct_prediction = 0
predicted_class_set = dt.predict(testing_set)
for i in range(len(testing_set)):
    original_class = testing_set_predicted[i]
    predicted_class = predicted_class_set[i]
    if(predicted_class == original_class):
        correct_prediction += 1
print("Decision Tree Classifier Accuracy:",float(correct_prediction)/float(len(testing_set)))
