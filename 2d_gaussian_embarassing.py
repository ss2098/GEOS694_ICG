import sys
import numpy as np
import matplotlib.pyplot as plt

# Resolution of the grid
STEP = 0.001

def gaussian_2d(x, y, sigma=1.0):
    """Calculate the 2D Gaussian density at point (x, y)."""
    coef = 1 / (2 * np.pi * sigma**2)
    expr = -1 * (x**2 + y**2) / (2 * sigma**2)
    return coef * np.exp(expr)

def main(xmin, xmax, ymin, ymax):
    """Computes and saves a specific chunk of the Gaussian grid."""
    # Convert inputs to float
    xmin, xmax, ymin, ymax = map(float, [xmin, xmax, ymin, ymax])
    
    x_range = np.arange(xmin, xmax, STEP)
    y_range = np.arange(ymin, ymax, STEP)
    
    z_list = []
    for x in x_range:
        for y in y_range:
            z_list.append(gaussian_2d(x, y))
            
    # Reshape based on the actual size of the generated ranges
    z_matrix = np.array(z_list).reshape(len(x_range), len(y_range))
    
    # Plotting logic
    plt.figure(figsize=(6, 5))
    # 'extent' ensures the axis labels match the actual coordinate space
    plt.imshow(z_matrix.T, extent=[xmin, xmax, ymin, ymax], origin='lower')
    plt.colorbar(label='Density')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Chunk: X[{xmin}, {xmax}] Y[{ymin}, {ymax}]")
    
    # Save the figure
    filename = f"gaussian_{xmin}_{xmax}.png"
    plt.savefig(filename)
    print(f"Successfully saved {filename}")

if __name__ == "__main__":
    # Check for correct number of arguments: script.py xmin xmax ymin ymax
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Usage: python 2d_gaussian_embarassing.py <xmin> <xmax> <ymin> <ymax>")
