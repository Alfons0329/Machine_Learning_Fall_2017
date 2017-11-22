import csv
import numpy as np
import os
import pprint
class kd_node:
    def __init__(self ,point = None, split = None, left_child_init = None, right_child_init = None, knn_traversed_init = False): #default constructor of the class
        self.point = point #dat a point
        self.split = split
        self.left_child = left_child_init
        self.right_child = right_child_init
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
        return root

    if split_attribute == 10:
        split_attribute = 2
    else:
        split_attribute += 1

    if median_index > 0:
        root.left_child = create_kd_tree(root.left_child, node_data_set[:median_index],split_attribute)
    if median_index < len(node_data_set)-1:
        root.right_child = create_kd_tree(root.right_child, node_data_set[median_index+1:],split_attribute)

    return root

def tree_traverse_check(current_kd_node,cnt):
    current_kd_node.knn_traversed = False

    if current_kd_node.left_child:
        tree_traverse_check(current_kd_node.left_child,cnt+1)
    if current_kd_node.right_child:
        tree_traverse_check(current_kd_node.right_child,cnt+1)

def validate(root,training_set):
    validation_set = []

    for i in range(0,36):
        validation_set.append(training_set[i])
    #what to output
    output_file = open('result.txt','w') #append mode
    predicted_correct = 0
    #knn 1
    first_three_output = [[] for i in range(3)]
    for knn_query in [1,5,10,100]:
        for query_index in range(0,36):
            query_point = validation_set[i] #take the point for querying

            for individual_knn_query in range(0,knn_query):
                original_class = query_point[11]
                tree_traverse_check(root,0) #clear all to false first
                NN,predicted_class = KNN_core(root,query_point)

                if(original_class == predicted_class):
                    predicted_correct+=1
                if(query_index >=0 and query_index<3): #outputresult
                    first_three_output[query_index].append(NN)

            output_file.write('KNN accuracy: '+str(float(predicted_correct/36.0)))
            output_file.write(first_three_output[0])
            output_file.write(first_three_output[1])
            output_file.write(first_three_output[2])


    output_file.close()

def KNN_core(root,query_point):

    nearest = root #just want the data in it
    min_dist = calculaue_distance (query_point,nearest.point)
    traversed_point = []
    cur_point = root #has to be the all node
    #binary search in k-dimensional space
    print("query datapt",query_point)
    while cur_point:
        traversed_point.append(cur_point)
        print("traversed to",cur_point.point, "split via ",cur_point.split)
        cur_dist = calculaue_distance(query_point,cur_point.point)

        if cur_dist < min_dist and cur_point.knn_traversed == False:
            nearest = cur_point
            min_dist = cur_dist

        cur_split = cur_point.split

        if(query_point[cur_split] < cur_point.point[cur_split]):
            cur_point = cur_point.left_child
            print("hl")
        else:
            cur_point = cur_point.right_child
            print("hr")
    #backtrace
    while traversed_point:
        back_point = traversed_point.pop()
        cur_split = back_point.split

        #do i need to enter parent's space for searching
        print("BACK TRACK TO ",back_point.point, "split via ",back_point.split)
        print("min dist ",min_dist," with hyprectl dist ",abs(float(query_point[cur_split]) - float(back_point.point[cur_split])))
        if abs(float(query_point[cur_split]) - float(back_point.point[cur_split])) < min_dist:
            if(query_point[cur_split] < back_point.point[cur_split]): #the other side
                cur_point = back_point.right_child
            else:
                cur_point = back_point.left_child

            if cur_point: #is the retraversed one
                traversed_point.append(cur_point)
                back_trace_distance = calculaue_distance(query_point,cur_point.point)

                if back_trace_distance < min_dist and cur_point.knn_traversed == False:
                    nearest = cur_point
                    min_dist = back_trace_distance

    nearest.knn_traversed = True
    nearest_id = nearest.point[0]
    nearest_class = nearest.point[11]
    print("nearest point ",nearest.point)
    return nearest_id,nearest_class

def calculaue_distance(point1,point2):
    dist=0.0
    for i in range(2,11):
        dist+=(float(point1[i])-float(point2[i]))*(float(point1[i])-float(point2[i]))

    dist2=dist
    print(" dist ",dist2)
    return dist

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
    #print("min dst 193 ",calculaue_distance(original_training_set[0],original_training_set[193]))
    #print("min dst 163 ",calculaue_distance(original_training_set[0],original_training_set[163]))
    #print("min dst 253 ",calculaue_distance(original_training_set[0],original_training_set[253]))
    #first_tree_traverse_check(root)
    validate(root,original_training_set)
    #total_cnt=0
    #tree_traverse_check(root,total_cnt)
    #print(total_cnt)
