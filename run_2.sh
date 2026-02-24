# Run the left half and right half simultaneously
python 2d_gaussian_embarassing.py -2 0 -2 2 &
python 2d_gaussian_embarassing.py 0 2 -2 2 &
wait
echo "Both tasks finished."

