"""
Configuration file for Fourier Drawing animation.

Modify these settings to customize your animation:
- IMAGE_PATH: Path to your image file (SVG, PNG, or JPG)
- N_VECTORS: Number of epicycles (more = more detail, but slower)
- NUM_SAMPLES: Number of points sampled from the image (higher = smoother)
- ANIMATION_DURATION: Time in seconds for one complete drawing cycle
- DRAW_CIRCLES: Whether to show the rotating circles
- DRAW_ARROWS: Whether to show the rotating vectors
- CIRCLE_COLOR: Color of the circles
- ARROW_COLOR: Color of the arrows
- PATH_COLOR: Color of the drawn path
"""

# ============== IMAGE SETTINGS ==============
IMAGE_PATH = 'images/The_Happy_Merchant.svg'  # Path to your image file

# ============== FOURIER SETTINGS ==============
N_VECTORS = 300          # Number of epicycles (recommended: 100-500)
NUM_SAMPLES = 10000      # Sampling resolution (recommended: 1000-10000)

# ============== ANIMATION SETTINGS ==============
ANIMATION_DURATION = 50.0  # Duration in seconds for one complete cycle
PAUSE_AT_END = 2.0        # Pause duration after completing the drawing

# ============== VISUAL SETTINGS ==============
DRAW_CIRCLES = True       # Show rotating circles
DRAW_ARROWS = True        # Show rotating vectors
SHOW_TRACER_DOT = True    # Show the drawing point

# Color settings (use Manim color names or hex codes)
CIRCLE_COLOR = "#4A90E2"  # Light blue
CIRCLE_OPACITY = 0.5
CIRCLE_STROKE_WIDTH = 0.5

ARROW_COLOR = "#FFFFFF"   # White
ARROW_STROKE_WIDTH = 2

PATH_COLOR = "#FFD700"    # Gold
PATH_STROKE_WIDTH = 1.5

TRACER_DOT_COLOR = "#AAAAAA"  # Gray
TRACER_DOT_RADIUS = 0.08

# ============== FRAME SETTINGS ==============
MAX_RADIUS = 3.5          # Maximum radius for scaling to fit in frame
