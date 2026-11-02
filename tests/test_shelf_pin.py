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
        - The part rests on the bed at Z = 0
        - Pin points straight up in +Z direction
        - Total Z height corresponds to depth (triangular face to pin tip)
        """
        bb = self.print_solid.BoundingBox()
        self.assertAlmostEqual(bb.zmin, 0.0, places=2, msg="Lowest point must sit at Z = 0 on the print bed")

        # The highest face in +Z must be the tip of the pin
        top_face = self.print_wp.faces(">Z").val()
        pin_tip_z = top_face.Center().z
        self.assertAlmostEqual(pin_tip_z, bb.zmax, places=1)

        # Width and backplate height along X and Y
        self.assertAlmostEqual(bb.xmax - bb.xmin, OVERALL_WIDTH, places=2)
        self.assertAlmostEqual(bb.ymax - bb.ymin, OVERALL_HEIGHT, places=2)


if __name__ == "__main__":
    unittest.main()
