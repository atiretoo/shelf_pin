"""
Parameters for the 3D-printable replacement shelf pin.
All dimensions are in millimeters (mm).
"""

import os

# Project directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
EXPORTS_DIR = os.path.join(ROOT_DIR, "exports")

# Overall dimensions
OVERALL_HEIGHT = 25.2  # Total height of backplate (mm)
OVERALL_WIDTH = 12.5   # Total width of backplate and shelf (mm)
BACKPLATE_THICKNESS = 1.9  # Thickness of vertical backplate (mm)

# Shelf ledge dimensions
SHELF_PROJECTION = 15.7  # Shelf projection from front face of backplate (mm)
SHELF_THICKNESS = 1.9   # Thickness of shelf horizontal ledge (mm)

# Pin dimensions
PIN_OUTER_DIAMETER = 6.25  # Outside diameter across ribs (mm)
PIN_INNER_DIAMETER = 5.0   # Inside/root diameter of pin core (mm)
PIN_LENGTH = 8.0           # Length of pin protruding from backplate (mm)
PIN_CHAMFER = 1.0          # Lead-in chamfer at tip of pin (mm)
PIN_NUM_RIBS = 8           # Number of longitudinal ribs (splines)
PIN_RIB_WIDTH = 0.9        # Circumferential width of each rib (mm)

# Edge rounding & aesthetics
BACKPLATE_CORNER_RADIUS = 1.5  # Radius for rounding backplate corners (mm)
SHELF_CORNER_RADIUS = 1.2      # Radius for rounding shelf front corners (mm)

# Export mesh tolerances
STL_TOLERANCE = 0.01          # Linear deflection for tessellation (mm)
STL_ANGULAR_TOLERANCE = 0.1   # Angular deflection for tessellation (radians)
