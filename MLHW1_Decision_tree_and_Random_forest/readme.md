# Introduction to Machine Learning Project 1 - Decision Tree and Random Forest
## Build environment
* Ubuntu 16.04 LTS 64bit
* g++ -std=c++11(see shell file)
* Written in c++
* Debug using valgrind
## What is Decision Tree and Random Forest
https://en.wikipedia.org/wiki/Decision_tree < /br>
https://en.wikipedia.org/wiki/Random_forest < /br>
## How decision tree is built
* Normal Decision Tree< /br>
0.Store the data into the set of vector< /br>
1.Back up the original classfication table in the aux table< /br>
2.Sort according to the attribute (dosent matter which attribute will get the most information gain sinc the  )< /br>
3.If different at index then we calculate at (or say split with (value[index]+value[index-1])/2)< /br>
4.Now the table has been splitted into 2 parts, then calcculate according to the ID3 algorithm< /br>
5.We have left_child and right_child So we split , new* left_child right child, connect them parent->newchild= something< /br>
6.take the needed data into leftchild which for example <180cm , then take all the person whose height <180cm into left child< /br>
7.If the node's data is homogenous, stop< /br>
8.the recursive algorithm is somehow like build_decision_tree(node* left_child) build_decision_tree(node* right_child) where the child is not null< /br>

Q:Which attribute to split first?< /br>
A:Doesnt matter, what matters is the boundary we split, the boundary has to bring us the most information gain< /br>
< /br>
* Extend the idea to Random Forest< /br>
0.Build an amount of decision tree, each time pick different N attribute where N<total attribute< /br>
1.Select the training data to build some amount of tree depend on the combinations of attributes selected< /br>
2.Traverse the forest, the highest vote for the predicted class is the< /br>
3.K Fold Cross validation still implementable< /br>
## How to valgrind?
* Install
```
$ sudo apt-get install valgrind
```
```
$ valgrind ./your_executable_file
```
## Shell script in bash  
* Make them executable
```
$ chmod+x run.sh && chmod+x RF.sh
```
* Run (build included in the )
```
$ ./run.sh && ./RF.sh
```
