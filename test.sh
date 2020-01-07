
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


#iteration variable
iter=1

masterfolder="./results/$algoname-$func($nobj)"
if [ -e $masterfolder ]; then
	plotfolder="$masterfolder/plots"
	if [ -e $plotfolder ]; then
		while [ -e "$plotfolder/run$iter.csv" ]; do
			iter=$(($iter+1))
		done
	else
		mkdir $plotfolder
	fi
else
	mkdir $masterfolder
	plotfolder="$masterfolder/plots"
	mkdir $plotfolder
fi

# calculating hard and soft limit
hardl=($(wc -l $trueParetoFrontsFile))
softl=$(($hardl / 5 + $hardl))

for (( i=$iter ; i<=10 ; i++ )); do
    echo -e "\n$func($nobj) algo:$algo iteration:$i ||||||||||||||||||||||||||||||||||||||||||||||||||||"
done
