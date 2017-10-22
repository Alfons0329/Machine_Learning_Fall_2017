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
string current_attribute; //use for untrophy Compare function

class decision_tree
{
public:
	decision_tree()
	{
		input_data();
		attribute_name={"sepal_length","sepal_width","pedal_length","pedal_width"};
		id3();
	}
	struct flower
	{
		int id;
		float sepal_length,sepal_width,pedal_length,pedal_width;
	    string ftype;
	};
	struct node
	{
		string split_on;
		bool is_leaf;
		vector<flower> current_node_data;
		node* left_child;
		node* right_child;

	};
	//vs splitted_attribute; //attribute that had been splitted before
	vector<string> aux_table_unsorted;
	vs attribute_name;
	void input_data()
	{
		ifstream fptr;

		fptr.open("irisdata.txt");
		vector<flower>flower_data;
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
				flower_data.pb(one_flower);
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
			return current_node;
		}
		else
		{
			//push the unsorted data back
			float cur_boundary=0.0,max_ig_boundary=0.0;
			double cur_entrophy=0.0,max_entrophy=0.0;
			string split_attribute;
			//continuous data, sort each column and gain the max entrophy
			for(int i=0;i<attribute_name.size();i++)
			{
				current_attribute=attribute_name[i];
				sort(current_data.begin(),current_data.end(),mycompare);
				for(int current_data_row=0;current_data_row<current_data.size();current_data_row++)//check which part have changed
				{
					if(current_data[current_data_row].ftype!=aux_table_unsorted[current_data_row]) //see the difference, do step 3 4
					{
						switch(str2int(current_attribute))
						{
							case str2int("sepal_length"):
							{
								cur_boundary=(current_data[current_data_row].sepal_length+current_data[current_data_row-1].sepal_length)/2.0;
								break;
							}
							case str2int("sepal_width"):
							{
								cur_boundary=(current_data[current_data_row].sepal_width+current_data[current_data_row-1].sepal_width)/2.0;
								break;
							}
							case str2int("pedal_length"):
							{
								cur_boundary=(current_data[current_data_row].pedal_length+current_data[current_data_row-1].pedal_length)/2.0;
								break;
							}
							case str2int("pedal_width"):
							{
								cur_boundary=(current_data[current_data_row].pedal_width+current_data[current_data_row-1].pedal_width)/2.0;
								break;
							}
						}
						//calculate the information gain
						cur_entrophy=id3(current_data,cur_boundary);
						if(cur_entrophy>max_entrophy)
						{
							max_entrophy=cur_entrophy;
							max_ig_boundary=cur_boundary;
							split_attribute=current_attribute;
						}
					}
				}

			}
			//new tree
			node* left_sub_tree=new node;
			node* right_sub_tree=new node;

			left_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"left",split_attribute);
			right_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"right",split_attribute);
			//splitting the tree
			current_node->left_child=left_sub_tree;
			current_node->right_child=right_sub_tree;

			build_decision_tree(left_sub_tree->current_node_data,current_node->left_child);
			build_decision_tree(right_sub_tree->current_node_data,current_node->right_child);
		}
	}
	double id3(vector<flower>& current_data,string split_attribute,float split_val)
	{
		msi group_a_hash;
		msi group_b_hash;
		vs flower_name={"Iris-setosa","Iris-versicolor","Iris-virginica"};
		int group_a=0,group_b=0;
		double entrophy=0.0;
		if(split_attribute=="start") //test
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
				if(current_data[i].split_attribute<split_val)
				{
					group_a_hash[current_data[i].ftype]++;
					group_a++;
				}
				else
				{
					group_b_hash[current_data[i].ftype]++;
					group_b++;
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
			if(group_b[flower_name[i]])
			{
				entrophy-=(group_b/(group_a+group_b))*((group_b_hash[flower_name[i]]/group_b)*(log2(group_b_hash[flower_name[i]]/group_b)));
			}
		}
		return (entrophy);
	}
	vector<flower> do_split(vector<flower>& current_data,float max_ig_boundary,string child_type,string split_attribute)
	{
		vecotr<flower> splitted_data;
		if(child_type=="left") //left<boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				if(current_data[i].split_attribute<max_ig_boundary)
				{
					splitted_data.pb(current_data[i]);
				}
			}
		}
		else //right>boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				if(current_data[i].split_attribute>=max_ig_boundary)
				{
					splitted_data.pb(current_data[i]);
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
	bool mycompare(flower flower_a,flower flower_b)
	{
		switch(str2int(current_attribute))
		{
			case str2int("sepal_length"):
			{
				return flower_a.sepal_length<flower_b.sepal_length;
				break;
			}
			case str2int("sepal_width"):
			{
				return flower_a.sepal_width<flower_b.sepal_width;
				break;
			}
			case str2int("pedal_length"):
			{
				return flower_a.pedal_length<flower_b.pedal_length;
				break;
			}
			case str2int("pedal_width"):
			{
				return flower_a.pedal_width<flower_b.pedal_width;
				break;
			}
		}
	}
	constexpr unsigned int str2int(const char* str)
	{
		int h=0;
		return !str[h] ? 5381 : (str2int(str, h+1) * 33) ^ str[h];
	}
};
