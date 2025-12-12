# helpers/fourier_calc.py
"""Fourier analysis utilities for extracting and processing path coordinates."""

import os
import numpy as np
from numpy.fft import fft
from svgpathtools import svg2paths
try:
    from PIL import Image
    from scipy import ndimage
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. PNG/JPG support disabled.")


def extract_path_coordinates(file_path, num_points):
    """
    Extract path coordinates from an image file (SVG, PNG, or JPG).
    
    Args:
        file_path: Path to the image file
        num_points: Number of points to sample from the path
        
    Returns:
        Tuple of (complex_points, num_points) or (None, 0) on error
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None, 0
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.svg':
        return _extract_from_svg(file_path, num_points)
    elif file_ext in ['.png', '.jpg', '.jpeg']:
        if not PIL_AVAILABLE:
            print("Error: PIL/Pillow required for PNG/JPG support")
            return None, 0
        return _extract_from_image(file_path, num_points)
    else:
        print(f"Error: Unsupported file format '{file_ext}'")
        return None, 0


def _extract_from_svg(svg_file_path, num_points):
    """Extract coordinates from SVG file."""
    try:
        paths, _ = svg2paths(svg_file_path)
    except Exception as e:
        print(f"Error reading SVG: {e}")
        return None, 0

    if not paths:
        print("Error: No paths found in the SVG file.")
        return None, 0

    # Use the first path (or combine all paths if needed)
    main_path = paths[0]
    t_values = np.linspace(0, 1, num_points, endpoint=False)
    complex_points = np.array([main_path.point(t) for t in t_values])
    
    return complex_points, num_points


def _extract_from_image(image_path, num_points):
    """Extract edge coordinates from PNG/JPG image."""
    try:
        # Load image and convert to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Detect edges using Sobel filter
        edges = ndimage.sobel(img_array)
        edges = edges > edges.mean()
        
        # Find edge coordinates
        y_coords, x_coords = np.where(edges)
        
        if len(x_coords) == 0:
            print("Error: No edges detected in image")
            return None, 0
        
        # Sort points to create a continuous path (simple approach)
        # For better results, use contour following
        points = np.column_stack((x_coords, y_coords))
        
        # Sample uniformly from the edge points
        indices = np.linspace(0, len(points)-1, num_points, dtype=int)
        sampled_points = points[indices]
        
        # Convert to complex numbers
        complex_points = sampled_points[:, 0] + 1j * sampled_points[:, 1]
        
        return complex_points, num_points
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, 0

def calculate_fourier_vectors(signal, N_samples, N_vectors):
    """
    Performs FFT, normalizes the coefficients, and sorts them.
    N_samples is required for correct normalization.
    """
    if signal is None:
        return []

    fourier_coeffs = fft(signal)
    
    # 1. Get the Frequencies (k-values)
    frequencies = np.fft.fftfreq(N_samples, d=1/N_samples)
    
    fourier_vectors = []
    for k, coeff in enumerate(fourier_coeffs):
        
        # 2. CRITICAL STEP: APPLY NORMALIZATION (division by N_samples)
        normalized_radius = np.abs(coeff) / N_samples
        
        fourier_vectors.append({
            'frequency': frequencies[k],
            'coefficient': coeff,
            'radius': normalized_radius, # CORRECTLY NORMALIZED HERE
            'phase': np.angle(coeff)
        })

    # 3. Sort by normalized radius and select the top N vectors
    fourier_vectors.sort(key=lambda v: v['radius'], reverse=True)
    
    return fourier_vectors[:N_vectors]