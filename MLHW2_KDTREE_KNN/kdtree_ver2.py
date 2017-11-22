import csv
import numpy as np
import os
import pprint
import math
class kd_node:
    def __init__(self ,point = None, split = None, left_child_init = None, right_child_init = None, knn_traversed_init = False): #default constructor of the class
        self.point = point #dat a point
        self.split = split
        self.left_child = left_child_init
        self.right_child = right_child_init
        self.parent = None
        self.knn_traversed = knn_traversed_init

def fileparsing():
    with open('train.csv','r') as opened_file : #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    for i in range(1,len(all_data_list)):
        for j in range(2,11):
            all_data_list[i][j]=float(all_data_list[i][j])

    return all_data_list

def append_knnquery_boolean(all_data_list):
    for i in range(0,len(all_data_list)):
        all_data_list[i].append('false')

def create_kd_tree(root,node_data_set,split_attribute):
    node_data_len = len(node_data_set)
    median_index = int(len(node_data_set)/2)
    node_data_set.sort(key=lambda x:x[split_attribute])
    point = node_data_set[median_index]
    root =  kd_node(point,split_attribute)

    if node_data_len ==1: #build over
        print("Leaf ",root.point[0], " split ",root.split)
        return root

    if split_attribute == 10:
        split_attribute = 2
    else:
        split_attribute += 1

    if median_index > 0:
        root.left_child = create_kd_tree(root.left_child, node_data_set[:median_index],split_attribute)
        root.left_child.parent = root
    if median_index < len(node_data_set)-1:
        root.right_child = create_kd_tree(root.right_child, node_data_set[median_index+1:],split_attribute)
        root.right_child.parent = root

    return root

def tree_traverse_check(current_kd_node,cnt):
    current_kd_node.knn_traversed = False
    #print("traversed ID ",current_kd_node.point[0]," split ",current_kd_node.split)
    if current_kd_node.left_child:
        tree_traverse_check(current_kd_node.left_child,cnt+1)
    if current_kd_node.right_child:
        tree_traverse_check(current_kd_node.right_child,cnt+1)

def validate(root,training_set):
    validation_set = []
    for i in range(0,36):
        validation_set.append(training_set[i])
    #what to output
    output_file = open('result.txt','w') #Write mode
    #integer declaration
    predicted_correct = 0
    #string class declaration
    original_class = None
    final_predicted_class = None
    #hashmap declaration for voting system
    knn_result_hash = {'cp':0,'im':0,'pp':0,'imU':0,'om':0,'omL':0,'imL':0,'imS':0}
    classname_set = ['cp','im','pp','imU','om','omL','imL','imS']
    #KNN main core
    first_three_output = [[] for i in range(3)]
    for knn_query in [1,5]:
        first_three_output = [[] for i in range(3)]
        predicted_correct += 1
        for query_index in range(0,3):
            query_point = validation_set[query_index] #take the point for querying
            original_class = query_point[11]
            for search_hash in range(len(classname_set)): #clear the hash map for the query from each point for voting
                knn_result_hash[classname_set[search_hash]] = 0

            tree_traverse_check(root,0) #clear all traversed mark to false first,which symbolized non traversed
            for individual_knn_query in range(0,knn_query):
                print("query_point ",query_point[0]," knn now " ,individual_knn_query)
                NN,predicted_class = KNN_core(root,query_point)
                knn_result_hash[predicted_class] += 1
                if(query_index >=0 and query_index<3): #outputresult
                    first_three_output[query_index].append(NN)
            #input()
            max_voted_class = 0
            for search_hash in range(len(classname_set)): #voting for the best result
                if knn_result_hash[classname_set[search_hash]] > max_voted_class:
                    max_voted_class = knn_result_hash[classname_set[search_hash]]
                    final_predicted_class = classname_set[search_hash]
            print("Original ",original_class," predicted class",final_predicted_class)
            if(original_class == final_predicted_class):
                print("Predicted correct ")
                predicted_correct+=1
            ###input
        print("A KNN Is end ",query_index,"Acc is ",float(predicted_correct)/36.0)
        print('\n'+'\n'+'\n'+'\n'+'\n')
        output_file.write('KNN accuracy: '+str(float(predicted_correct)/36.0)+'\n')
        for output_index in range(len(first_three_output[0])):
            output_file.write(first_three_output[0][output_index]+' ')
        output_file.write('\n')
        for output_index in range(len(first_three_output[1])):
            output_file.write(first_three_output[1][output_index]+' ')
        output_file.write('\n')
        for output_index in range(len(first_three_output[2])):
            output_file.write(first_three_output[2][output_index]+' ')
        output_file.write('\n')

        output_file.write('\n')

    output_file.close()
