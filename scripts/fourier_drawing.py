"""
DEPRECATED: This script has been moved to the project root.
Please use ../fourier_drawing.py instead.

This file is kept for backward compatibility.
"""

from manim import *
import numpy as np
import sys
import os

# Add parent directory to path
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, PROJECT_ROOT)

# Import from main config file
from config import *
from helpers.fourier_calc import extract_path_coordinates, calculate_fourier_vectors
from helpers.complex_to_np import complex_to_np

# Use settings from config.py (for backward compatibility)
SVG_FILE_PATH = IMAGE_PATH
N_VECTORS = N_VECTORS
NUM_SAMPLES = NUM_SAMPLES

# --- DATA GENERATION (The part you wanted to fix!) ---
# This executes BEFORE the Manim scene starts rendering.

# 1. Get the signal and N
signal, N_samples = extract_path_coordinates(SVG_FILE_PATH, NUM_SAMPLES)

# 2. Get the fully processed, normalized, and sorted vectors
DRAWING_VECTORS = calculate_fourier_vectors(signal, N_samples, N_VECTORS)

# 3. Apply Final Scaling for Manim's Frame
# We check the largest radius and scale everything so it fits nicely (e.g., max radius = 3.5)
if DRAWING_VECTORS:
    max_r = DRAWING_VECTORS[0]['radius']
    # Use 3.5 units as the target maximum radius for good screen fit
    SCALE_FACTOR = 3.5 / max_r 

    for v in DRAWING_VECTORS:
        v['radius'] *= SCALE_FACTOR # Apply the scaling factor

    print(f"\n[Manim Prep] Max Radius: {max_r:.4f} Scaled to: {DRAWING_VECTORS[0]['radius']:.4f}")
else:
    # If the file couldn't be loaded, we can't run the scene
    print("\n[Manim Prep] Cannot run scene: Vector data is empty.")
    exit()

# --- The Epicycle Mobject and FourierDrawing Scene remain the same, 
#     but now they use the globally defined DRAWING_VECTORS ---

class Epicycle(VGroup):
    """
    A Manim Mobject representing the entire system of rotating vectors (epicycles).
    """
    def __init__(self, vectors=DRAWING_VECTORS, t_max=50.0, **kwargs):
        super().__init__(**kwargs)
        self.vectors = vectors
        self.time = 0.0
        self.t_max = t_max # The 'time' needed to trace the full image (0 to 1)

        # 2a. Create the Circles and Vectors
        self.circles = VGroup()
        self.arrows = VGroup()

        # Vector 1 (DC component) often represents the center point
        initial_position = vectors[0]['radius'] * np.exp(1j * vectors[0]['phase'])
        
        # Center the entire drawing around (0, 0)
        center_offset = complex_to_np(initial_position)
        
        last_center = ORIGIN - center_offset

        for v in vectors:
            radius = v['radius']
            
           # 1. Initialize with only the necessary argument (radius)
            circle = Circle(radius=radius)
            
            # 2. Apply styling using separate methods
            circle.set_stroke(color=BLUE, width=0.5)
            circle.set_fill(opacity=0)
            
            # This line moves the circle to its starting position
            circle.move_to(last_center)
            
            self.circles.add(circle)
            
            # Create an Arrow/Line for the current vector
            arrow = Arrow(last_center, last_center + radius * RIGHT, buff=0)
            arrow.set_stroke(color=WHITE, width=2)
            self.arrows.add(arrow)
            
            # The next vector starts at the tip of this one
            last_center += complex_to_np(radius * np.exp(1j * v['phase']))

        self.add(self.circles, self.arrows)
        
        # 2b. Create the Tracer Dot
        self.tracer_dot = Dot(last_center, radius=0.08, color='#AAAAAA')
        self.add(self.tracer_dot)
        
        # 2c. Add the Updater (the animation engine)
        self.add_updater(self.update_epicycles)

    def update_epicycles(self, mobject, dt):
        """Calculates the new position of the vector tips based on time 't'."""
        
        # Manim's internal clock is mobject.get_time()
        # We normalize Manim's clock to our 0-to-1 signal time
        mobject.time += dt
        t = (mobject.time % self.t_max) / self.t_max  # Normalize to [0, 1]
        
        current_center = ORIGIN - complex_to_np(self.vectors[0]['radius'] * np.exp(1j * self.vectors[0]['phase']))
        
        # Loop through all vectors to calculate the cumulative position
        for i, v in enumerate(self.vectors):
            
            # The angular frequency (omega) is 2 * pi * frequency (f)
            omega = v['frequency'] * 2 * np.pi
            
            # Total angle = initial phase + rotation over time (omega * t)
            angle = v['phase'] + omega * t
            
            # Current vector tip position (complex number)
            vector_tip = v['radius'] * np.exp(1j * angle)
            
            # Update Circle position
            self.circles[i].move_to(current_center)
            
            # Update Arrow position and length
            new_tip = current_center + complex_to_np(vector_tip)
            self.arrows[i].put_start_and_end_on(current_center, new_tip)
            
            # The center of the next circle is the tip of the current arrow
            current_center = new_tip

        # Update the Tracer Dot (the final drawing point)
        self.tracer_dot.move_to(current_center)

class FourierDrawing(Scene):
    def construct(self):
        
        # 1. Create the Epicycle Mobject (using the global DRAWING_VECTORS)
        epicycles = Epicycle(
            vectors=DRAWING_VECTORS,  
            t_max=50.0 
        )
        epicycles.center()
        
        # 2. Add the drawing system to the scene
        self.add(epicycles)

        # 3. Initialize the drawing path as an empty VMobject
        drawing_path = VMobject()
        drawing_path.set_color(GOLD_A).set_stroke(width=1.5)
        drawing_path.start_new_path(epicycles.tracer_dot.get_center())
        
        # 4. Define the updater function
        def update_path(path):
            # The path starts by adding a single line segment to the tracer dot's position
            new_point = epicycles.tracer_dot.get_center()
            path.add_line_to(new_point)
            
        # 5. Add the path to the scene and attach the updater
        # Placing self.add(drawing_path) here ensures it's ready for the updater
        self.add(drawing_path) 
        drawing_path.add_updater(update_path)
        
        # 6. Animate the Drawing
        # Wait for exactly the full duration to complete one full drawing cycle
        self.wait(epicycles.t_max)
        
        # Remove updaters to freeze the final state
        drawing_path.clear_updaters()
        epicycles.clear_updaters()
        
        # Hold the completed drawing for 2 seconds
        self.wait(2)




    










