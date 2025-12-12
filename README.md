# Fourier Drawing Animation

A highly optimized and generalized Manim project that creates mesmerizing epicycle animations from any image using Fourier transforms.

## Features

- ✅ **Multi-format support**: Works with SVG, PNG, and JPG images
- ✅ **Highly configurable**: All settings in one easy-to-edit config file
- ✅ **Optimized performance**: Efficient FFT-based calculations
- ✅ **Clean architecture**: Modular, well-documented code
- ✅ **Flexible visualization**: Toggle circles, arrows, and customize colors

## Quick Start

### 1. Installation

Ensure you have the required dependencies:

```bash
pip install manim pillow scipy svgpathtools
```

For PNG/JPG to SVG conversion (optional):
```bash
# Install ImageMagick and Potrace
# Windows: Download from official websites
# Linux: sudo apt-get install imagemagick potrace
# Mac: brew install imagemagick potrace
```

### 2. Basic Usage

1. **Configure your animation** in `config.py`:
   ```python
   IMAGE_PATH = 'images/your_image.svg'  # or .png, .jpg
   N_VECTORS = 300                        # Number of epicycles
   NUM_SAMPLES = 10000                    # Sampling resolution
   ANIMATION_DURATION = 50.0              # Animation length in seconds
   ```

2. **Run the animation**:
   ```bash
   # Quick preview (low quality)
   manim -pql fourier_drawing.py FourierDrawing
   
   # High quality render
   manim -pqh fourier_drawing.py FourierDrawing
   
   # 4K quality
   manim -pqk fourier_drawing.py FourierDrawing
   ```

## Configuration Options

All settings are in `config.py`:

### Image Settings
- `IMAGE_PATH`: Path to your image file (SVG, PNG, or JPG)

### Fourier Settings
- `N_VECTORS`: Number of epicycles (100-500 recommended)
- `NUM_SAMPLES`: Sampling resolution (1000-10000 recommended)

### Animation Settings
- `ANIMATION_DURATION`: Duration in seconds for one complete cycle
- `PAUSE_AT_END`: Pause duration after completing the drawing

### Visual Settings
- `DRAW_CIRCLES`: Show/hide rotating circles
- `DRAW_ARROWS`: Show/hide rotating vectors
- `SHOW_TRACER_DOT`: Show/hide the drawing point
- Various color and style options

## Project Structure

```
d:/Python/Manim/
├── config.py                 # Main configuration file
├── fourier_drawing.py        # Main animation script
├── helpers/
│   ├── fourier_calc.py      # Fourier transform calculations
│   └── complex_to_np.py     # Utility functions
├── images/
│   ├── vectorize.py         # PNG/JPG to SVG converter
│   └── [your images]
└── media/                   # Rendered videos (created automatically)
```

## Converting Images

### For PNG/JPG Images

The script automatically handles PNG/JPG files by detecting edges. For better results, you can convert them to SVG first:

```bash
cd images
python vectorize.py your_image.jpg output.svg
```

Then update `config.py`:
```python
IMAGE_PATH = 'images/output.svg'
```

## Tips for Best Results

1. **Start small**: Begin with `N_VECTORS=100` and `NUM_SAMPLES=1000` for quick tests
2. **Simple images work best**: High-contrast, simple shapes produce cleaner results
3. **Adjust duration**: Longer durations (50-100s) look smoother but take longer to render
4. **Quality vs. Speed**:
   - More vectors = more detail but slower rendering
   - More samples = smoother paths but slower preprocessing

## Performance Guide

| Setting | Fast | Balanced | High Quality |
|---------|------|----------|--------------|
| N_VECTORS | 50-100 | 200-300 | 500-1000 |
| NUM_SAMPLES | 1000-2000 | 5000-10000 | 10000-20000 |
| Render time | <1 min | 2-5 min | 10+ min |

## Troubleshooting

### "No module named 'PIL'"
```bash
pip install pillow
```

### "No module named 'svgpathtools'"
```bash
pip install svgpathtools
```

### Image not loading
- Check the file path in `config.py`
- Ensure the image file exists
- Try using an absolute path

### Animation cuts off early
- Increase `ANIMATION_DURATION` in `config.py`
- Ensure `PAUSE_AT_END` is set to a positive value

### Poor quality output
- Increase `NUM_SAMPLES` for smoother paths
- Increase `N_VECTORS` for more detail
- Use higher render quality: `-pqh` or `-pqk`

## Examples

See the `images/` directory for example images and their settings:

1. **Simple logo** (N_VECTORS=100, NUM_SAMPLES=2000, Duration=20s)
2. **Complex drawing** (N_VECTORS=500, NUM_SAMPLES=10000, Duration=60s)

## License

This project is open source and available for educational purposes.

## Credits

Built with:
- [Manim Community](https://www.manim.community/)
- NumPy, SciPy
- svgpathtools
- Pillow (PIL)
