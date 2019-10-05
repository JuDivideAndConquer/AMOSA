for i in {1..30}
do
    echo -e "\niteration $i |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    ./amosa_real.py "$1" "$2"
    ./convergence.py "$3"
done