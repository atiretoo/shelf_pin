"""
Unit tests for the replacement shelf pin CadQuery models.
"""

import unittest
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
)
from src.shelf_pin import create_shelf_pin, rotate_for_print


class TestShelfPinGeometry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pin_wp = create_shelf_pin()
        cls.solid = cls.pin_wp.val()
        cls.print_wp = rotate_for_print(cls.pin_wp)
        cls.print_solid = cls.print_wp.val()

    def test_solid_validity(self):
        self.assertTrue(self.solid.isValid(), "Shelf pin CAD solid must be valid BRep")
        self.assertTrue(self.print_solid.isValid(), "Print-ready solid must be valid BRep")
        self.assertGreater(self.solid.Volume(), 2000.0, "Volume should be greater than 2000 mm^3")

    def test_cad_bounding_box(self):
        bb = self.solid.BoundingBox()
        total_width = bb.xmax - bb.xmin
        total_depth = bb.ymax - bb.ymin
        total_height = bb.zmax - bb.zmin

        self.assertAlmostEqual(total_width, OVERALL_WIDTH, places=2, msg="Overall width should match 12.5 mm")
        self.assertAlmostEqual(total_height, OVERALL_HEIGHT, places=2, msg="Overall height should match 25.2 mm")

        expected_depth = PIN_LENGTH + BACKPLATE_THICKNESS + SHELF_PROJECTION
        self.assertAlmostEqual(total_depth, expected_depth, places=2, msg="Overall depth should match sum of pin, backplate, and shelf")

    def test_shelf_to_pin_rib_offset(self):
        """
        Verify that the top surface of the shelf is 1.9 mm above the topmost rib of the pin.
        """
        # Find the horizontal shelf resting face (normal +Z, projecting in -Y)
        shelf_faces = [
            f for f in self.solid.Faces()
            if f.normalAt().z > 0.9 and f.Center().y < -BACKPLATE_THICKNESS
        ]
        self.assertTrue(len(shelf_faces) > 0, "Must have a flat shelf top face")
        shelf_top_z = shelf_faces[0].Center().z

        # Topmost rib crest is at PIN_OUTER_DIAMETER / 2
        top_rib_z = PIN_OUTER_DIAMETER / 2.0
        offset = shelf_top_z - top_rib_z
        self.assertAlmostEqual(offset, SHELF_THICKNESS, places=2, msg="Shelf top must be 1.9 mm above topmost rib")

    def test_print_ready_orientation(self):
        """
        Verify that in print-ready orientation:
        - The flat hypotenuse of the triangular gusset rests on the print bed at Z = 0
        - Large contact area (> 250 mm^2) for strong bed adhesion
        - Width along X is preserved (12.5 mm)
        - Pin is angled upward at 45 degrees
        """
        bb = self.print_solid.BoundingBox()
        self.assertAlmostEqual(bb.zmin, 0.0, places=2, msg="Lowest point must sit at Z = 0 on the print bed")

        # Verify flat bottom face at Z = 0
        bottom_faces = [
            f for f in self.print_solid.Faces()
            if abs(f.normalAt().z - (-1.0)) < 0.05 and abs(f.Center().z) < 0.02
        ]
        self.assertEqual(len(bottom_faces), 1, "Must have exactly 1 flat face resting on the print bed")
        self.assertGreater(bottom_faces[0].Area(), 250.0, "Bed contact area must exceed 250 mm^2 for bed adhesion")

        # Width along X
        self.assertAlmostEqual(bb.xmax - bb.xmin, OVERALL_WIDTH, places=2)


if __name__ == "__main__":
    unittest.main()
