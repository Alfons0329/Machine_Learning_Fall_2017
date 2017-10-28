#!/bin/bash
cd ../MLHW1_Decision_tree_and_Random_forest
echo "Current directory ${PWD}"
gpp="g++"
gpp_flags="-std=c++11"


if [ -e "random_forest_main.cpp" -a -e "random_forest.h" ];
then
    $gpp $gpp_flags random_forest_main.cpp -o rf_out
    echo "Random forest build OK!"
    ./rf_out
else
    echo "Random forest BUILD FAILED ! main.cpp and random_forest.h have to be both exist!"
fi
