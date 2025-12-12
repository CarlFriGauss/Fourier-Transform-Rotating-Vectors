# Quick Start Examples

This file contains pre-configured settings for different use cases.
Copy the settings you want into config.py

## Example 1: Fast Preview (Quick Test)
```python
IMAGE_PATH = 'images/The_Happy_Merchant.svg'
N_VECTORS = 50
NUM_SAMPLES = 1000
ANIMATION_DURATION = 10.0
```
Render time: ~30 seconds
Best for: Quick tests and iteration

## Example 2: Balanced Quality (Recommended)
```python
IMAGE_PATH = 'images/The_Happy_Merchant.svg'
N_VECTORS = 300
NUM_SAMPLES = 10000
ANIMATION_DURATION = 50.0
```
Render time: 2-5 minutes
Best for: Most projects

## Example 3: High Detail
```python
IMAGE_PATH = 'images/The_Happy_Merchant.svg'
N_VECTORS = 1000
NUM_SAMPLES = 20000
ANIMATION_DURATION = 100.0
```
Render time: 10+ minutes
Best for: Final renders, complex images

## Example 4: Minimalist Style (No Circles)
```python
IMAGE_PATH = 'images/The_Happy_Merchant.svg'
N_VECTORS = 300
NUM_SAMPLES = 10000
ANIMATION_DURATION = 50.0
DRAW_CIRCLES = False
DRAW_ARROWS = True
SHOW_TRACER_DOT = False
PATH_COLOR = "#00FF00"
PATH_STROKE_WIDTH = 2.0
```

## Example 5: PNG/JPG Image
```python
IMAGE_PATH = 'images/The_Happy_Merchant.jpg'
N_VECTORS = 500
NUM_SAMPLES = 15000
ANIMATION_DURATION = 60.0
```
Note: For better results with photos, convert to SVG first:
```bash
cd images
python vectorize.py The_Happy_Merchant.jpg output.svg
```

## Color Schemes

### Classic
```python
CIRCLE_COLOR = "#4A90E2"  # Blue
ARROW_COLOR = "#FFFFFF"   # White
PATH_COLOR = "#FFD700"    # Gold
```

### Neon
```python
CIRCLE_COLOR = "#FF00FF"  # Magenta
ARROW_COLOR = "#00FFFF"   # Cyan
PATH_COLOR = "#00FF00"    # Green
```

### Monochrome
```python
CIRCLE_COLOR = "#666666"  # Gray
ARROW_COLOR = "#AAAAAA"   # Light gray
PATH_COLOR = "#FFFFFF"    # White
```

## Command Line Examples

### Using run.py utility:
```bash
# Quick preview
python run.py images/test.svg --quality low

# High quality with custom settings
python run.py images/logo.png --vectors 500 --duration 30 --quality high

# Convert and render
python run.py images/photo.jpg --convert output.svg --vectors 300
```

### Using manim directly:
```bash
# Low quality preview
manim -pql fourier_drawing.py FourierDrawing

# Medium quality
manim -pqm fourier_drawing.py FourierDrawing

# High quality (1080p)
manim -pqh fourier_drawing.py FourierDrawing

# 4K quality
manim -pqk fourier_drawing.py FourierDrawing
```
