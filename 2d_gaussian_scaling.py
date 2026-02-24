import time
import os
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# Problem size: STEP=0.0005 should yield a 30-60s serial runtime
STEP = 0.0005


def gaussian_2d(x, y, sigma=1.0):
    """Calculate the 2D Gaussian density at point (x, y)."""
    coef = 1 / (2 * np.pi * sigma**2)
    exponent = -1 * (x**2 + y**2) / (2 * sigma**2)
    return coef * np.exp(exponent)


def compute_slice(x, y_coords, sigma=1.0):
    """Worker function to compute all Y values for a given X coordinate."""
    return [gaussian_2d(x, y, sigma) for y in y_coords]


def main():
    """Execute scaling benchmarks and plot results."""
    # Setup coordinate arrays
    x_coords = np.arange(-2.0, 2.0, STEP)
    y_coords = np.arange(-2.0, 2.0, STEP)
    
    physical_cores = os.cpu_count()
    
    # Define worker counts to test: 1 up to physical cores, then beyond
    worker_counts = list(range(1, physical_cores + 1))
    worker_counts.extend([physical_cores + 4, physical_cores + 8])
    
    runtimes = []

    print(f"--- Starting Scaling Analysis (STEP={STEP}) ---")
    print(f"System detected {physical_cores} CPU cores.\n")

    for workers in worker_counts:
        print(f"Testing max_workers={workers}...", end=" ", flush=True)
        
        start_time = time.time()
        # Use Multiprocessing to bypass the GIL
        with ProcessPoolExecutor(max_workers=workers) as executor:
            # Map the slices across the process pool
            list(executor.map(compute_slice, x_coords, [y_coords] * len(x_coords)))
        
        duration = time.time() - start_time
        runtimes.append(duration)
        print(f"Time: {duration:.2f} seconds")

    # Generate the Scaling Plot
    plt.figure(figsize=(10, 6))
    plt.plot(worker_counts, runtimes, marker='o', color='navy', label='Execution Time')
    
    # Visual marker for physical core limit
    plt.axvline(x=physical_cores, color='crimson', linestyle='--', 
                label=f'Physical Core Limit ({physical_cores})')
    
    plt.xlabel("Number of Workers (max_workers)")
    plt.ylabel("Runtime (s)")
    plt.title(f"Scaling Analysis: Performance vs. Parallel Workers\n(Grid Resolution: {STEP})")
    plt.legend()
    plt.grid(alpha=0.3)
    
    # save figure
    plt.savefig("task4_scaling_plot.png")
    print("\n[SUCCESS] Plot saved as 'task4_scaling_plot.png'")
    plt.show()


if __name__ == "__main__":
    main()
