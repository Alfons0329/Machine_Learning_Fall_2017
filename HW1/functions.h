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

std::ios_base::sync_with_stdio

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
	decision_tree
	{

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
		vector<node*> child;
		vector<string> aux_table_unsorted;
	};
	//vs splitted_attribute; //attribute that had been splitted before
	vs attribute_name={sepal_length,sepal_width,pedal_length,pedal_width};
	void input_data()
	{
		ifstream fptr

		fptr.open(FILE_NAME);
		vector<flower>flower_data;
		flower one_flower;
		column_cnt=0;
		string str;
		while(fptr)
		{
	        getline(fptr,str);
			for(int i=0;i<str.size();i++)
			{
				one_flower.sepal_length=str.substr(0,3);
				one_flower.sepal_width=str.substr(4,3);
				one_flower.pedal_length=str.substr(8,3);
				one_flower.sepal_width=str.substr(12,3);
				one_flower.class=str.substr(17,str.size()-17+1);
				one_flower.id=i;
				flower_data.pb(one_flower);
				if((str[i]==','||i==str.size()-1)&&i==0)
				{
					column_cnt++;
				}
			}
			for(int i=0;i<current_data.size();i++)
			{
				current_node->aux_table_unsorted.pb(current_data[i].ftype);
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
			node->is_leaf=1;
			return current_node;
		}
		else
		{
			//push the unsorted data back
			float cur_boundary=0.0,max_ig_boundary=0.0;
			double cur_entrophy=0.0,max_entrophy=0.0;

			//continuous data, sort each column and gain the max entrophy
			for(int i=0;i<column_cnt;i++)
			{
				current_attribute=attribute_name[i];
				sort(current_data.begin(),current_data.end(),mycompare);
				for(int current_data_row=0;current_data_row<current_data.size();current_data_row++)//check which part have changed
				{
					if(current_data[current_data_row].ftype!=aux_table_unsorted[i]) //see the difference, do step 3 4
					{
						cur_boundary=(current_data[current_data_row].attribute_name[i]+current_data[current_data_row].attribute_name[i-1])/2.0;
						break;
					}
				}
				//calculate the information gain
				cur_entrophy=id3(current_data,cur_boundary);
				if(cur_entrophy>max_entrophy)
				{
					max_entrophy=cur_entrophy;
					max_ig_boundary=cur_boundary;
				}
			}
			//new tree
			node* left_sub_tree=new node;
			node* right_sub_tree=new node;

			left_sub_tree->current_node_data=
			right_sub_tree->current_node_data=
			//splitting the tree
		}
	}
	double id3(vector<flower>& current_data,string split_attribute,float split_val)
	{
		msi group_a_hash;
		msi group_b_hash;
		vs flower_name={Iris-setosa,Iris-versicolor,Iris-virginica};
		int group_a=0,group_b=0;
		double entrophy=0.0;
		if(split_attribute=="start") //test
		{
			for(int i=0;i<current_data.size();i++)
			{
				group_a_hash[current_data[i].ftype]++;
				group_a++;
			}
			for(int i=0;i<flower_name;i++)
			{
				entrophy-=((group_a[flower_name[i]]/group_a)*(log2(group_a[flower_name[i]]/group_a)));
			}
			return entrophy;
		}
		else
		{
			for(int i=0;i<current_data.size();i++)
			{
				if(current_data[i].split_attribute<split_val)
				{
					group_a[current_data[i].ftype]++;
					group_a++;
				}
				else
				{
					group_b[current_data[i].ftype]++;
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
	vector<flower> do_split(float boundary,vector<flower>& current_data,string child_type,string split_attribute)
	{
		vecotr<flower>splitted_data;
		if(child_type=="left") //left<boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				if(current_data[i].split_attribute<split_val)
				{
					splitted_data.pb(current_data[i]);
				}
			}
		}
		else //right>boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				if(current_data[i].split_attribute>=split_val)
				{
					splitted_data.pb(current_data[i]);
				}
			}
		}
		return splitted_data;
	}
	bool is_homogeneous() //if the data is whole homogenous, then no need to split
	{
		for(int i=0;i<flower_data.size()-1;i++)
		{
			if(flower_data[i].ftype!=flower_data[i+1].ftype)
			{
				return false;
			}
		}
		return true;
	}
	bool sort_compare(struct flower_a,struct flower_b)
	{
		return flower_a.current_attribute<flower_b.current_attribute;
	}
}
