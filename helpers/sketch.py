import os
import numpy as np
from skimage import io, color, filters, measure, feature

def image_to_sketch(image_path):
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Load the image
    image = io.imread(image_path)
    
    # If image has 4 channels (RGBA), drop the alpha channel
    if image.shape[-1] == 4:
        image = image[..., :3]
    # Convert to grayscale
    gray_image = color.rgb2gray(image)
    
    # Apply Gaussian blur to reduce noise
    blurred_image = filters.gaussian(gray_image, sigma=1.0)
    
    # Use Canny edge detection
    edges = feature.canny(blurred_image, sigma=1.0) 
    
    # Find contours from the edges
    contours = measure.find_contours(edges, level=0.8)
    
    # Create a blank canvas to draw the contours
    sketch = np.zeros_like(gray_image)
    for contour in contours:
        contour = contour.astype(int)
        for point in contour:
            y, x = point
            if 0 <= y < sketch.shape[0] and 0 <= x < sketch.shape[1]:
                sketch[y, x] = 1
    return sketch


