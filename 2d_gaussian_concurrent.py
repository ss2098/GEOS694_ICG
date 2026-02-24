"""
GEOS694 Lab 5: Task 3 - Parallel Gaussian using Concurrent Futures
This script uses Multiprocessing to parallelize a 2D Gaussian calculation.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# Resolution of the grid
STEP = 0.001


def gaussian_2d(x, y, sigma=1.0):
    """
    Calculate the 2D Gaussian value at a specific (x, y) coordinate.
    """
    coefficient = 1 / (2 * np.pi * sigma**2)
    exponent = -1 * (x**2 + y**2) / (2 * sigma**2)
    return coefficient * np.exp(exponent)


def compute_slice(x, y_coords, sigma):
    """
    Worker function to compute a full 'slice' (all Y values for one X).
    Parallelizing by row/column is more efficient than by individual pixel
    due to the reduction in communication overhead between processes.
    """
    return [gaussian_2d(x, y, sigma) for y in y_coords]


def plot_result(z_data):
    """
    Creates a single plot from the complete 2D array.
    """
    plt.imshow(z_data.T)
    plt.gca().invert_yaxis()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{z_data.shape} points (Parallel Processed)")
    plt.gca().set_aspect(1)


def main(xmin, xmax, ymin, ymax, sigma=1):
    """
    Sets up the process pool and aggregates the parallel results.
    """
    x_coords = np.arange(float(xmin), float(xmax), STEP)
    y_coords = np.arange(float(ymin), float(ymax), STEP)

    # Initialize the ProcessPoolExecutor with 4 workers as requested
    # Note: I have used Multiprocessing here to bypass the GIL
    with ProcessPoolExecutor(max_workers=4) as executor:
        # map() applies the worker function to every value in x_coords.
        # passingg constant y_coords and sigma values for every call.
        results = list(executor.map(
            compute_slice, 
            x_coords, 
            [y_coords] * len(x_coords), 
            [sigma] * len(x_coords)
        ))

    # Converting the list of computed slices back into a 2D NumPy array
    zz_matrix = np.array(results)
    plot_result(zz_matrix)


if __name__ == "__main__":
    print("Starting Concurrent Execution...")
    start_time = time.time()
    
    # Range parameters
    main(-2, 2, -2, 2)
    
    elapsed = time.time() - start_time
    print(f"Concurrent Elapsed Time: {elapsed:.4f}s")
    plt.show()
