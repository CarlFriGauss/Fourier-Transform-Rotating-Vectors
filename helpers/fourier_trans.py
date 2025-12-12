# fourier_trans.py (Now just a simple test script)
from helpers.fourier_calc import extract_path_coordinates, calculate_fourier_vectors

# --- Configuration ---
SVG_FILE = 'images/output.svg' 
N_VECTORS = 100
NUM_SAMPLES = 1000

# 1. Read and Sample
signal, N_samples = extract_path_coordinates(SVG_FILE, NUM_SAMPLES)

# 2. Calculate and Normalize
drawing_vectors = calculate_fourier_vectors(signal, N_samples, N_VECTORS)

print(f"--- Top {N_VECTORS} Vectors (Normalized) ---")

# Print the top 5 (The Radius should now be small!)
for i, v in enumerate(drawing_vectors[:5]):
    print(f"Vector {i+1}: Radius (R): {v['radius']:.4f}, Frequency (f): {v['frequency']:.1f}")