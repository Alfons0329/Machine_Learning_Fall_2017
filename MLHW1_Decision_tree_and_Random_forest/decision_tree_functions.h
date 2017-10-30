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
*/
#include <bits/stdc++.h>
#define pb push_back
#define PAUSE {fgetc(stdin);}
#define data_cnt 150
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
	vector<flower> all_flower_data;
	//vs attribute_name;
	vi attribute_name_id;
	void init()
	{
		srand(time(0));
		input_data();
		attribute_name_id={0,1,2,3}; //since switch case string is unable to use nor is the constexpr method
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
			float cur_boundary=0.0,max_ig_boundary=0.0;
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
			//cout<<"\nSplit with "<<split_attribute_id<<" which has boundary "<<max_ig_boundary<<" entrophy "<<max_entrophy<<endl;
			left_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"left",split_attribute_id);
			/*cout<<"Left subbtree data contains:  "<<left_sub_tree->current_node_data.size()<<endl;
			for(int i=0;i<left_sub_tree->current_node_data.size();i++)
			{
				cout<<left_sub_tree->current_node_data[i].sepal_length<<"|"<<left_sub_tree->current_node_data[i].sepal_width<<"|"<<left_sub_tree->current_node_data[i].pedal_length<<"|"<<left_sub_tree->current_node_data[i].pedal_width<<"|"<<left_sub_tree->current_node_data[i].ftype<<endl;
			}*/


			right_sub_tree->current_node_data=do_split(current_data,max_ig_boundary,"right",split_attribute_id);
			/*cout<<"Right subtree data contains:  "<<right_sub_tree->current_node_data.size()<<endl;
			for(int i=0;i<right_sub_tree->current_node_data.size();i++)
			{
				cout<<right_sub_tree->current_node_data[i].sepal_length<<"|"<<right_sub_tree->current_node_data[i].sepal_width<<"|"<<right_sub_tree->current_node_data[i].pedal_length<<"|"<<right_sub_tree->current_node_data[i].pedal_width<<"|"<<right_sub_tree->current_node_data[i].ftype<<endl;

			}*/

			//splitting the tree
			current_node->right_child=right_sub_tree;
			current_node->left_child=left_sub_tree;
			//PAUSE;

			build_decision_tree(left_sub_tree->current_node_data,current_node->left_child);
			build_decision_tree(right_sub_tree->current_node_data,current_node->right_child);
		}
	}
	double id3(vector<flower>& current_data,int current_attribute_id,float cur_boundary)
	{
		msi group_a_hash;
		msi group_b_hash;
		vs flower_name={"Iris-setosa","Iris-versicolor","Iris-virginica"};
		int group_a=0,group_b=0;
		float entrophy=0.0;
		if(current_attribute_id==9) //test
		{
			for(int i=0;i<current_data.size();i++)
			{
				group_a_hash[current_data[i].ftype]++;
				group_a++;
			}
			for(int i=0;i<flower_name.size();i++)
			{
				entrophy-=((group_a_hash[flower_name[i]]/(float)group_a)*(log2(group_a_hash[flower_name[i]]/(float)group_a)));
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
		//FATAL!! IF ONE PART IS NOT SPLITTED, IT IS NOT USEFUL AT ALL
		if(group_a==0 || group_b==0)
		{
			return 999.0;
		}
		//group_a entrophy
		//cout<<"ga "<<group_a<<"gb "<<group_b<<endl;
		for(int i=0;i<3;i++)
		{
			if(group_a_hash[flower_name[i]])
			{
				//cout<<"flower a"<<group_a_hash[flower_name[i]]<<endl;
				entrophy-=(group_a/(float)(group_a+group_b))*((group_a_hash[flower_name[i]]/(float)group_a)*(log2(group_a_hash[flower_name[i]]/(float)group_a)));
			}
		}
		//group_b entrophy
		for(int i=0;i<3;i++)
		{
			if(group_b_hash[flower_name[i]])
			{
				entrophy-=(group_b/(float)(group_a+group_b))*((group_b_hash[flower_name[i]]/(float)group_b)*(log2(group_b_hash[flower_name[i]]/(float)group_b)));
			}
		}
		//cout<<"Split on current_attribute_id "<<current_attribute_id<<" entrophy is "<<entrophy<<endl;
		////PAUSE;
		return (entrophy);
	}
	vector<flower> do_split(vector<flower>& current_data,float max_ig_boundary,string child_type,int split_attribute_id)
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
		float acc1=0.0,acc2=0.0,acc3=0.0,acc4=0.0,acc5=0.0;
		random_shuffle(all_flower_data.begin(),all_flower_data.end());
		//doing k fold
		//training test 1
		root= new node;
		root->is_leaf=0;
		//cout<<"Training set #1 \n";
		vector<flower> flower_training_data1;
		vector<flower> validate_data1  (all_flower_data.begin(),all_flower_data.begin()+30);
		for(int i=0;i<all_flower_data.size();i++)
		{
			if(i>=30)
			{
				flower_training_data1.pb(all_flower_data[i]);
			}
		}
		root->current_node_data=flower_training_data1;
		build_decision_tree(flower_training_data1,root);
		acc1=validate_result(validate_data1,flower_recall,flower_precision);
		flower_training_data1.clear();
		validate_data1.clear();
		clear_tree(root);
		//training test 2
		//root= new node; no need to do
		//cout<<"Training set #2 \n";
		vector<flower> flower_training_data2 ;
		vector<flower> validate_data2 (all_flower_data.begin()+30,all_flower_data.begin()+60);
        for(int i=0;i<all_flower_data.size();i++)
        {
			if(i<30)
			{
				flower_training_data2.pb(all_flower_data[i]);
			}
			else if(i>=60)
			{
				flower_training_data2.pb(all_flower_data[i]);
			}
        }
		root->current_node_data=flower_training_data2;
		build_decision_tree(flower_training_data2,root);
		acc2=validate_result(validate_data2,flower_recall,flower_precision);
		flower_training_data2.clear();
		validate_data2.clear();
		clear_tree(root);
		//training test 3
		//root= new node;
		//cout<<"Training set #3 \n";
		vector<flower> flower_training_data3 ;
		vector<flower> validate_data3 (all_flower_data.begin()+60,all_flower_data.begin()+90);
		for(int i=0;i<all_flower_data.size();i++)
		{
			if(i<60)
			{
				flower_training_data3.pb(all_flower_data[i]);
			}
			else if(i>=90)
			{
				flower_training_data3.pb(all_flower_data[i]);
			}
		}
		root->current_node_data=flower_training_data3;
		build_decision_tree(flower_training_data3,root);
		acc3=validate_result(validate_data3,flower_recall,flower_precision);
		flower_training_data3.clear();
		validate_data3.clear();
		clear_tree(root);

		//cout<<"Training set #4 \n";
		vector<flower> flower_training_data4;
		vector<flower> validate_data4 (all_flower_data.begin()+90,all_flower_data.begin()+120);
		for(int i=0;i<all_flower_data.size();i++)
		{
			if(i<90)
			{
				flower_training_data4.pb(all_flower_data[i]);
			}
			else if(i>=120)
			{
				flower_training_data4.pb(all_flower_data[i]);
			}
		}
		root->current_node_data=flower_training_data4;
		build_decision_tree(flower_training_data4,root);
		acc4=validate_result(validate_data4,flower_recall,flower_precision);
		flower_training_data4.clear();
		validate_data4.clear();
		clear_tree(root);

		//cout<<"Training set #5 \n";
		vector<flower> flower_training_data5 ;
		vector<flower> validate_data5 (all_flower_data.begin()+120,all_flower_data.begin()+150);
		for(int i=0;i<all_flower_data.size();i++)
		{
			if(i<=120)
			{
				flower_training_data5.pb(all_flower_data[i]);
			}
		}
		root->current_node_data=flower_training_data5;
		build_decision_tree(flower_training_data5,root);
		acc5=validate_result(validate_data5,flower_recall,flower_precision);
		flower_training_data5.clear();
		validate_data5.clear();
		clear_tree(root);
		cout<<(acc1+acc2+acc3+acc4+acc5)/5.0<<endl;
		cout<<flower_precision["Iris-setosa"]/5.0<<" "<<flower_recall["Iris-setosa"]/5.0<<endl;
		cout<<flower_precision["Iris-virginica"]/5.0<<" "<<flower_recall["Iris-virginica"]/5.0<<endl;
		cout<<flower_precision["Iris-versicolor"]/5.0<<" "<<flower_recall["Iris-versicolor"]/5.0<<endl;
	}
	float validate_result(vector<flower>& validate_data, map<string,float>& flower_recall, map<string,float>& flower_precision)
	{
		int tp=0,setosa_cnt=0,virg_cnt=0,versi_cnt=0,setosa_true=0,virg_true=0,versi_true=0,setosa_predict=0,virg_predict=0,versi_predict=0;
		float precision=0.0, recall=0.0 ,acc=0.0;
		vector<string> flower_names={"Iris-setosa","Iris-virginica","Iris-versicolor"};
		string original_class,predicted_class;
		//cout<<"Validation data set contains\n";
		/*for(int i=0;i<validate_data.size();i++)//debug purpose
		{
			cout<< validate_data[i].sepal_length<<","<< validate_data[i].sepal_width<<","<< validate_data[i].pedal_length<<","<< validate_data[i].pedal_width<<","<< validate_data[i].ftype<<endl;
		}*/
		for(int j=0;j<validate_data.size();j++)
		{
			predicted_class=traverse_decision_tree(root,validate_data[j]);
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
			predicted_class=traverse_decision_tree(root,validate_data[j]);
			//cout<<"Original class "<<original_class<<" Predicted class "<<predicted_class<<endl;
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
		/*precision=((setosa_true/(float)setosa_predict)+(virg_true/(float)virg_predict)+(versi_true/(float)versi_predict))/3.0;
		recall=((setosa_true/(float)setosa_cnt)+(virg_true/(float)virg_cnt)+(versi_true/(float)versi_cnt))/3.0;*/
		acc=tp/((float)validate_data.size());
		//cout<<"tp: "<<tp<<","<<setosa_cnt<<","<<virg_cnt<<","<<versi_cnt<<","<<setosa_true<<","<<virg_true<<","<<versi_true<<","<<setosa_predict<<","<<virg_predict<<","<<versi_predict<<endl;
		//cout<<"Precision "<<precision<<" Recall "<<recall<<" Accuracy "<<acc<<endl;
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

		int depth_of_tree=0;
		string predicted_class;
		while(!current_node->is_leaf)
		{

			switch(current_node->cur_node_split_attribute_id)
			{
				case 0:
				{
					if(one_flower.sepal_length<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;

					depth_of_tree++;
					break;
				}
				case 1:
				{
					if(one_flower.sepal_width<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;

					depth_of_tree++;
					break;
					}
				case 2:
				{
					if(one_flower.pedal_length<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;

					depth_of_tree++;
					break;
				}
				case 3:
				{
					if(one_flower.pedal_width<=current_node->cur_node_split_boundary)
						current_node=current_node->left_child;
					else
						current_node=current_node->right_child;

					depth_of_tree++;
					break;
				}
			}
			//printf("Depth %d \n",depth_of_tree);
			msi attribute_statistics;
			int current_attribute_vote=0;
			for(int i=0;i<current_node->current_node_data.size();i++)
			{
				attribute_statistics[current_node->current_node_data[i].ftype]++;
			}
			//printf("stastics \n");
			//cout<<"Set  "<<attribute_statistics["Iris-setosa"]<<" Versi  "<<attribute_statistics["Iris-versicolor"]<<"Virginici   "<<attribute_statistics["Iris-virginica"]<<endl;
			for(std::map<string,int>::iterator it=attribute_statistics.begin();it!=attribute_statistics.end();it++)
			{
				if(it->second >= current_attribute_vote)
				{
					predicted_class=it->first;
					current_attribute_vote=it->second;
				}
				//cout<<"Vote highest "<<it->first<<" and votre num "<<current_attribute_vote<<endl;
			}
			//cout<<"IN class "<<one_flower.ftype<<"  ptd class   "<<predicted_class<<endl;

			/*if(predicted_class==one_flower.ftype)
			{
				//cout<<"Find samc class \n";
				//current_node->is_leaf=1;
			}*/
			attribute_statistics.clear();
		}
		return predicted_class;
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
	/*constexpr unsigned int str2int(const char* str)
	{
		int h=0;
		return !str[h] ? 5381 : (str2int(str, h+1) * 33) ^ str[h];
	}*/
};
