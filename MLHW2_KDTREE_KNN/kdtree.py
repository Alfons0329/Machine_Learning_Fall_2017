import csv
import numpy as np

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
            float(all_data_list[i][j])
            #print("parsed to",all_data_list[i][j])

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
        #print("i is now ",i)
        column_calculate = [] #empty
        for j in node_data_set:
            column_calculate.append(j[i])
        var = calculate_variance(column_calculate)
        #print(var)
        if var == 0:
            #print(column_calculate,"splitted by",i)
            x = 0
        if var > max_var:
            max_var = var
            split = i #use i+2 !!!! since first and second data is not the descripitive one
    #sort via variance to get the split_attribute
    #print("Split with ",split,"  var   ",max_var)
    #print(" nodedataset with no variance is terminated ",node_data_set)

    node_data_set.sort(key=lambda x:x[split])
    #cut in half
    point = node_data_set[int(node_data_len/2)]
    root =  kd_node(point,split)
    #split just like BST
    root.left_child = create_kd_tree(root.left_child, node_data_set[0:int(node_data_len/2)])
    root.right_child = create_kd_tree(root.right_child, node_data_set[int(node_data_len/2+1):node_data_len])
    return root

def calculate_variance(node_data_set):
    #print("In calculating var ",node_data_set)
    data_set_for_variance = np.array(node_data_set).astype(float)
    return np.var(data_set_for_variance)


def first_tree_traverse_check(current_kd_node):
    #print ("Current point ",current_kd_node.point,"Split with ",current_kd_node.split)
    current_kd_node.knn_traversed = False
    if current_kd_node.left_child:
        tree_traverse_check(current_kd_node.left_child)
    if current_kd_node.right_child:
        tree_traverse_check(current_kd_node.right_child)


def tree_traverse_check(current_kd_node):
    #print ("Current point ",current_kd_node.point,"Split with ",current_kd_node.split,"Traversed ??",current_kd_node.knn_traversed)
    current_kd_node.knn_traversed = False
    if current_kd_node.left_child:
        tree_traverse_check(current_kd_node.left_child)
    if current_kd_node.right_child:
        tree_traverse_check(current_kd_node.right_child)

def validate(root,training_set):
    validation_set = []
    for i in range(0,36):
        validation_set.append(training_set[i])
    #what to output
    output_file = open("output.txt","a") #append mode
    predicted_correct = 0
    #knn 1
    first_three_output = [[] for i in range(3)]

    for i in range(0,36):
        query_point = validation_set[i]
        print("qry pt ",query_point)
        original_class = query_point[1]
        tree_traverse_check(root) #clear all to false first
        NN,predicted_class = KNN_core(root,query_point)
        if(original_class == predicted_class):
            predicted_correct+=1

        if(i >=0 and i<3): #outputresult
            first_three_output[i].append(NN)

    print("KNN accuracy: ",float(predicted_correct/36.0))
    print(first_three_output[0])
    print(first_three_output[1])
    print(first_three_output[2])


    #knn 5

    #knn 10

    #knn 100

def KNN_core(root,query_point):

    nearest = root #just want the data in it
    min_dist = calculaue_distance (query_point,nearest.point)
    traversed_point = []
    cur_point = root #has to be the all node
    #binary search in k-dimensional space
    while cur_point:
        traversed_point.append(cur_point)
        cur_dist = calculaue_distance(query_point,cur_point.point)

        if cur_dist < min_dist and cur_point.knn_traversed == False:
            nearest = cur_point
            min_dist = cur_dist

        cur_split = cur_point.split

        if(query_point[cur_split]<cur_point.point[cur_split]):
            cur_point = cur_point.left_child
        else:
            cur_point = cur_point.right_child

    #backtrace
    while traversed_point:
        back_point = traversed_point.pop()
        cur_split = back_point.split

        #do i need to enter parent's space for searching
        if abs(float(query_point[cur_split]) - float(back_point.point[cur_split])) < min_dist:
            if(query_point[cur_split] < back_point.point[cur_split]): #the other side
                cur_point = back_point.right_child
            else:
                cur_point = back_point.left_child

            if cur_point: #is the retraversed one
                traversed_point.append(cur_point)
                back_trace_distance = (query_point,cur_point.point)
                if cur_dist < min_dist and cur_point.knn_traversed == False:
                    nearest = cur_point
                    min_dist = cur_dist

    nearest_id = nearest.point[0]
    nearest_class = nearest.point[1]
    return nearest_id,nearest_class

def calculaue_distance(point1,point2):
    sum=0.0

    for i in range(2,11):
        sum+=(float(point1[i])-float(point2[i]))*(float(point1[i])-float(point2[i]))

    return sum

if __name__ == "__main__":
    training_set = fileparsing()
    training_set = training_set[1:len(training_set)] #remove the first one
    original_training_set = training_set[1:len(training_set)]
    append_knnquery_boolean(training_set)
    root = None

    root = create_kd_tree(root,training_set)
    print("Root is ",root.point)
    first_tree_traverse_check(root)
    validate(root,original_training_set)
    #total_cnt=0
    #tree_traverse_check(root,total_cnt)
    #print(total_cnt)
