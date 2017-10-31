/*
Modify the source code from decision_tree_functions.h, each time split different attribute to train , train about 4 tree using Combination from C(4,3) of features
*/
#include <bits/stdc++.h>
#define pb push_back
#define PAUSE {fgetc(stdin);}
#define data_cnt 150
#define RANDOM_FOREST_ATTRIBUTE_COMBINATION 4
using namespace std;
typedef vector<string> vs;
typedef vector<vs> vvs;
typedef vector<int> vi;
typedef map<string, int> msi;
typedef vector<double> vd;

unsigned int column_cnt;
int current_attribute_id; //use for untrophy Compare function

class random_forest
{
public:
	struct flower
	{
		int id;
		double sepal_length,sepal_width,pedal_length,pedal_width;
	    string ftype;
	};
	struct node
	{
		int cur_node_split_attribute_id;
		double cur_node_split_boundary;
		string result_ftype;
		bool is_leaf;
		vector<flower> current_node_data;
		node* left_child;
		node* right_child;

	};
	//vs splitted_attribute; //attribute that had been splitted before
	vector<node*> random_forest_trees;
	vector<flower> all_flower_data;
	//vs attribute_name;
	vi attribute_name_id;
	void init()
	{
		srand(time(0));
        input_data();
		attribute_name_id={0,1,2,3};
		decision_tree_train();
	}
	void input_data()
	{
		ifstream fptr;

		fptr.open("irisdata.txt");
		//cout<<"Fopen ok"<<endl;
		flower one_flower;
		string str;
		for(int i=0;i<data_cnt;i++)
		{
	        getline(fptr,str);
			one_flower.sepal_length=stof(str.substr(0,3));
			one_flower.sepal_width=stof(str.substr(4,3));
			one_flower.pedal_length=stof(str.substr(8,3));
			one_flower.pedal_width=stof(str.substr(12,3));
			one_flower.ftype=str.substr(16,str.size()-16+1);
			//	one_flower.id=i;
			all_flower_data.pb(one_flower);
		}
	}
	void build_decision_tree(vector<flower> current_data, node* current_node)
	{
		if(current_data.size()==0||current_data.size()==1||current_node==NULL)
		{
			//printf("IS EMPTY\n");
			current_node->is_leaf=1;
			current_node->left_child=NULL;
			current_node->right_child=NULL;
			current_node->result_ftype=current_data[0].ftype;
			return ; //no need to proceed
		}
		else if(is_homogeneous(current_data))
		{
			//cout<<"IS HOMOGENEOUS \n";
			current_node->is_leaf=1;
			current_node->left_child=NULL;
			current_node->right_child=NULL;
			current_node->result_ftype=current_data[0].ftype;
			return ;
		}
		else if(current_node->is_leaf==0)
		{
			//push the unsorted data back
			double cur_boundary=0.0,max_ig_boundary=0.0;
			double cur_entrophy=0.0,max_entrophy=999.0;
			int split_attribute_id=0;
			//continuous data, sort each column and gain the max entrophy
			for(int i=0;i<attribute_name_id.size();i++)
			{
				current_attribute_id=attribute_name_id[i];
				sort(current_data.begin(),current_data.end(),mycompare);
				//cout<<"Cur data sort with attname id and sort by such id"<<attribute_name_id[i];
				/*for(int i=0;i<current_data.size();i++)
				{
					cout<<current_data[i].ftype<<"   "<<aux_table_unsorted[i]<<endl;
				}*/
				//PAUSE;
				for(int current_data_row=1;current_data_row<current_data.size();current_data_row++)//check which part have changed
				{
					if(current_data[current_data_row].ftype!=current_data[current_data_row-1].ftype) //see the difference, do step 3 4
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
						//PAUSE;
						cur_entrophy=id3(current_data,current_attribute_id,cur_boundary);
						//cout<<"current_attribute_id "<<current_attribute_id<<" cur_boundary " <<cur_boundary<<" entrophy"<<cur_entrophy;

						if(cur_entrophy<=max_entrophy)
						{
							//printf(" Update min entrophy!! current boundary %f  \n	",cur_boundary);
							max_entrophy=cur_entrophy;
							max_ig_boundary=cur_boundary;
							split_attribute_id=current_attribute_id;
						}
					}
				}

			}
			//record the current split standard
			current_node->cur_node_split_attribute_id=split_attribute_id;
			current_node->cur_node_split_boundary=max_ig_boundary;
			//new tree

			node* left_sub_tree=new node;
			node* right_sub_tree=new node;

			left_sub_tree->is_leaf=0;
			right_sub_tree->is_leaf=0;

			left_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"left",split_attribute_id);
		    right_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"right",split_attribute_id);

			//splitting the tree
			current_node->right_child=right_sub_tree;
			current_node->left_child=left_sub_tree;
			//PAUSE;

			build_decision_tree(left_sub_tree->current_node_data,current_node->left_child);
			build_decision_tree(right_sub_tree->current_node_data,current_node->right_child);
		}
	}
	double id3(vector<flower>& current_data,int current_attribute_id,double cur_boundary)
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
				entrophy-=((group_a_hash[flower_name[i]]/(double)group_a)*(log2(group_a_hash[flower_name[i]]/(double)group_a)));
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
						if(current_data[i].sepal_length<=cur_boundary)
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
						if(current_data[i].sepal_width<=cur_boundary)
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
						if(current_data[i].pedal_length<=cur_boundary)
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
						if(current_data[i].pedal_width<=cur_boundary)
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
		if(group_a==0 || group_b==0)
		{
			return 999.0;
		}
		//group_a entrophy
		for(int i=0;i<3;i++)
		{
			if(group_a_hash[flower_name[i]])
			{

				entrophy-=(group_a/(double)(group_a+group_b))*((group_a_hash[flower_name[i]]/(double)group_a)*(log2(group_a_hash[flower_name[i]]/(double)group_a)));
			}
		}
		for(int i=0;i<3;i++)
		{
			if(group_b_hash[flower_name[i]])
			{
				entrophy-=(group_b/(double)(group_a+group_b))*((group_b_hash[flower_name[i]]/(double)group_b)*(log2(group_b_hash[flower_name[i]]/(double)group_b)));
			}
		}
		return (entrophy);
	}
	vector<flower> do_split(vector<flower>& current_data,double max_ig_boundary,string child_type,int split_attribute_id)
	{
		vector<flower> splitted_data;
		splitted_data.clear();
		splitted_data.resize(0);
		if(child_type=="left") //left<=boundary
		{
			for(int i=0;i<current_data.size();i++)
			{
				switch(split_attribute_id)
				{
					case 0:
					{
						if(current_data[i].sepal_length<=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 1:
					{
						if(current_data[i].sepal_width<=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 2:
					{
						if(current_data[i].pedal_length<=max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;

					}
					case 3:
					{
						if(current_data[i].pedal_width<=max_ig_boundary)
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
						if(current_data[i].sepal_length>max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 1:
					{
						if(current_data[i].sepal_width>max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;
					}
					case 2:
					{
						if(current_data[i].pedal_length>max_ig_boundary)
						{
							splitted_data.pb(current_data[i]);
						}
						break;

					}
					case 3:
					{
						if(current_data[i].pedal_width>max_ig_boundary)
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
		if(current_data.size()==1)
		{
			return true;
		}
		else
		{
			for(int i=0;i<current_data.size();i++)
			{
				if(current_data[0].ftype!=current_data[i].ftype)
				{
					return false;
				}
			}
		}

		return true;
	}
	static bool mycompare(flower flower_a,flower flower_b)
	{
		if(current_attribute_id==0)
			return flower_a.sepal_length<flower_b.sepal_length;
		else if(current_attribute_id==1)
			return flower_a.sepal_width<flower_b.sepal_width;
		else if(current_attribute_id==2)
			return flower_a.pedal_length<flower_b.pedal_length;
		else
			return flower_a.pedal_width<flower_b.pedal_width;
	}

	void decision_tree_train() //train3 and validate3
	{
		map<string,float> flower_recall;
		map<string,float> flower_precision;

		double total_accuracy=0.0;
		random_forest_trees.resize(5);
		for(int i=0;i<random_forest_trees.size();i++)
        {
            random_forest_trees[i]=new node;
        }
		cout<<"Random forest: \n";
        //cout<<"Building the random forest using C(4,3) attribute in the attribute list, 4 trees are built.\nThe training set is select the odd index in traning set.\n";
        //cout<<"Each time a conbination is selected and built that tree. \n";
        vector<flower> flower_training_data;
        vector<flower> validate_data;
        random_shuffle(all_flower_data.begin(),all_flower_data.end());
		//build random forest
		for(int i=0;i<5;i++)
		{
			//cout<<"tr size "<<flower_training_data.size()<<" va size "<<validate_data.size()<<endl;
			switch(i)
			{
				case 0:
				{
					for(int j=0;j<120;j++)
					{
						if(j<24)
						{
							//validate_data.pb(all_flower_data[i]);
						}
						else
						{
							flower_training_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 1:
				{
					for(int j=0;j<120;j++)
					{
						if(j<48&&j>=24)
						{
							//validate_data.pb(all_flower_data[i]);
						}
						else
						{
							flower_training_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 2:
				{
					for(int j=0;j<120;j++)
					{
						if(j<72&&j>=48)
						{
							//validate_data.pb(all_flower_data[i]);
						}
						else
						{
							flower_training_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 3:
				{
					for(int j=0;j<120;j++)
					{
						if(j<96&&j>=72)
						{

						}
						else
						{
							flower_training_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 4:
				{
					for(int j=0;j<120;j++)
					{
						if(j<120&&j>=96)
						{
							//validate_data.pb(all_flower_data[i]);
						}
						else
						{
							flower_training_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
			}
			//cout<<"cnt  "<<i<<endl;
			random_forest_trees[i]->is_leaf=0; //tree2 segfaluts, dont know why O_O
	        build_decision_tree(flower_training_data,random_forest_trees[i]);
			flower_training_data.clear();
			//validate_data.clear();
		}
		//cout<<"Validate \n";
		for(int i=0;i<5;i++)
		{
			switch(i)
			{
				case 0:
				{
					for(int j=0;j<all_flower_data.size();j++)
					{
						if(j<20)
						{
							validate_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 1:
				{
					for(int j=0;j<all_flower_data.size();j++)
					{
						if(j<60&&j>=30)
						{
							validate_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 2:
				{
					for(int j=0;j<all_flower_data.size();j++)
					{
						if(j<90&&j>=60)
						{
							validate_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 3:
				{
					for(int j=0;j<all_flower_data.size();j++)
					{
						if(j<120&&j>=90)
						{
							validate_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
				case 4:
				{
					for(int j=0;j<all_flower_data.size();j++)
					{
						if(j<150&&j>=120)
						{
							validate_data.pb(all_flower_data[j]);
						}
					}
					break;
				}
			}
			total_accuracy+=validate_result(validate_data,flower_recall,flower_precision);
			validate_data.clear();
		}
        for(int i=0;i<5;i++)
            clear_tree(random_forest_trees[i]);
		cout<<total_accuracy/5.0<<endl;
		cout<<flower_precision["Iris-setosa"]/5.0<<" "<<flower_recall["Iris-setosa"]/5.0<<endl;
		cout<<flower_precision["Iris-virginica"]/5.0<<" "<<flower_recall["Iris-virginica"]/5.0<<endl;
		cout<<flower_precision["Iris-versicolor"]/5.0<<" "<<flower_recall["Iris-versicolor"]/5.0<<endl;
	}
	double validate_result(vector<flower>& validate_data, map<string,float>& flower_recall, map<string,float>& flower_precision)
	{
		int tp=0,setosa_cnt=0,virg_cnt=0,versi_cnt=0,setosa_true=0,virg_true=0,versi_true=0,setosa_predict=0,virg_predict=0,versi_predict=0;
		double precision=0.0, recall=0.0 ,acc=0.0;
		vector<string> flower_names={"Iris-setosa","Iris-virginica","Iris-versicolor"};
		string original_class,predicted_class;

		for(int j=0;j<validate_data.size();j++)
		{
            //random forest vote begins at here
            int current_vote=0;
            msi random_forest_vote;
            for(int i=0;i<random_forest_trees.size();i++)//traverse 4 different trees and find the highest vote, that is the predicted_class
            {
				random_forest_vote[traverse_decision_tree(random_forest_trees[i],validate_data[j])]++;
            }
            predicted_class="Iris-setosa"; //default
            for(std::map<string,int>::iterator it=random_forest_vote.begin() ; it!=random_forest_vote.end();it++)
            {
                if(it->second>current_vote)
                {
                    current_vote=it->second;
                    predicted_class=it->first;
                }
            }
            //random forest vote ends at here
			if(predicted_class=="Iris-setosa")
			{
				setosa_predict++;
			}
			else if(predicted_class=="Iris-virginica")
			{
				virg_predict++;
			}
			else if(predicted_class=="Iris-versicolor")
			{
				versi_predict++;
			}

		}

		for(int j=0;j<validate_data.size();j++)
		{
			original_class=validate_data[j].ftype;
            //random forest vote begins at here
            int current_vote=0;
            msi random_forest_vote;
            for(int i=0;i<random_forest_trees.size();i++)//traverse 4 different trees and find the highest vote, that is the predicted_class
            {
                random_forest_vote[traverse_decision_tree(random_forest_trees[i],validate_data[j])]++;
            }
            predicted_class="Iris-setosa"; //default
            for(std::map<string,int>::iterator it=random_forest_vote.begin() ; it!=random_forest_vote.end();it++)
            {
                if(it->second>current_vote)
                {
                    current_vote=it->second;
                    predicted_class=it->first;
                }
            }
            //random forest vote ends at here
			if(original_class=="Iris-setosa")
			{
				setosa_cnt++;
				if(original_class==predicted_class)
				{
					setosa_true++;
					tp++;
				}
			}
			else if(original_class=="Iris-virginica")
			{
				virg_cnt++;
				if(original_class==predicted_class)
				{
					virg_true++;
					tp++;
				}
			}
			else if(original_class=="Iris-versicolor")
			{
				versi_cnt++;
				if(original_class==predicted_class)
				{
					versi_true++;
					tp++;
				}
			}
		}
		/*precision=((setosa_true/(double)setosa_predict)+(virg_true/(double)virg_predict)+(versi_true/(double)versi_predict))/3.0;
		recall=((setosa_true/(double)setosa_cnt)+(virg_true/(double)virg_cnt)+(versi_true/(double)versi_cnt))/3.0;*/
		acc=tp/((double)validate_data.size());
		//cout<<"tp: "<<tp<<setosa_cnt<<","<<virg_cnt<<","<<versi_cnt<<","<<setosa_true<<","<<virg_true<<","<<versi_true<<","<<setosa_predict<<","<<virg_predict<<","<<versi_predict<<endl;
		flower_recall["Iris-setosa"]+=(setosa_true/(float)setosa_cnt);
		flower_recall["Iris-virginica"]+=(virg_true/(float)virg_cnt);
		flower_recall["Iris-versicolor"]+=(versi_true/(float)versi_cnt);
		flower_precision["Iris-setosa"]+=(setosa_true/(float)setosa_predict);
		flower_precision["Iris-virginica"]+=(virg_true/(float)virg_predict);
		flower_precision["Iris-versicolor"]+=(versi_true/(float)versi_predict);
		return acc;
	}
	string traverse_decision_tree(node* current_node,flower one_flower)
	{
		string predicted_class;
		//cout<<"Traverse at "<<current_node->is_leaf<<endl;
		while(!current_node->is_leaf)
		{
			//cout<<"Traverse at inner "<<current_node<<endl;
			switch(current_node->cur_node_split_attribute_id)
			{
				case 0:
				{
					if(one_flower.sepal_length<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
				case 1:
				{
					if(one_flower.sepal_width<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
					}
				case 2:
				{
					if(one_flower.pedal_length<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
				case 3:
				{
					if(one_flower.pedal_width<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;
					break;
				}
			}
		}
		return current_node->current_node_data[0].ftype;
	}
	void clear_tree(struct node* current_node)
	{
  		if(!current_node)  // it's not
 		{
			clear_tree(current_node->left_child); // it's NULL so the call does nothing
      		clear_tree(current_node->right_child); // it's NULL so the call does nothing
			free( current_node );  // free here
  		}
	}

};
