# 1st arguement : name of the test function (in caps)
# 2nd arguement : no of objectives
# 3rd arguement : file name of the true pareto front points
# 4th arguement : no of interations
# example : $ ./experiment.sh DTLZ1 true_pareto_fronts/DTLZ1\(3\).csv 30

# check if the result folder exists if not create one
if [ ! -e results ]; then
    mkdir results
fi

func=$1
nobj=$2
trueParetoFrontsFile=$3
coolingRate=0.8

# True pareto front file validation
if [ ! -e $trueParetoFrontsFile ]; then
    echo "File '$trueParetoFrontsFile' does not exits"
    exit 1
fi


#iteration variable
iter=1

masterfolder="./results/$func($nobj)"
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

for (( i=$iter ; i<=$4 ; i++ )); do

    echo -e "\n$func($nobj) algo:$algo iteration:$i ||||||||||||||||||||||||||||||||||||||||||||||||||||"
    plot="$plotfolder/run$i.csv"
    convFilename="$masterfolder/conv.csv"
    rHVFilename="$masterfolder/rHV.csv"

    python3 ./amosa_real.py $func $nobj $hardl $softl $coolingRate $plot

    conv=$(python3 ./convergence.py "$trueParetoFrontsFile" "$plot")
    echo "convergence : $conv"
    echo -e "$conv" >>$convFilename

    rHV=$(python3 ./hypervolume.py "$func" "$plot")
    echo "hypervolume : $rHV"
    echo -e "$rHV" >>$rHVFilename

done
