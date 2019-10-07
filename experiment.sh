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

for i in {1..30}; do
    echo -e "\niteration $i |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    
    ./amosa_real.py "$1" "$2"
    
    conv=$(./convergence.py "$3")
    echo "convergence : $conv"
    echo -e "$conv" >>$convFilename

    #rHV=$(./hypervolume.py "$3")
    #echo "hypervolume : $rHV"
    #echo -e "$rHV" >>$rHVFilename
done