"""
CadQuery implementation of the replacement shelf pin.

The model replaces a fragile injection-molded shelf pin featuring a central thin rib
with a robust, full-width solid triangular gusset designed for 3D printing.
"""

import math
import cadquery as cq
from src.params import (
    OVERALL_HEIGHT,
    OVERALL_WIDTH,
    BACKPLATE_THICKNESS,
    SHELF_PROJECTION,
    SHELF_THICKNESS,
    PIN_OUTER_DIAMETER,
    PIN_INNER_DIAMETER,
    PIN_LENGTH,
    PIN_CHAMFER,
    PIN_NUM_RIBS,
    PIN_RIB_WIDTH,
    BACKPLATE_CORNER_RADIUS,
    SHELF_CORNER_RADIUS,
)


def _generate_rib_profile_points():
    """
    Generate 2D coordinates for the ribbed pin cross-section.
    Starts at +90 degrees (12 o'clock / +Z in functional orientation) so that a rib
    is positioned directly at the top of the pin, matching the design requirement.
    """
    r_in = PIN_INNER_DIAMETER / 2.0
    r_out = PIN_OUTER_DIAMETER / 2.0
    w2 = PIN_RIB_WIDTH / 2.0
    n = PIN_NUM_RIBS

    full_pts = []
    for i in range(n):
        # 12 o'clock start is pi / 2
        theta = i * 2.0 * math.pi / n + math.pi / 2.0
        d_theta_in = math.asin(min(w2 / r_in, 0.99))
        d_theta_out = math.asin(min(w2 / r_out, 0.99))

        # Root before rib
        full_pts.append((r_in * math.cos(theta - d_theta_in), r_in * math.sin(theta - d_theta_in)))
        # Crest left
        full_pts.append((r_out * math.cos(theta - d_theta_out), r_out * math.sin(theta - d_theta_out)))
        # Crest right
        full_pts.append((r_out * math.cos(theta + d_theta_out), r_out * math.sin(theta + d_theta_out)))
        # Root after rib
        full_pts.append((r_in * math.cos(theta + d_theta_in), r_in * math.sin(theta + d_theta_in)))

        # Intermediate root circle point between ribs for curvature stability
        theta_mid = (i + 0.5) * 2.0 * math.pi / n + math.pi / 2.0
        full_pts.append((r_in * math.cos(theta_mid), r_in * math.sin(theta_mid)))

    return full_pts


def create_shelf_pin():
    """
    Creates the shelf pin solid in functional/assembly orientation.
    - Global X: Width direction (-OVERALL_WIDTH/2 to +OVERALL_WIDTH/2)
    - Global Y: Back-to-front (+Y: pin into cabinet hole, -Y: shelf projection into room)
    - Global Z: Height direction (-OVERALL_HEIGHT/2 to +OVERALL_HEIGHT/2)
    """
    # 1. Side profile in YZ plane
    # The pin center is at (Y=0, Z=0) on the back face of the backplate.
    # The topmost rib is at Z = PIN_OUTER_DIAMETER / 2.
    # The shelf top surface is at Z = PIN_OUTER_DIAMETER / 2 + SHELF_THICKNESS.
    z_top_rib = PIN_OUTER_DIAMETER / 2.0
    z_shelf_top = z_top_rib + SHELF_THICKNESS
    z_shelf_bottom = z_top_rib
    z_backplate_top = OVERALL_HEIGHT / 2.0
    z_backplate_bottom = -OVERALL_HEIGHT / 2.0

    y_back_face = 0.0
    y_front_face = -BACKPLATE_THICKNESS
    y_shelf_tip = -(BACKPLATE_THICKNESS + SHELF_PROJECTION)

    # 2D profile polygon in YZ plane
    side_pts = [
        (y_back_face, z_backplate_top),
        (y_back_face, z_backplate_bottom),
        (y_front_face, z_backplate_bottom),
        (y_shelf_tip, z_shelf_bottom),
        (y_shelf_tip, z_shelf_top),
        (y_front_face, z_shelf_top),
        (y_front_face, z_backplate_top),
    ]

    # Extrude full width along X axis
    part = (
        cq.Workplane("YZ")
        .polyline(side_pts)
        .close()
        .extrude(OVERALL_WIDTH / 2.0, both=True)
    )

    # 2. Fillet backplate top & bottom corners and shelf front vertical corners
    part = part.edges("(|Y) and (>Z)").fillet(BACKPLATE_CORNER_RADIUS)
    part = part.edges("(|Y) and (<Z)").fillet(BACKPLATE_CORNER_RADIUS)
    part = part.edges("(|Z) and (<Y)").fillet(SHELF_CORNER_RADIUS)

    # 3. Add ribbed pin to backplate back face (>Y)
    rib_pts = _generate_rib_profile_points()
    part = (
        part.faces(">Y")
        .workplane(centerOption="ProjectedOrigin")
        .polyline(rib_pts)
        .close()
        .extrude(PIN_LENGTH)
    )

    # 4. Add 45-degree lead-in chamfer to the pin tip using an explicit revolve cutter
    r_out = PIN_OUTER_DIAMETER / 2.0
    ch = PIN_CHAMFER
    chamfer_cutter = (
        cq.Workplane("XY")
        .polyline([
            (r_out - ch, PIN_LENGTH),
            (r_out + 2.0, PIN_LENGTH),
            (r_out + 2.0, PIN_LENGTH - ch),
        ])
        .close()
        .revolve(360, (0, 0, 0), (0, 1, 0))
    )
    part = part.cut(chamfer_cutter)

    return part


def rotate_for_print(part_wp):
    """
    Rotates and positions the shelf pin for 3D printing:
    - Rotates 45 degrees around X axis so the flat hypotenuse of the triangular
      gusset rests directly on the print bed (Z = 0).
    - Pin points up at 45 degrees, which avoids layer-line shear weakness, requires
      no support material, and provides a large flat bed adhesion footprint (>270 mm^2).
    - Z-aligned so lowest face touches print bed at Z = 0.
    """
    # Rotate 45 degrees around X axis to seat the triangular hypotenuse flat on the bed
    rotated = part_wp.rotate((0, 0, 0), (1, 0, 0), 45)
    bb = rotated.val().BoundingBox()
    # Translate so bottom sits on Z = 0
    positioned = rotated.translate((0, 0, -bb.zmin))
    return positioned


if __name__ == "__main__":
    wp = create_shelf_pin()
    print("Created shelf pin:", wp.val().isValid())
    print_wp = rotate_for_print(wp)
    print("Created print-ready shelf pin:", print_wp.val().isValid())
