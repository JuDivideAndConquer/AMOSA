# first arguement : name of the test function (in caps)
# second arguement : 0 or 1 (0 for AMOSA, 1 for Ref_AMOSA)
# third arguement : file name of the true pareto front points
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

if [ -f $rHVFilename ]; then
    rm $rHVFilename
fi

for i in {1..3}; do
    echo -e "\niteration $i |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    
    ./amosa_real.py "$1" "$2"
    
    conv=$(./convergence.py "$3")
    echo "convergence : $conv"
    echo -e "$conv" >>$convFilename

    rHV=$(./hypervolume.py "$1")
    echo "hypervolume : $rHV"
    echo -e "$rHV" >>$rHVFilename
done