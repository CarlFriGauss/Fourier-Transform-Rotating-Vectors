"""
Command-line utility for Fourier Drawing Animation

Usage:
    python run.py [image_path] [options]

Examples:
    python run.py images/my_image.svg
    python run.py images/photo.jpg --vectors 500 --samples 10000
    python run.py images/logo.png --duration 30 --quality high
"""

import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Create Fourier epicycle animations from images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py images/my_image.svg
  python run.py images/photo.jpg --vectors 500 --samples 10000
  python run.py images/logo.png --duration 30 --quality high
        """
    )
    
    parser.add_argument('image', nargs='?', help='Path to image file (SVG, PNG, or JPG)')
    parser.add_argument('-v', '--vectors', type=int, help='Number of epicycles')
    parser.add_argument('-s', '--samples', type=int, help='Number of sample points')
    parser.add_argument('-d', '--duration', type=float, help='Animation duration in seconds')
    parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high', '4k'], 
                       default='medium', help='Render quality')
    parser.add_argument('--no-circles', action='store_true', help='Hide circles')
    parser.add_argument('--no-arrows', action='store_true', help='Hide arrows')
    parser.add_argument('--preview', action='store_true', help='Preview without saving')
    parser.add_argument('--convert', help='Convert PNG/JPG to SVG first')
    
    args = parser.parse_args()
    
    # Handle image conversion
    if args.convert:
        print(f"Converting {args.image} to SVG...")
        from helpers.vectorize import jpg_to_svg_potrace
        output_svg = args.convert if args.convert.endswith('.svg') else args.convert + '.svg'
        jpg_to_svg_potrace(args.image, output_svg)
        args.image = output_svg
    
    # Update config if arguments provided
    if args.image:
        update_config('IMAGE_PATH', f"'{args.image}'")
    if args.vectors:
        update_config('N_VECTORS', str(args.vectors))
    if args.samples:
        update_config('NUM_SAMPLES', str(args.samples))
    if args.duration:
        update_config('ANIMATION_DURATION', str(args.duration))
    if args.no_circles:
        update_config('DRAW_CIRCLES', 'False')
    if args.no_arrows:
        update_config('DRAW_ARROWS', 'False')
    
    # Build manim command
    quality_flags = {
        'low': '-ql',
        'medium': '-qm',
        'high': '-qh',
        '4k': '-qk'
    }
    
    quality_flag = quality_flags[args.quality]
    preview_flag = '-p' if args.preview or not args.image else '-p'
    
    manim_cmd = f'manim {preview_flag}{quality_flag} fourier_drawing.py FourierDrawing'
    
    print(f"\n{'='*60}")
    print("Running Fourier Drawing Animation")
    print(f"{'='*60}")
    print(f"Command: {manim_cmd}\n")
    
    os.system(manim_cmd)

def update_config(key, value):
    """Update a value in config.py"""
    with open('config.py', 'r') as f:
        lines = f.readlines()
    
    with open('config.py', 'w') as f:
        for line in lines:
            if line.strip().startswith(key + ' ='):
                f.write(f"{key} = {value}\n")
            else:
                f.write(line)

if __name__ == '__main__':
    main()
