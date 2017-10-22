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
#include <bits/c++.h>
#define pb push_back

using namespace std;
typedef vector<string> vs;
typedef vector<vs> vvs;
typedef vector<int> vi;
typedef map<string, int> msi;
typedef vector<double> vd;

unsigned int column_cnt;


class decision_tree
{
public:
	struct flower
	{
		int id;
		float sepal_length,sepal_width,pedal_length,pedal_width;
	    string ftype;
	};
	struct node
	{
		string splitOn;
		bool isLeaf;
		vi idlist;
		vector<node*> child;
		vector<string> aux_table_unsorted
	};
	vs splitted_attribute; //attribute that had been splitted before
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
	        getline(fprt,str);
			for(int i=0;i<str.size();i++)
			{
				one_flower.sepal_length=str.substr(0,3);
				one_flower.sepal_width=str.substr(4,3);
				one_flower.pedal_length=str.substr(8,3);
				one_flower.sepal_width=str.substr(12,3);
				one_flower.class=str.substr(17,str.size()-17);
				one_flower.id=i;
				flower_data.pb(one_flower);
				if((str[i]==','||i==str.size()-1)&&i==0)
				{
					column_cnt++;
				}
			}
		}
	}
	void build_decision_tree()
	{
		for(int i=0;i<column_cnt;i++)
		{
			//scan all columns to determine split part

			for(int j=0;j<flower_data;j++)
			{
				so
			}
		}
	}
	double id3(vector<flower>& flower_data)
	{
		flower_data
	}
	bool is_homogeneous()
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
}
