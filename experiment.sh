# 1st arguement : name of the test function (in caps)
# 2nd arguement : 0 or 1 (0 for AMOSA, 1 for Ref_AMOSA)
# 3rd arguement : no of objectives
# 4th arguement : file name of the true pareto front points
# example : $ ./experiment.sh DTLZ1 0 true_pareto_fronts/DTLZ1\(3\).csv 

convFilename="Ref_AMOSA_conv.csv"
rHVFilename="Ref_AMOSA_rHV.csv"

if [ $2==0 ]; then
    convFilename="AMOSA_conv.csv"
    rHVFilename="AMOSA_rHV.csv"
elif [ $2==1 ]; then
    convFilename="Ref_AMOSA_conv.csv"
    rHVFilename="Ref_AMOSA_rHV.csv"
fi

if [ -f $convFilename ]; then
    rm $convFilename
fi

rm ./plots/*

if [ -f $rHVFilename ]; then
    rm $rHVFilename
fi

for i in {1..30}; do
    echo -e "\niteration $i |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    
    ./amosa_real.py "$1" "$2" "$3"

    cp objective_values.txt ./plots/$1"_"$i.csv
    
    conv=$(./convergence.py "$4")
    echo "convergence : $conv"
    echo -e "$conv" >>$convFilename

    rHV=$(./hypervolume.py "$1")
    echo "hypervolume : $rHV"
    echo -e "$rHV" >>$rHVFilename
done