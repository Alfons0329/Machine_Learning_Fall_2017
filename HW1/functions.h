/*
Flow chart of ID3
0.Store the data into the set of vector
1.Back up the original classfication table in the aux table
2.Sort according to the attribute (dosent matter which attribute will get the most information gain sinc the  )
3.Compare with the original table if different at index then we calculate at (or say split with (value[index]+value[index-1])/2)
4.Now the table has been splitted into 2 parts, then calcculate according to the ID3 algorithm
5.We have left_child and right_child So we split , new* left_child right child, connect them parent->newchild= something
6.take the needed data into leftchild which for example <180cm , then take all the person whose height <180cm into left child
7.If the node's data is homogenous, stop
8. still back up the aux table of original classfication and thus we can do step 2 3
9.the recursive algorithm is somehow like build_decision_tree(node* left_child) build_decision_tree(node* right_child) where the child is not null

Q:Which attribute to split first?
A:Doesnt matter, what matters is the boundary we split, the boundary has to bring us the most information gain

Q: Recursive is better? since loop cannot iterate to left_child and iterate to right_child, but by using recursive, it can
A: ??
Then each node should contain
struct node
{
	string splitOn;
	bool isLeaf; //is homogeneous
	vi idlist; //to store the CURRENT DATA, each time, we want to calculate the entrophy, check table
	node* left_child, right_child
	vector<string> aux_table_unsorted //to Compare
};

*/
#include <bits/stdc++.h>
#define pb push_back
using namespace std;


using namespace std;
typedef vector<string> vs;
typedef vector<vs> vvs;
typedef vector<int> vi;
typedef map<string, int> msi;
typedef vector<double> vd;

unsigned int column_cnt;
int current_attribute_id; //use for untrophy Compare function

class decision_tree
{
public:
	decision_tree()
	{
		input_data();
		attribute_name={"sepal_length","sepal_width","pedal_length","pedal_width"};
		attribute_name_id={0,1,2,3}; //since switch case string is unable to use nor is the constexpr method
		id3(all_flower_data,9,0);//test
		decision_tree_train();
	}
	struct flower
	{
		int id;
		float sepal_length,sepal_width,pedal_length,pedal_width;
	    string ftype;
	};
	struct node
	{
		int cur_node_split_attribute_id;
		float cur_node_split_boundary;
		string result_ftype;
		bool is_leaf;
		vector<flower> current_node_data;
		node* left_child;
		node* right_child;

	};
	//vs splitted_attribute; //attribute that had been splitted before
	node* root;
	vector<string> aux_table_unsorted;
	vector<flower> all_flower_data;
	vs attribute_name;
	vi attribute_name_id;
	void input_data()
	{
		ifstream fptr;

		fptr.open("irisdata.txt");
		cout<<"Fopen ok"<<endl;
		flower one_flower;
		string str;
		while(fptr)
		{
	        getline(fptr,str);
			for(int i=0;i<str.size();i++)
			{
				one_flower.sepal_length=stof(str.substr(0,3));
				one_flower.sepal_width=stof(str.substr(4,3));
				one_flower.pedal_length=stof(str.substr(8,3));
				one_flower.sepal_width=stof(str.substr(12,3));
				one_flower.ftype=str.substr(17,str.size()-17+1);
				one_flower.id=i;
				all_flower_data.pb(one_flower);
				aux_table_unsorted.pb(str.substr(17,str.size()-17+1));
			}

		}
	}
	node* build_decision_tree(vector<flower>& current_data, node* current_node)
	{
		if(current_data.size()==0)
		{
			return NULL; //no need to proceed
		}
		else if(is_homogeneous(current_data))
		{
			current_node->is_leaf=1;
			current_node->left_child=NULL;
			current_node->right_child=NULL;
			current_node->result_ftype=current_data[0].ftype;
			return current_node;
		}
		else
		{
			//push the unsorted data back
			float cur_boundary=0.0,max_ig_boundary=0.0;
			double cur_entrophy=0.0,max_entrophy=0.0;
			int split_attribute_id;
			//continuous data, sort each column and gain the max entrophy
			for(int i=0;i<attribute_name_id.size();i++)
			{
				current_attribute_id=attribute_name_id[i];
				sort(current_data.begin(),current_data.end(),mycompare);
				for(int current_data_row=0;current_data_row<current_data.size();current_data_row++)//check which part have changed
				{
					if(current_data[current_data_row].ftype!=aux_table_unsorted[current_data_row]) //see the difference, do step 3 4
					{
						switch(current_attribute_id)
						{
							case 0:
							{
								cur_boundary=(current_data[current_data_row].sepal_length+current_data[current_data_row-1].sepal_length)/2.0;
								break;
							}
							case 1:
							{
								cur_boundary=(current_data[current_data_row].sepal_width+current_data[current_data_row-1].sepal_width)/2.0;
								break;
							}
							case 2:
							{
								cur_boundary=(current_data[current_data_row].pedal_length+current_data[current_data_row-1].pedal_length)/2.0;
								break;
							}
							case 3:
							{
								cur_boundary=(current_data[current_data_row].pedal_width+current_data[current_data_row-1].pedal_width)/2.0;
								break;
							}
						}
						//calculate the information gain
						cur_entrophy=id3(current_data,current_attribute_id,cur_boundary);
						if(cur_entrophy>max_entrophy)
						{
							max_entrophy=cur_entrophy;
							max_ig_boundary=cur_boundary;
							split_attribute_id=current_attribute_id;
						}
					}
				}

			}
			//record the current split standard
			current_node->cur_node_split_attribute_id=split_attribute_id
			current_node->cur_node_split_boundary=max_ig_boundary;
			//new tree
			node* left_sub_tree=new node;
			node* right_sub_tree=new node;

			left_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"left",split_attribute_id);
			right_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"right",split_attribute_id);
			//splitting the tree
			current_node->left_child=left_sub_tree;
			current_node->right_child=right_sub_tree;

