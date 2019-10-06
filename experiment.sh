file="./convergence$2.csv"
if [ -f $file ]; then
    rm $file
fi

for i in {1..30}; do
    echo -e "\niteration $i |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    ./amosa_real.py "$1" "$2"
    conv=$(./convergence.py "$3")
    echo "convergence : $conv"
    echo -e "$conv" >>$file
done