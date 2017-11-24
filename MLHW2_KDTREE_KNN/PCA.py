import csv
import sys
import math
import numpy as np

PCA_PERCENTAGE = 0.85 #constant for PCA PCA_PERCENTAGE where how much proportion to hold for eigen_vectors
top_N = 0
class kd_point:
    def __init__(self ,point = None, split = None, left_child_init = None, right_child_init = None, knn_traversed_init = False): #default constructor of the class
        self.point = point #dat a point
        self.split = split
        self.left_child = left_child_init
        self.right_child = right_child_init
        self.knn_traversed = knn_traversed_init

def fileparsing():
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    with open(train_filename,'r') as opened_file: #use r for reading a file
        parsed_data = csv.reader(opened_file)
        all_data_list = list(parsed_data)

    for i in range(1,len(all_data_list)):
        for j in range(2,11):
            all_data_list[i][j]=float(all_data_list[i][j])

    with open(test_filename,'r') as opened_file:
        parsed_data = csv.reader(opened_file)
        test_data_list = list(parsed_data)

    for i in range(0,len(test_data_list)):
        for j in range(2,11):
            test_data_list[i][j]=float(test_data_list[i][j])

    return all_data_list,test_data_list
def PCA_analysis(training_set):
    training_set_pointonly = first_three_output = [[] for i in range(len(training_set))]

    for i in range (len(training_set)):
        training_set_pointonly[i]=(training_set[i][2:11])
        #print(training_set_pointonly[i])
    #doing the PCA analysis
    #zero mean of each atrribute, which is V2_attribute = V1_attribute - MEAN[attribute]

    mean_value_matrix, mean_value = get_mean_value_matrix(training_set_pointonly)
    #print(mean_value_matrix.shape)
    #print(mean_value)

    covariance_matrix = np.cov(mean_value_matrix, rowvar=0) #use row for each data
    eigen_values, eigen_vectors = np.linalg.eig(np.mat(covariance_matrix)) #calculate eigen_values and eigen_vectors
    #get top_N
    #print("Eigen values ",eigen_values)
    #print("Eigen vectors ",eigen_vectors)
    top_N = top_N_attributes_analysys(eigen_values)

    sorted_eigen_values_index = np.argsort(eigen_values)#get the index from smallest to biggest eigen values
    top_N_eigen_values_index = sorted_eigen_values_index[-1:-(top_N+1):-1]#sort in descending order
    top_N_eigen_vectors = eigen_vectors[:,top_N_eigen_values_index]
    np.array(top_N_eigen_vectors)
    new_mean_value = []
    for i in range(len(top_N_eigen_values_index)):
        new_mean_value.append(mean_value[top_N_eigen_values_index[i]])

    np.matrix(new_mean_value) #change from numpy to matrix for multiplication in np.multiply
    optimized_training_set = mean_value_matrix * top_N_eigen_vectors #does not need to add meanvalue since it is just a shift operation

    optimized_training_set = optimized_training_set.tolist() #change back to list type in python

    for i in range(len(optimized_training_set)):
        optimized_training_set[i].insert(0,training_set[i][0])
        optimized_training_set[i].insert(1,training_set[i][1])
        optimized_training_set[i].insert(11,training_set[i][11])
        optimized_training_set[i].insert(12,False)
        #print(optimized_training_set[i])

    #input()
    return optimized_training_set,top_N

def get_mean_value_matrix(training_set_pointonly):
    mean_value = np.mean(training_set_pointonly, axis = 0)
    mean_value_matrix = training_set_pointonly - mean_value

    return mean_value_matrix, mean_value

def top_N_attributes_analysys(eigen_values):
    top_N = 0
    cur_sum = 0.0
    descend = np.sort(eigen_values)[-1::-1]
    sum_eigen_values = sum(descend)
    global PCA_PERCENTAGE
    for i in range(len(descend)):
        cur_sum += descend[i]
        top_N += 1
        if cur_sum >= sum_eigen_values*PCA_PERCENTAGE:
            return top_N
def append_knnquery_boolean(all_data_list):
    for i in range(0,len(all_data_list)):
        all_data_list[i].append('false')

def create_kd_tree(root,point_data_set,split_attribute,top_N):
    point_data_len = len(point_data_set)
    median_index = int(len(point_data_set)/2)
    point_data_set.sort(key=lambda x:x[split_attribute])
    point = point_data_set[median_index]
    root =  kd_point(point,split_attribute)

    if point_data_len ==1: #build over
        return root

    if split_attribute == top_N+1:
        split_attribute = 2
    else:
        split_attribute += 1

    if median_index > 0:
        root.left_child = create_kd_tree(root.left_child, point_data_set[:median_index],split_attribute,top_N)
    if median_index < len(point_data_set)-1:
        root.right_child = create_kd_tree(root.right_child, point_data_set[median_index+1:],split_attribute,top_N)

    return root

def tree_traverse_check(current_kd_point,cnt):
    current_kd_point.knn_traversed = False
    if current_kd_point.left_child:
        tree_traverse_check(current_kd_point.left_child,cnt+1)
    if current_kd_point.right_child:
        tree_traverse_check(current_kd_point.right_child,cnt+1)

