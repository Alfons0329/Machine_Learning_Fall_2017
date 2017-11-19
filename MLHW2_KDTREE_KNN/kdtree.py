import csv
import numpy as np

class kd_node:
    def __init__(self ,point = None, split = None, left_child_init = None, right_child_init = None, knn_traversed_init = False): #default constructor of the class
        self.point = point #datqa point
        self.split = split
        self.left_child = left_child_init
        self.right_child = right_child_init
        self.knn_traversed = knn_traversed_init

def fileparsing():
    with open('train.csv','r') as opened_file : #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    return all_data_list
    #print(all_data_list)

def append_knnquery_boolean(all_data_list):
    for i in range(0,len(all_data_list)):
        all_data_list[i].append('false')

    #print(all_data_list)

def create_kd_tree(root,node_data_set):
    node_data_len = len(node_data_set)
    if node_data_len <= 1:
        return

    column_len = len(node_data_set[0]) #append somthing so minus by 4
    max_var = 0
    split = 0
    for i in range(2,column_len-2):
        print("i is now ",i)
        column_calculate = [] #empty
        for j in node_data_set:
            column_calculate.append(j[i])
        var = calculate_variance(column_calculate)
        print(var)
        if var == 0:
            print(column_calculate,"splitted by",i)
        if var > max_var:
            max_var = var
            split = i #use i+2 !!!! since first and second data is not the descripitive one
    #sort via variance to get the split_attribute
    print("Split with ",split,"  var   ",max_var)
    #print(" nodedataset with no variance is terminated ",node_data_set)

    node_data_set.sort(key=lambda x:x[split])
    #cut in half
    point = node_data_set[int(node_data_len/2)]
    root =  kd_node(point,split)
    root.left_child = create_kd_tree(root.left_child, node_data_set[0:int(node_data_len/2)])
    root.right_child = create_kd_tree(root.right_child, node_data_set[int(node_data_len/2+1):node_data_len])
    return root

def calculate_variance(node_data_set):
    #print("In calculating var ",node_data_set)
    data_set_for_variance = np.array(node_data_set).astype(float)
    return np.var(data_set_for_variance)


def tree_traverse_check(current_kd_node,cnt):
    cnt+=1
    print ("Current point ",current_kd_node.point,"Split with ",current_kd_node.split,"Traversed ??",current_kd_node.knn_traversed)
    if current_kd_node.left_child:
        tree_traverse_check(current_kd_node.left_child,cnt)
    if current_kd_node.right_child:
        tree_traverse_check(current_kd_node.right_child,cnt)

if __name__ == "__main__":
    training_set = fileparsing()
    training_set = training_set[1:len(training_set)] #remove the first one
    append_knnquery_boolean(training_set)
    root = None
    root = create_kd_tree(root,training_set)
    total_cnt=0
    tree_traverse_check(root,total_cnt)
    print(total_cnt)
    
