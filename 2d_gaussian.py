import time
import numpy as np
import matplotlib.pyplot as plt

# Global resolution constant
STEP = 0.001


def gaussian_2d(x, y, sigma=1.0):
    """
    Calculate the 2D Gaussian density at point (x, y).

    Args:
        x (float): X-coordinate.
        y (float): Y-coordinate.
        sigma (float): Standard deviation.

    Returns:
        float: Probability density.
    """
    coefficient = 1 / (2 * np.pi * sigma**2)
    exponent = -1 * (x**2 + y**2) / (2 * sigma**2)
    return coefficient * np.exp(exponent)


def plot_gaussian(z_data):
    """
    Visualizes the 2D array using imshow.
    """
    plt.imshow(z_data.T)
    plt.gca().invert_yaxis()  # to align axes correctly 
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{z_data.shape} points")
    plt.gca().set_aspect(1)


def main(xmin, xmax, ymin, ymax, sigma=1):
    """
    Main execution loop for serial Gaussian calculation.
    """
    x_coords = np.arange(float(xmin), float(xmax), STEP)
    y_coords = np.arange(float(ymin), float(ymax), STEP)
    
    z_list = []
    for x in x_coords:
        for y in y_coords:
            z_list.append(gaussian_2d(x, y, sigma))
            
    # Reshape the flat list back into the grid dimensions
    z_matrix = np.array(z_list).reshape(len(x_coords), len(y_coords))
    plot_gaussian(z_matrix)


if __name__ == "__main__":
    start_time = time.time()
    main(-2, 2, -2, 2)
    elapsed = time.time() - start_time
    print(f"Elapsed Time: {elapsed:.4f}s")
    plt.show()
