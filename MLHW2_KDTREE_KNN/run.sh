#!/bin/bash
cd ../MLHW2_KDTREE_KNN

python_src="python3"

if [ -e "kdtree_ver2.py" -a -e "train.csv" -a -e "test.csv" ];
then
    $python_src kdtree_ver2.py train.csv test.csv
    $python_src PCA.py train.csv test.csv
else
    echo "kdtree build failed, check if kdtree_ver2.py, train.csv and test.csv are all exist"
fi
