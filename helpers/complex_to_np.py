"""
Utility functions for coordinate conversion.

This module provides helper functions to convert between complex numbers
and Manim's 3D coordinate system.
"""

import numpy as np


def complex_to_np(complex_number):
    """
    Convert a complex number to a Manim 3D coordinate array.
    
    Args:
        complex_number: A complex number (x + iy)
        
    Returns:
        numpy.ndarray: 3D coordinate [x, y, 0] for Manim
        
    Example:
        >>> z = 3 + 4j
        >>> complex_to_np(z)
        array([3., 4., 0.])
    """
    return np.array([complex_number.real, complex_number.imag, 0])