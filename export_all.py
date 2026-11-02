"""
Export script for the 3D-printable replacement shelf pin.
Generates STEP and STL files for both functional (CAD) and print-ready orientations.
"""

import os
import cadquery as cq
from src.params import EXPORTS_DIR, STL_TOLERANCE, STL_ANGULAR_TOLERANCE
from src.shelf_pin import create_shelf_pin, rotate_for_print


def export_all():
    os.makedirs(EXPORTS_DIR, exist_ok=True)

    print("Generating shelf pin solid...")
    pin_wp = create_shelf_pin()

    # 1. Export STEP (functional/CAD orientation)
    step_path = os.path.join(EXPORTS_DIR, "shelf_pin.step")
    cq.exporters.export(pin_wp, step_path)
    print(f"  -> Exported STEP (CAD space): {step_path}")

    # 2. Export STL (functional/CAD orientation)
    stl_path = os.path.join(EXPORTS_DIR, "shelf_pin.stl")
    cq.exporters.export(
        pin_wp,
        stl_path,
        cq.exporters.ExportTypes.STL,
        tolerance=STL_TOLERANCE,
        angularTolerance=STL_ANGULAR_TOLERANCE,
    )
    print(f"  -> Exported STL (CAD space): {stl_path}")

    # 3. Export print-ready orientation: pin pointing UP (+Z), triangular part facing bed
    print("Generating print-ready orientation...")
    print_wp = rotate_for_print(pin_wp)

    step_print_path = os.path.join(EXPORTS_DIR, "shelf_pin_print_ready.step")
    cq.exporters.export(print_wp, step_print_path)
    print(f"  -> Exported STEP (Print-ready): {step_print_path}")

    stl_print_path = os.path.join(EXPORTS_DIR, "shelf_pin_print_ready.stl")
    cq.exporters.export(
        print_wp,
        stl_print_path,
        cq.exporters.ExportTypes.STL,
        tolerance=STL_TOLERANCE,
        angularTolerance=STL_ANGULAR_TOLERANCE,
    )
    print(f"  -> Exported STL (Print-ready): {stl_print_path}")

    print("\nAll exports successfully generated in exports/!")


if __name__ == "__main__":
    export_all()
