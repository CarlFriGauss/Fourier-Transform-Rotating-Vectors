"""
Optimized Fourier Drawing Animation Script

This script creates an animation of epicycles drawing an image using Fourier transforms.
The script automatically handles SVG, PNG, and JPG image formats.

Usage:
    manim -pql fourier_drawing.py FourierDrawing
    manim -pqh fourier_drawing.py FourierDrawing  (for high quality)

All settings can be modified in config.py
"""

from manim import *
import numpy as np
import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Import configuration and helpers
from config import *
from helpers.fourier_calc import extract_path_coordinates, calculate_fourier_vectors
from helpers.complex_to_np import complex_to_np


class Epicycle(VGroup):
    """
    Manim Mobject representing a system of rotating epicycles.
    
    This class manages all the rotating circles and vectors that combine
    to trace out a drawing using Fourier series approximation.
    """
    
    def __init__(self, vectors, t_max=ANIMATION_DURATION, 
                 show_circles=DRAW_CIRCLES, show_arrows=DRAW_ARROWS,
                 show_tracer=SHOW_TRACER_DOT, **kwargs):
        super().__init__(**kwargs)
        self.vectors = vectors
        self.time = 0.0
        self.t_max = t_max
        self.show_circles = show_circles
        self.show_arrows = show_arrows
        
        # Initialize component groups
        self.circles = VGroup()
        self.arrows = VGroup()
        
        # Calculate initial position and center offset
        initial_position = vectors[0]['radius'] * np.exp(1j * vectors[0]['phase'])
        center_offset = complex_to_np(initial_position)
        last_center = ORIGIN - center_offset
        
        # Create all epicycle components
        for v in vectors:
            radius = v['radius']
            
            # Create circle
            if show_circles:
                circle = Circle(radius=radius)
                circle.set_stroke(color=CIRCLE_COLOR, width=CIRCLE_STROKE_WIDTH, opacity=CIRCLE_OPACITY)
                circle.set_fill(opacity=0)
                circle.move_to(last_center)
                self.circles.add(circle)
            
            # Create arrow/vector
            if show_arrows:
                arrow = Arrow(last_center, last_center + radius * RIGHT, buff=0)
                arrow.set_stroke(color=ARROW_COLOR, width=ARROW_STROKE_WIDTH)
                self.arrows.add(arrow)
            
            # Update position for next epicycle
            last_center += complex_to_np(radius * np.exp(1j * v['phase']))
        
        # Add components to the group
        if show_circles:
            self.add(self.circles)
        if show_arrows:
            self.add(self.arrows)
        
        # Create tracer dot
        if show_tracer:
            self.tracer_dot = Dot(last_center, radius=TRACER_DOT_RADIUS, color=TRACER_DOT_COLOR)
            self.add(self.tracer_dot)
        else:
            # Create invisible tracer point for path drawing
            self.tracer_dot = Dot(last_center, radius=0.001, opacity=0)
            self.add(self.tracer_dot)
        
        # Add updater for animation
        self.add_updater(self.update_epicycles)
    
    def update_epicycles(self, mobject, dt):
        """Update all epicycle positions based on elapsed time."""
        mobject.time += dt
        t = (mobject.time % self.t_max) / self.t_max  # Normalize to [0, 1]
        
        # Calculate initial center position
        current_center = ORIGIN - complex_to_np(
            self.vectors[0]['radius'] * np.exp(1j * self.vectors[0]['phase'])
        )
        
        # Update each epicycle
        for i, v in enumerate(self.vectors):
            # Calculate rotation angle
            omega = v['frequency'] * 2 * np.pi
            angle = v['phase'] + omega * t
            vector_tip = v['radius'] * np.exp(1j * angle)
            
            # Update circle position
            if self.show_circles:
                self.circles[i].move_to(current_center)
            
            # Update arrow position and orientation
            if self.show_arrows:
                new_tip = current_center + complex_to_np(vector_tip)
                self.arrows[i].put_start_and_end_on(current_center, new_tip)
                current_center = new_tip
            else:
                current_center += complex_to_np(vector_tip)
        
        # Update tracer dot position
        self.tracer_dot.move_to(current_center)


class FourierDrawing(Scene):
    """Main scene for Fourier drawing animation."""
    
    def construct(self):
        # Load and process image
        print(f"\\n{'='*60}")
        print(f"Loading image: {IMAGE_PATH}")
        print(f"Samples: {NUM_SAMPLES} | Vectors: {N_VECTORS}")
        print(f"{'='*60}\\n")
        
        signal, n_samples = extract_path_coordinates(IMAGE_PATH, NUM_SAMPLES)
        
        if signal is None:
            print("\\n❌ Failed to load image. Exiting...")
            return
        
        # Calculate Fourier vectors
        vectors = calculate_fourier_vectors(signal, n_samples, N_VECTORS)
        
        if not vectors:
            print("\\n❌ Failed to calculate Fourier vectors. Exiting...")
            return
        
        # Scale vectors to fit in frame
        max_r = vectors[0]['radius']
        scale_factor = MAX_RADIUS / max_r
        
        for v in vectors:
            v['radius'] *= scale_factor
        
        print(f"✓ Processed {len(vectors)} vectors")
        print(f"✓ Scaled radius from {max_r:.2f} to {vectors[0]['radius']:.2f}\\n")
        
        # Create epicycle system
        epicycles = Epicycle(vectors=vectors, t_max=ANIMATION_DURATION)
        epicycles.center()
        self.add(epicycles)
        
        # Initialize drawing path
        drawing_path = VMobject()
        drawing_path.set_color(PATH_COLOR).set_stroke(width=PATH_STROKE_WIDTH)
        drawing_path.start_new_path(epicycles.tracer_dot.get_center())
        
        # Add path updater
        def update_path(path):
            new_point = epicycles.tracer_dot.get_center()
            path.add_line_to(new_point)
        
        self.add(drawing_path)
        drawing_path.add_updater(update_path)
        
        # Animate
        print(f"▶ Starting animation ({ANIMATION_DURATION}s)...\\n")
        self.wait(ANIMATION_DURATION)
        
        # Clean up and freeze final state
        drawing_path.clear_updaters()
        epicycles.clear_updaters()
        
        print(f"✓ Animation complete!\\n")
        self.wait(PAUSE_AT_END)


# Entry point for direct execution
if __name__ == "__main__":
    print("\\n" + "="*60)
    print("FOURIER DRAWING ANIMATION")
    print("="*60)
    print(f"\\nConfiguration:")
    print(f"  Image: {IMAGE_PATH}")
    print(f"  Vectors: {N_VECTORS}")
    print(f"  Samples: {NUM_SAMPLES}")
    print(f"  Duration: {ANIMATION_DURATION}s")
    print("\\nRun with: manim -pql fourier_drawing.py FourierDrawing")
    print("="*60 + "\\n")
