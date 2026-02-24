# Run four quadrants simultaneously
python 2d_gaussian_embarassing.py -2 0 -2 0 &
python 2d_gaussian_embarassing.py 0 2 -2 0 &
python 2d_gaussian_embarassing.py -2 0 0 2 &
python 2d_gaussian_embarassing.py 0 2 0 2 &
wait
echo "All four quadrants finished."

