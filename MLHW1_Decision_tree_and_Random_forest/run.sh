#!/bin/bash
cd ../MLHW1_Decision_tree_and_Random_forest
echo "Current directory ${PWD}"
gpp="g++"
gpp_flags="-std=c++11"


if [ -e "main.cpp" -a -e "decision_tree_functions.h" ];
then
    $gpp $gpp_flags main.cpp -o dt_out
    echo "Decision tree build OK!"
    ./dt_out
else
    echo "Decision tree BUILD FAILED ! main.cpp and decision_tree_functions.h have to be both exist!"
fi
