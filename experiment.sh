# 1st arguement : name of the test function (in caps)
# 2nd arguement : 0 or 1 (0 for AMOSA, 1 for Ref_AMOSA)
# 3rd arguement : no of objectives
# 4th arguement : file name of the true pareto front points
# example : $ ./experiment.sh DTLZ1 0 true_pareto_fronts/DTLZ1\(3\).csv

# check if the result folder exists if not create one
if [ ! -e results ]; then
    mkdir results
fi

func=$1
nobj=$2
algo=$3
trueParetoFrontsFile=$4

# read -p "Enter the name of the test function : " func
# read -p "Enter the number of objectives : " nobj
# read -p "Enter the algorithm type(0 of AMOSA, 1 of Ref_AMOSA) : " algo
# read -p "File storing true pareto front points : " trueParetoFrontsFile

# Algo validation
if [ $algo -eq 0 ]; then
    algoname="AMOSA"
elif [ $algo -eq 1 ]; then
    algoname="Ref_AMOSA"
else
    echo "Invalid algo"
    exit 1
fi

# True pareto front file validation
if [ ! -e $trueParetoFrontsFile ]; then
    echo "File '$trueParetoFrontsFile' does not exits"
    exit 1
fi

masterfolder="./results/$algoname-$func($nobj)"
if [ -e $masterfolder ]; then
    rm -r $masterfolder
fi
mkdir $masterfolder

plotfolder="$masterfolder/plots"
mkdir $plotfolder

# calculating hard and soft limit
hardl=($(wc -l $trueParetoFrontsFile))
softl=$(($hardl / 5 + $hardl))

for i in {1..3}; do
    echo -e "\n$func($nobj) algo:$algo iteration:$i |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    plot="$plotfolder/run$i.csv"
    convFilename="$masterfolder/conv.csv"
    rHVFilename="$masterfolder/rHV.csv"

    ./amosa_real.py $func $algo $nobj $hardl $softl $plot

    conv=$(./convergence.py "$trueParetoFrontsFile" "$plot")
    echo "convergence : $conv"
    echo -e "$conv" >>$convFilename

    rHV=$(./hypervolume.py "$func" "$plot")
    echo "hypervolume : $rHV"
    echo -e "$rHV" >>$rHVFilename

done