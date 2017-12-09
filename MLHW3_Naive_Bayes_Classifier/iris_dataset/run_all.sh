#!/bin/bash
#cd ../MLHW3_Naive_Bayes_Classifier/iris_dataset
python_src="python" #python for anaconda and python3 for non-anaconda system
iris_dataset="iris.csv"
iris_train="train.csv"
iris_test="test.csv"
if [ -e "rnd_tstdata_gnr.py" -a -e $iris_dataset ];
then
    $python_src rnd_tstdata_gnr.py $iris_dataset $iris_train $iris_test
else
    echo "
    Random training_set and testing_set generator build failed
    check if rnd_tstdata_gnr,
    iris.csv and test.csv are all exist"
fi

if [ -e "naive_bayes_classifier.py" -a -e $iris_train -a -e $iris_train ];
then
    $python_src naive_bayes_classifier.py $iris_train $iris_test
else
    echo "
    Naive_Bayes_Classifier build failed,
    check if kdtree_ver2.py,
    train.csv and test.csv are all exist"
fi