			build_decision_tree(left_sub_tree->current_node_data,current_node->left_child);
			build_decision_tree(right_sub_tree->current_node_data,current_node->right_child);
		}
	}
	double id3(vector<flower>& current_data,int current_attribute_id,float split_val)
	{
		msi group_a_hash;
		msi group_b_hash;
		vs flower_name={"Iris-setosa","Iris-versicolor","Iris-virginica"};
		int group_a=0,group_b=0;
		double entrophy=0.0;
		if(current_attribute_id==9) //test
		{
			for(int i=0;i<current_data.size();i++)
			{
				group_a_hash[current_data[i].ftype]++;
				group_a++;
			}
			for(int i=0;i<flower_name.size();i++)
			{
				entrophy-=((group_a_hash[flower_name[i]]/group_a)*(log2(group_a_hash[flower_name[i]]/group_a)));
			}
			return entrophy;
		}
		else
		{
			for(int i=0;i<current_data.size();i++)
			{
				switch(current_attribute_id)
				{
					case 0:
					{
						if(current_data[i].sepal_length<split_val)
						{
							group_a_hash[current_data[i].ftype]++;
							group_a++;
						}
						else
						{
							group_b_hash[current_data[i].ftype]++;
							group_b++;
						}
						break;
					}
					case 1:
					{
						if(current_data[i].sepal_width<split_val)
						{
							group_a_hash[current_data[i].ftype]++;
							group_a++;
						}
						else
						{
							group_b_hash[current_data[i].ftype]++;
							group_b++;
						}
						break;
					}
					case 2:
					{
						if(current_data[i].pedal_length<split_val)
						{
							group_a_hash[current_data[i].ftype]++;
							group_a++;
						}
						else
						{
							group_b_hash[current_data[i].ftype]++;
							group_b++;
						}
						break;
					}
					case 3:
					{
						if(current_data[i].pedal_width<split_val)
						{
							group_a_hash[current_data[i].ftype]++;
							group_a++;
						}
						else
						{
							group_b_hash[current_data[i].ftype]++;
							group_b++;
						}
						break;
					}
				}
			}
		}

		//group_a entrophy
		for(int i=0;i<3;i++)
		{
			if(group_a_hash[flower_name[i]])
			{
				entrophy-=(group_a/(group_a+group_b))*((group_a_hash[flower_name[i]]/group_a)*(log2(group_a_hash[flower_name[i]]/group_a)));
			}
		}
		//group_b entrophy
		for(int i=0;i<3;i++)
		{
			if(group_b_hash[flower_name[i]])
			{
				entrophy-=(group_b/(group_a+group_b))*((group_b_hash[flower_name[i]]/group_b)*(log2(group_b_hash[flower_name[i]]/group_b)));
			}
		}
		cout<<"Split on current_attribute_id "<<current_attribute_id<<" entrophy is "<<entrophy<<endl;
		return (entrophy);
	}
	vector<flower> do_split(vector<flower>& current_data,float max_ig_boundary,string child_type,int split_attribute_id)
	{
		vector<flower> splitted_data;
		if(child_type=="left") //left<boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				switch(split_attribute_id)
				{
					case 0:
					{
						if(current_data[i].sepal_length<max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 1:
					{
						if(current_data[i].sepal_width<max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 2:
					{
						if(current_data[i].pedal_length<max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;

					}
					case 3:
					{
						if(current_data[i].pedal_width<max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}

				}

			}
		}
		else //right>boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				switch(split_attribute_id)
				{
					case 0:
					{
						if(current_data[i].sepal_length>=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 1:
					{
						if(current_data[i].sepal_width>=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 2:
					{
						if(current_data[i].pedal_length>=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;

					}
					case 3:
					{
						if(current_data[i].pedal_width>=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}

				}
			}

		}
		return splitted_data;
	}
	bool is_homogeneous(vector<flower>& current_data) //if the data is whole homogenous, then no need to split
	{
		for(int i=0;i<current_data.size()-1;i++)
		{
			if(current_data[i].ftype!=current_data[i+1].ftype)
			{
				return false;
			}
		}
		return true;
	}
	static bool mycompare(flower flower_a,flower flower_b)
	{
		switch(current_attribute_id)
		{
			case 0:
			{
				return flower_a.sepal_length<flower_b.sepal_length;
				break;
			}
			case 1:
			{
				return flower_a.sepal_width<flower_b.sepal_width;
				break;
			}
			case 2:
			{
				return flower_a.pedal_length<flower_b.pedal_length;
				break;
			}
			case 3:
			{
				return flower_a.pedal_width<flower_b.pedal_width;
				break;
			}
		}
	}
	void decision_tree_train() //train3 and validate3
	{
		float acc1,acc2,acc3;
		root= new* node;
		random_shuffle(all_flower_data.begin(),all_flower_data.end());
		cout<<"Dataset after random shuffle---------------\n";
		for(int i=0;i<all_flower_data.size();i++)
		{
			cout<<all_flower_data[i].sepal_length<<" "<<all_flower_data[i].sepal_width<<" "<<all_flower_data[i].pedal_length<<" "<<all_flower_data[i].pedal_width<<" "<<all_flower_data[i].ftype<<endl;
		}
		//doing k fold
		//training test 1 0~74 for train 75~149 for validate
		cour<<"Training set #1 \n";
		vector<flower> flower_traning_data1 (all_flower_data.begin(),all_flower_data.begin()+74);
		vector<flower> validate_data1 (all_flower_data.begin()+75,all_flower_data.end());
		root->current_node_data=flower_traning_data1;
		root=build_decision_tree(flower_traning_data1,root);
		acc1=validate_result(validate_data1);
		flower_traning_data1.clear();
		validate_data1.clear();
		//training test 2 75~149 for train 0~74 for validate
		cour<<"Training set #1 \n";
		vector<flower> flower_traning_data2 (all_flower_data.begin()+75,all_flower_data.end());
		vector<flower> validate_data2 (all_flower_data.begin(),all_flower_data.begin()+74);
		root->current_node_data=flower_traning_data2;
		root=build_decision_tree(flower_traning_data2,root);
		acc2=validate_result(validate_data2);
		flower_traning_data2.clear();
		validate_data2.clear();
		//training test 3 25~100 for train, rest for validate
		cour<<"Training set #1 \n";
		vector<flower> flower_traning_data3 (all_flower_data.begin(),all_flower_data.begin()+74);
		vector<flower> validate_data3;
		for(int i=0;i<all_flower_data.size();i++)
		{
			if(i<24)
			{
				validate_data3.pb(all_flower_data[i]);
			}
			else if(i>99)
			{
				validate_data3.pb(all_flower_data[i]);
			}
		}
		root->current_node_data=flower_traning_data3;
		root=build_decision_tree(flower_traning_data3,root);
		acc3=validate_result(validate_data3);
		flower_traning_data3.clear();
		validate_data3.clear();

		cout<<"Total accuracy: "<<(acc1+acc2+acc3)/3.0<<endl;
	}
	float validate_result(vector<flower>& validate_data)
	{
		int tp=0,fp=0,tn=0,fn=0;
		float precision=0.0, recall=0.0 ,acc=0.0;
		vector<string> flower_names={Iris-setosa,Iris-virginica,Iris-versicolor};
		string original_class,predicted_class;
		for(int i=0;i<flower_names.size();i++)
		{
			for(int j=0;i<validate_data.size();i++)
			{
				original_class=validate_data[j].ftype;
				predicted_class=traverse_decision_tree(root,validate_data[j]);
				if(flower_names[i]==original_class && predicted_class==flower_names[i])//true positive
				{
					tp++;
				}
				else if(flower_names[i]!=original_class && predicted_class==flower_names[i]) //false positive
				{
					fp++;
				}
				else if(flower_names[i]=!=original_class && predicted_class!=flower_names[i])
				{
					tn++;
				}
				else if(flower_names[i]==original_class && predicted_class!=flower_names[i])
				{
					fn++;
				}
			}
			precision+=((float)(tp))/((float)(tp+fp));
			recall+=((float)(tp))/((float)(tp+fn));
			acc+=((float)(tp)+tn)/((float)(tp+fp+tn+fn));
		}
		precision/=3.0;
		recall/=3.0;
		acc/=3.0;
		cour<<"Precision "<<precision<<" Recall "<<recall<<" Accuracy "<<acc<<endl;
	}
	string traverse_decision_tree(node* current_node,struct one_flower)
	{
		string predicted_class;
		while(!current_node->is_leaf)
		{
			switch(current_node->cur_node_split_attribute_id)
			{
				case 0:
				{
					if(one_flower.pedal_length<current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
				case 1:
				{
					if(one_flower.pedal_width<current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
				case 2:
				{
					if(one_flower.sepal_length<current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
				case 3:
				{
					if(one_flower.sepal_width<current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
			}
		}
		return current_node->current_node_data[0].ftype;
	}

	/*constexpr unsigned int str2int(const char* str)
	{
		int h=0;
		return !str[h] ? 5381 : (str2int(str, h+1) * 33) ^ str[h];
	}*/
};
