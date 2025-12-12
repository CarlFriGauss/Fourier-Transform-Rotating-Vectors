from manim import *
import numpy as np
from manim.utils.color import BLUE_GREY, RED, YELLOW_A 

# Import the core calculation logic from your helper directory
from helpers.fourier_calc import extract_path_coordinates, calculate_fourier_vectors
from helpers.complex_to_np import complex_to_np 

# --- 2. The Custom Mobject: The Epicycle System ---
class Epicycle(VGroup):
    """
    A Manim Mobject representing the entire system of rotating vectors (epicycles).
    """
    def __init__(self, vectors, t_max=1.0, **kwargs):
        super().__init__(**kwargs)
        self.vectors = vectors
        self.t_max = t_max # The 'time' needed to trace the full image (0 to 1)

        # 2a. Create the Circles and Vectors
        self.circles = VGroup()
        self.arrows = VGroup()

        # Vector 1 (DC component) often represents the center point
        initial_position = vectors[0]['radius'] * np.exp(1j * vectors[0]['phi'])
        
        # Center the entire drawing around (0, 0)
        center_offset = complex_to_np(initial_position)
        
        last_center = ORIGIN - center_offset

        for v in vectors:
            radius = v['radius']
            
            # Create a Circle for the current vector
            circle = Circle(radius=radius, color=BLUE_GREY, stroke_width=0.5, opacity=0.5)
            circle.move_to(last_center)
            self.circles.add(circle)

            # Create an Arrow/Line for the current vector
            arrow = Line(last_center, last_center + radius * RIGHT, buff=0, color=YELLOW_A)
            self.arrows.add(arrow)
            
            # The next vector starts at the tip of this one
            last_center += complex_to_np(radius * np.exp(1j * v['phase']))

        self.add(self.circles, self.arrows)
        
        # 2b. Create the Tracer Dot
        self.tracer_dot = Dot(last_center, radius=0.08, color=RED)
        self.add(self.tracer_dot)
        
        # 2c. Add the Updater (the animation engine)
        self.add_updater(self.update_epicycles)

    def update_epicycles(self, mobject, dt):
        """Calculates the new position of the vector tips based on time 't'."""
        
        # Manim's internal clock is mobject.get_time()
        # We normalize Manim's clock to our 0-to-1 signal time
        t = mobject.get_time() % self.t_max
        
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