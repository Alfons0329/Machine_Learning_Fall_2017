# Introduction to Machine Learning Project 1 - Decision Tree and Random Forest
## Build environment
* Ubuntu 16.04 LTS 64bit
* g++ -std=c++11(see shell file)
* Written in c++
* Debug using valgrind
## What is Decision Tree and Random Forest
https://en.wikipedia.org/wiki/Decision_tree <br />
https://en.wikipedia.org/wiki/Random_forest <br />
## How decision tree is built
* Normal Decision Tree<br />
0.Store the data into the set of vector  
1.Sort according to the attribute (dose not matter which attribute will get the most information gain since all splitting and attribute will be calculated)<br />
2.If different at index then we calculate at (or say split with (value[index]+value[index-1])/2)<br />
3.Now the table has been split into 2 parts, then calculate “each splitting point”according to the ID3 algorithm
By using the std::map, we will increase the convenience to make a statistics of dataset.
After calculating the position of splitting with LEAST ENTROPY , which means the “chaos” of data is the LEAST, then we split at such position to reduce the data inconsistency.<br />
4.We now have left_child and right_child. We split ,and  new* left_child right child, connect them parent->newchild= something<br />
5.take the needed data into leftchild which for example <180cm , then take all the person whose height <180cm into left child and vice versa for splitting the data set according to the current criterium.<br />
6.If the node's data is homogeneous, stop (the node cannot be split even more).
7.the recursive algorithm is somehow like build_decision_tree(node* left_child) build_decision_tree(node* right_child) where the child is not null<br />
Q:Which attribute to split first?
A:Doesnt matter, what matters is the boundary we split, the boundary has to bring us the most information gain

* Extend the idea to Random Forest<br />
0.Build 5 decision tree where data picked from the data which require 120 training sets<br />
1.Each tree contains 96 datasets, reason is that 120/24=5 and 120-24=96, just like the K-Fold interval for one decision tree, but now we have the subinterval for 5 trees and 24 as a count number for interval.<br />
2.Traverse the forest, the highest vote for the predicted class is the.<br />
3.K Fold Cross validation still implementable.<br />
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
