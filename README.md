# Heavy-Duty Replacement Shelf Pin

This repository contains a parametric [CadQuery](https://github.com/CadQuery/cadquery) model for a heavy-duty 3D-printable replacement shelf pin.

The design replaces the typical injection-molded shelf pin—which often fails at its thin central rib—with a solid triangular gusset spanning the full width of the support.

## Key Dimensions & Features

- **Overall Height**: 25.2 mm (backplate height)
- **Overall Width**: 12.5 mm (full width of backplate and support)
- **Backplate Thickness**: 1.9 mm
- **Shelf Projection**: 15.7 mm (measured from front face of backplate)
- **Shelf Thickness**: 1.9 mm (top of shelf sits 1.9 mm above topmost rib)
- **Pin Outer Diameter**: 6.35 mm (exactly 1/4" across longitudinal ribs/splines for snug press-fit in deburred holes)
- **Pin Inner Diameter**: 5.0 mm (root diameter of pin core)
- **Pin Length**: 8.0 mm with a 1.0 mm 45° lead-in chamfer for easy cabinet insertion
- **Rib Configuration**: 8 longitudinal ribs clocked by 22.5° so the topmost point falls between ribs, preventing heat buildup and nozzle blob defects during 3D printing.
- **Full-Width Solid Gusset**: Replaces the fragile single central rib with a continuous solid triangular wedge across the entire 12.5 mm width.
- **3D Print Orientation**: Oriented with the flat hypotenuse of the triangular gusset resting directly on the bed ($Z = 0$) and the pin angled upwards at 45°. This orientation:
  - Eliminates layer-line shear weakness through the pin.
  - Requires zero support material (all upward faces are at or above 45°).
  - Provides a large flat bed adhesion footprint (>275 mm²).

## Project Structure

```
shelf_pin/
├── assets/                          # Reference images of original part
│   ├── shelf_pin_front.jpg
│   ├── shelf_pin_back.jpg
│   └── shelf_pin_side.jpg
├── exports/                         # Generated STL and STEP files
│   ├── shelf_pin.step               # Functional / CAD orientation
│   ├── shelf_pin.stl
│   ├── shelf_pin_print_ready.step   # 3D print orientation (Z = 0 at bed, pin +Z)
│   └── shelf_pin_print_ready.stl
├── src/
│   ├── __init__.py
│   ├── params.py                    # Parametric dimensions & tolerances
│   └── shelf_pin.py                 # CadQuery model generation & rotation helpers
├── tests/
│   ├── __init__.py
│   └── test_shelf_pin.py            # Automated geometry validation tests
├── export_all.py                    # Script to regenerate STEP and STL outputs
├── CODE_OF_CONDUCT.md
├── COPYING                          # GNU AGPLv3 for Python source code
├── LICENSE                          # CC BY-SA 4.0 for hardware / 3D models
└── README.md
```

## Modeling Guidelines & Best Practices

When designing parts and assemblies in this project:

- **BRep over CSG**: Prioritize Boundary Representation modeling (selecting faces/edges and applying features such as extrude, hole, fillet, shell) over pure CSG boolean operations (`union`, `cut`) to maintain robust, parametric geometry.
- **Coordinate Systems & Workplanes**:
  - Remember the right-hand cyclic order ($X \rightarrow Y \rightarrow Z \rightarrow X$).
  - Planes `"XY"`, `"YZ"`, and `"ZX"` have $+Z$, $+X$, and $+Y$ normal vectors respectively.
  - Avoid `"XZ"` if positive $+Y$ extrusion is expected; use `"ZX"` instead (where local coordinates map as $(z, x)$) or select faces directly with `.faces(">Y").workplane()`.
- **Selectors**:
  - Prefer stable geometric selectors (`>Z`, `<Z`, `|X`, etc.) and tagging (`.tag("name")`) over fragile numeric indices (`>>Z[0]`).
  - Explicitly specify `centerOption` (e.g. `CenterOfBoundBox` or `ProjectedOrigin`) when face centering behavior is critical.

## Running Tests & Exports

### Requirements
- Python 3.9+
- [CadQuery](https://github.com/CadQuery/cadquery)

### Run Unit Tests
```bash
python -m unittest discover tests
```

### Export STL and STEP Files
```bash
python export_all.py
```

## Development & AI Policy: The "Centaur" Approach

This project is developed using a collaborative human-AI workflow. The code, architecture, and documentation were written and refined with the assistance of advanced AI models. 

I approach AI not as a tool for blind self-automation, but as a collaborative interaction. I aspire to be a [centaur](https://mitsloan.mit.edu/ideas-made-to-matter/3-ways-to-use-ai-are-you-a-cyborg-a-centaur-or-a-self-automator), "... maintain[ing] structured and controlled interactions with AI, harnessing it as a tool for targeted efficiency". I acknowledge that when learning a new domain I might be a cyborg "... collaborat[ing] closely with the AI tool -- probing its suggestions, allowing it to lead the way, and taking its advice on some occasions while pushing back against it on others." Both are OK. In this model, the AI acts as a high-powered pair-programming partner. It helps me rapidly explore and develop my own understanding of complex topics. Meanwhile, I hold the strategic vision, conduct the physical testing/validation, and apply and build domain knowledge as I go.

For rules regarding AI-assisted contributions from the community, please see the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project utilizes a **Dual License** structure to comply with both software and open-source hardware best practices. These specific open-source licenses were chosen to support the transition to an anarchist economy—promoting mutual aid, free distribution of information, and breaking down artificial scarcity.

*   **Software (Python Code):** All source code in this repository is licensed under the [GNU Affero General Public License v3.0 (AGPLv3)](COPYING). This ensures that any modifications to the code remain open-source and provides explicit patent protections.
*   **Hardware (3D Models):** The generated output files (STL and STEP files) are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](LICENSE). This is the standard license for the 3D printing community.
