import subprocess
import os
import sys


# from scipy.fft import fft2, ifft2, fftshift, ifftshift

def jpg_to_svg_potrace(input_jpg_path, output_svg_path):
    """
    Converts a JPEG (raster) image to an SVG (vector) image using
    ImageMagick's 'magick' executable and the 'potrace' command-line tool.
    """
    if not os.path.exists(input_jpg_path):
        print(f"Error: Input file '{input_jpg_path}' not found.")
        return

    temp_pnm_path = "temp_input.pnm"
    
    # ----------------------------------------------------
    # STEP 1: Convert JPEG to PNM (using ImageMagick 'magick')
    # ----------------------------------------------------
    print(f"1/2: Converting '{input_jpg_path}' to temporary bitmap '{temp_pnm_path}'...")
    
    try:
        # **UPDATED:** Using 'magick' instead of 'convert'
        magick_command = [
            'magick', 
            input_jpg_path, 
            '-threshold', '50%', 
            temp_pnm_path
        ]
        
        # Run the command
        subprocess.run(magick_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    except subprocess.CalledProcessError as e:
        print(f"Error during ImageMagick 'magick' (Step 1). Is ImageMagick installed and available?")
        print(f"Details: {e.stderr.decode()}")
        if os.path.exists(temp_pnm_path):
            os.remove(temp_pnm_path)
        return

    except FileNotFoundError:
        print("Error: The 'magick' command (ImageMagick) was not found. Please ensure it is installed.")
        if os.path.exists(temp_pnm_path):
            os.remove(temp_pnm_path)
        return

    # ----------------------------------------------------
    # STEP 2: Vectorize PNM to SVG (using 'potrace')
    # ----------------------------------------------------
    print(f"2/2: Vectorizing bitmap to SVG '{output_svg_path}'...")

    try:
        potrace_command = [
            'potrace', 
            temp_pnm_path, 
            '-s',           
            '-o', output_svg_path
        ]
        
        subprocess.run(potrace_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"\n✅ SUCCESS: Vectorization complete. SVG saved to '{output_svg_path}'")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during Potrace (Step 2).")
        print(f"Details: {e.stderr.decode()}")
        
    finally:
        if os.path.exists(temp_pnm_path):
            os.remove(temp_pnm_path)
            

# --- Example Usage ---
if __name__ == "__main__":
    input_file = "my_photo.jpg" 
    output_file = "my_photo_traced.svg"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if len(sys.argv) > 2:
             output_file = sys.argv[2]

    print(f"Starting vectorization of {input_file}...")
    jpg_to_svg_potrace(input_file, output_file)