def binarysearch(cur_point,query_point):
	if query_point[cur_point.split] < cur_point.point[cur_point.split]:
		if cur_point.left_child == None:
			return cur_point
		else:
			return binarysearch(cur_point.left_child, query_point)
	else:
		if cur_point.right_child == None:
			return cur_point
		else:
			return binarysearch(cur_point.right_child, query_point)

def KNN_core(root,query_point):

    pre_point = kd_node(2,3)
    cur_point = binarysearch(root,query_point)
    nearest = None
    while cur_point != None:
        min_dist = calculaue_distance(query_point,cur_point.point)
        nearest = cur_point
        if cur_point.left_child == None and cur_point.right_child == None: #Leaf node, trace back ascend
            pre_point = cur_point
            cur_point = cur_point.parent
            nearest = cur_point
        elif abs(query_point[cur_point.split] - cur_point.point[cur_point.split]) < min_dist:
            if query_point[cur_point.split] < cur_point.point[cur_point.split]:
                if cur_point.right_child == None or cur_point.right_child == pre_point:#reach end or nothing to query, stop
                    pre_point = cur_point
                    cur_point = cur_point.parent
                else:
                    pre_point = cur_point
                    cur_point = binarysearch(cur_point.right_child,query_point)
            else:
                if cur_point.left_child == None or cur_point.left_child == pre_point:#reach end or nothing to query, stop
                    pre_point = cur_point
                    cur_point = cur_point.parent
                else:
                    pre_point = cur_point
                    cur_point = binarysearch(cur_point.left_child,query_point)
            if cur_point != None:
                nearest = cur_point
        else:
            pre_point = cur_point
            cur_point = cur_point.parent

    print("nearest ",nearest.point[0])
    return nearest.point[0],nearest.point[11]

def calculaue_distance(point1,point2):
    dist=0.0
    for i in range(2,11):
        dist+=(float(point1[i])-float(point2[i]))*(float(point1[i])-float(point2[i]))

    dist2=dist
    print(point1[0],"<--------------->",point2[0],"dist ",math.sqrt(dist2),)
    return math.sqrt(dist)

if __name__ == "__main__":
    training_set = fileparsing()
    original_training_set = fileparsing()

    training_set = training_set[1:len(training_set)] #remove the first one
    original_training_set = original_training_set[1:len(original_training_set)]
    #print("ts0",training_set[0])
    append_knnquery_boolean(training_set)
    root = None
    root = create_kd_tree(root,training_set,2)
    tree_traverse_check(root,1)
    #print("Root is ",root.point, "split via ",root.split ," 69 is ",original_training_set[69])
    #print("163 num and 193 num ",original_training_set[163][0],"     ",original_training_set[193][0])
    print("min dst 2 ",calculaue_distance(original_training_set[1],original_training_set[2]))
    print("min dst 213 ",calculaue_distance(original_training_set[1],original_training_set[213]))
    print("min dst 23 ",calculaue_distance(original_training_set[0],original_training_set[23]))
    #first_tree_traverse_check(root)
    validate(root,original_training_set)
    #total_cnt=0
    #tree_traverse_check(root,total_cnt)
    #print(total_cnt)