def validate(root,testing_set):
    #what to output
    output_file = open('result.txt','a') #append mode
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
    for knn_query in [1,5,10,100]:
        first_three_output = [[] for i in range(3)]
        predicted_correct = 0 #reset the predicted_correct for each knn
        for query_index in range(len(testing_set)): #test the first 3, will be changed to 36 later
            query_point = testing_set[query_index] #take the point for querying
            original_class = query_point[-2]
            for search_hash in range(len(classname_set)): #clear the hash map for the query from each point for voting
                knn_result_hash[classname_set[search_hash]] = 0

            tree_traverse_check(root,0) #clear all traversed mark to false first,which symbolized non traversed
            for individual_knn_query in range(0,knn_query):#do knn for individual point
                NN,predicted_class = KNN_core(root,query_point,individual_knn_query,knn_query)
                knn_result_hash[predicted_class] += 1 #update the hash result
                if(query_index >=0 and query_index<3): #outputresult
                    first_three_output[query_index].append(NN)

            max_voted_class = 0
            for search_hash in range(len(classname_set)): #voting for the best result
                if knn_result_hash[classname_set[search_hash]] > max_voted_class:
                    max_voted_class = knn_result_hash[classname_set[search_hash]]
                    final_predicted_class = classname_set[search_hash]

            print("Original ",original_class," predicted class",final_predicted_class)
            if(original_class == final_predicted_class):
                predicted_correct+=1

        print("A KNN Is end ",query_index,"Acc is ",float(predicted_correct)/36.0)
        output_file.write('PCA KNN accuracy: '+str(float(predicted_correct)/36.0)+'\n')
        for cnt in range(3):
            for output_index in range(len(first_three_output[cnt])):
                output_file.write(str(first_three_output[cnt][output_index])+' ') #dunno why sometimes it will be converted to float
            output_file.write('\n')
        output_file.write('\n')

    output_file.close()

def KNN_core(root,query_point,cur_knn,all_knn):

    nearest = None #just want the data in it
    min_dist = 9999.9999 #calculaue_distance (query_point,nearest.point)
    traversed_point = []
    cur_point = root #has to be the all node
    #binary search in k-dimensional space
    while cur_point:
        traversed_point.append(cur_point)
        cur_dist = calculaue_distance(query_point,cur_point.point)
        cur_split =  cur_point.split
        if cur_dist < min_dist and cur_point.knn_traversed == False: #if currently has the better point update it
            nearest = cur_point
            min_dist = cur_dist

        if( query_point[cur_split] < cur_point.point[cur_split]): #binary search bor that point
            cur_point = cur_point.left_child
        else:
            cur_point = cur_point.right_child

    #backtrace
    while traversed_point:
        back_point = traversed_point.pop() #backtracking the traversed point
        cur_split = back_point.split
        #whether do i need to enter parent's space for searching
        if back_point.left_child == None and back_point.right_child == None: #if backpoint is a leaf, just check its distance and no need to head for other side
            if calculaue_distance(query_point,back_point.point) < min_dist and back_point.knn_traversed == False:
                nearest = back_point
                min_dist = calculaue_distance(query_point,back_point.point)
        else: #if the distance b/w query_point and back_point at that axis is closer than that of current backpoint<->querypoint, backtrace the other side
            if abs(float(query_point[cur_split]) - float(back_point.point[cur_split])) < min_dist or cur_knn < all_knn:
                if(query_point[cur_split] < back_point.point[cur_split]): #head toward the other side
                    cur_point = back_point.right_child
                else:
                    cur_point = back_point.left_child
                if cur_point != None: #is the retraversed one
                    while cur_point:
                        traversed_point.append(cur_point)
                        cur_dist = calculaue_distance(query_point,cur_point.point)
                        cur_split =  cur_point.split
                        if cur_dist < min_dist and cur_point.knn_traversed == False: #if currently has the better point update it
                            nearest = cur_point
                            min_dist = cur_dist
                        if( query_point[cur_split] < cur_point.point[cur_split]): #binary search bor that point
                            cur_point = cur_point.left_child
                        else:
                            cur_point = cur_point.right_child

    nearest.knn_traversed = True #mark that knn point to be true, so that next time it will not be selected for closer distance
    nearest_id = nearest.point[0]
    nearest_class = nearest.point[-2]
    return nearest_id,nearest_class


def calculaue_distance(point1,point2):
    dist=0.0
    global top_N
    for i in range(2,top_N+2):
        dist+=(float(point1[i])-float(point2[i]))*(float(point1[i])-float(point2[i]))
    return math.sqrt(dist)

if __name__ == "__main__":
    training_set , testing_set = fileparsing()
    training_set = training_set[1:len(training_set)] #remove the first one
    optimized_training_set, top_N = PCA_analysis(training_set)
    optimized_testing_set = optimized_training_set[0:36]
    #append_knnquery_boolean(optimized_training_set)
    root = None
    root = create_kd_tree(root,optimized_training_set,2,top_N)
    tree_traverse_check(root,1)
    for i in range(len(optimized_testing_set)): #change type
        optimized_testing_set[i][0] = int(optimized_testing_set[i][0])
        for j in range(2,2+top_N):
            optimized_testing_set[i][j] = float(optimized_testing_set[i][j])

    optimized_testing_set.sort(key=lambda x:x[0]) #resort according to ID
    print(optimized_testing_set)
    #input()
    validate(root,optimized_testing_set)
