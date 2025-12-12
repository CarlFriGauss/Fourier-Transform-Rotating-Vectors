"""
Initialize the Fourier Drawing project with default settings.

Run this script once after cloning the repository to set up
the project structure and verify all dependencies.
"""

import os
import sys

def check_imports():
    """Check if all required packages are installed."""
    print("Checking dependencies...")
    missing = []
    
    try:
        import manim
        print("✓ manim")
    except ImportError:
        missing.append("manim")
        print("✗ manim - MISSING")
    
    try:
        import numpy
        print("✓ numpy")
    except ImportError:
        missing.append("numpy")
        print("✗ numpy - MISSING")
    
    try:
        from PIL import Image
        print("✓ Pillow (PIL)")
    except ImportError:
        missing.append("Pillow")
        print("✗ Pillow - MISSING (optional for PNG/JPG)")
    
    try:
        import scipy
        print("✓ scipy")
    except ImportError:
        missing.append("scipy")
        print("✗ scipy - MISSING (optional for PNG/JPG)")
    
    try:
        import svgpathtools
        print("✓ svgpathtools")
    except ImportError:
        missing.append("svgpathtools")
        print("✗ svgpathtools - MISSING")
    
    return missing

def create_directories():
    """Create necessary directories if they don't exist."""
    print("\nChecking directory structure...")
    
    dirs = ['images', 'media', 'helpers']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"✓ Created {d}/")
        else:
            print(f"✓ {d}/ exists")

def main():
    print("="*60)
    print("FOURIER DRAWING PROJECT SETUP")
    print("="*60)
    print()
    
    # Check dependencies
    missing = check_imports()
    print()
    
    if missing:
        print(f"⚠ Missing packages: {', '.join(missing)}")
        print("\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        print("\nOr install all requirements:")
        print("  pip install -r requirements.txt")
    else:
        print("✓ All dependencies installed!")
    
    print()
    
    # Check directories
    create_directories()
    print()
    
    # Check for sample images
    print("Checking for sample images...")
    image_files = [f for f in os.listdir('images') if f.endswith(('.svg', '.png', '.jpg', '.jpeg'))]
    if image_files:
        print(f"✓ Found {len(image_files)} image(s) in images/")
        for img in image_files[:5]:  # Show first 5
            print(f"  - {img}")
        if len(image_files) > 5:
            print(f"  ... and {len(image_files) - 5} more")
    else:
        print("⚠ No images found in images/ directory")
        print("  Add your SVG, PNG, or JPG files to images/")
    
    print()
    print("="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Add your image to the images/ folder")
    print("2. Edit config.py with your desired settings")
    print("3. Run: manim -pql fourier_drawing.py FourierDrawing")
    print()
    print("For more help, see:")
    print("  - README.md for full documentation")
    print("  - EXAMPLES.md for configuration examples")
    print("  - config.py for all available settings")
    print()

if __name__ == '__main__':
    main()
