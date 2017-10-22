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
	    float sepal_length,sepal_width,pedal_length,pedal_width;
	    string class;
	};
	struct node
	{
		string splitOn;
		bool isLeaf;
		vector<string> child_values;
		vector<node*> child;
	};

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
				flower_data.pb(one_flower);
				if(str[i]==','||i==str.size()-1)
				{
					column_cnt++;
				}
			}
		}
	}
	void biuld_decision_tree()
	{
	    for(int i=0;i<column_cnt;i++)
		{

		}
	}
	bool is_homogeneous()
	{

	}
}
