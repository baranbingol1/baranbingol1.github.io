---
name: manimce-best-practices
description: |
  Use when writing or rendering Manim animations for this blog: Manim, ManimCE, Scene, MathTex, tools/manim, animated WebP, GIF, light/dark clips.

  Manim Community Edition API plus this repo's dual-theme WebP pipeline. Not ManimGL (manimlib / manimgl).
---

## This repository

**Read [blog.md](blog.md) first.** Every shipped clip goes through `tools/manim/render.sh` and `{% include anim.html %}`. Do not run `manim` on the host, do not emit GIF as the page asset, do not use `BLUE`/`YELLOW` for chrome.

The rest of this skill is the Manim CE API cookbook.

## How to use

Read individual rule files for detailed explanations and code examples:

### Core Concepts
- [rules/scenes.md](rules/scenes.md) - Scene structure, construct method, and scene types
- [rules/mobjects.md](rules/mobjects.md) - Mobject types, VMobject, Groups, and positioning
- [rules/animations.md](rules/animations.md) - Animation classes, playing animations, and timing

### Creation & Transformation
- [rules/creation-animations.md](rules/creation-animations.md) - Create, Write, FadeIn, DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) - Transform, ReplacementTransform, morphing
- [rules/animation-groups.md](rules/animation-groups.md) - AnimationGroup, LaggedStart, Succession

### Text & Math
- [rules/text.md](rules/text.md) - Text mobjects, fonts, and styling
- [rules/latex.md](rules/latex.md) - MathTex, Tex, LaTeX rendering, and coloring formulas
- [rules/text-animations.md](rules/text-animations.md) - Write, AddTextLetterByLetter, TypeWithCursor

### Styling & Appearance
- [rules/colors.md](rules/colors.md) - Color constants, gradients, and color manipulation
- [rules/styling.md](rules/styling.md) - Fill, stroke, opacity, and visual properties

### Positioning & Layout
- [rules/positioning.md](rules/positioning.md) - move_to, next_to, align_to, shift methods
- [rules/grouping.md](rules/grouping.md) - VGroup, Group, arrange, and layout patterns

### Coordinate Systems & Graphing
- [rules/axes.md](rules/axes.md) - Axes, NumberPlane, coordinate systems
- [rules/graphing.md](rules/graphing.md) - Plotting functions, parametric curves
- [rules/3d.md](rules/3d.md) - ThreeDScene, 3D axes, surfaces, camera orientation

### Animation Control
- [rules/timing.md](rules/timing.md) - Rate functions, easing, run_time, lag_ratio
- [rules/updaters.md](rules/updaters.md) - Updaters, ValueTracker, dynamic animations
- [rules/camera.md](rules/camera.md) - MovingCameraScene, zoom, pan, frame manipulation

### Configuration & CLI
- [rules/cli.md](rules/cli.md) - Upstream CLI. For this blog, ignore it and use `tools/manim/render.sh` (see [blog.md](blog.md)).
- [rules/config.md](rules/config.md) - Configuration system, manim.cfg, settings

### Shapes & Geometry
- [rules/shapes.md](rules/shapes.md) - Circle, Square, Rectangle, Polygon, and geometric primitives
- [rules/lines.md](rules/lines.md) - Line, Arrow, Vector, DashedLine, and connectors

## Working Examples

Complete, tested example files demonstrating common patterns. Copy structure, not their default palette, and not their `manim -pql` footers.

- [examples/basic_animations.py](examples/basic_animations.py) - Shape creation, text, lagged animations, path movement
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX equations, color-coded math, derivations
- [examples/updater_patterns.py](examples/updater_patterns.py) - ValueTracker, dynamic animations, physics simulations
- [examples/graph_plotting.py](examples/graph_plotting.py) - Axes, functions, areas, Riemann sums, polar plots
- [examples/3d_visualization.py](examples/3d_visualization.py) - ThreeDScene, surfaces, 3D camera, parametric curves

## Scene Templates

Start from [templates/basic_scene.py](templates/basic_scene.py) and save the result under `tools/manim/scenes/`. Camera and 3D templates are API references only; skip them unless the user asks.

- [templates/basic_scene.py](templates/basic_scene.py) - 2D scene using `blog_theme.C`
- [templates/camera_scene.py](templates/camera_scene.py) - MovingCameraScene with zoom/pan
- [templates/threed_scene.py](templates/threed_scene.py) - 3D scene with surfaces and camera rotation

## Quick Reference

### Basic Scene Structure
```python
from manim import *
from blog_theme import C

class MyScene(Scene):
    def construct(self):
        circle = Circle(color=C["accent"])
        label = Text("circle", color=C["text"])
        self.play(Create(circle), Write(label))
        self.wait(1)
```

### Render Command

```bash
./tools/manim/render.sh scene.py MyScene images/my-post/scene
./tools/manim/render.sh --quick scene.py MyScene images/my-post/scene
```

Then `{% include anim.html %}`. Details in [blog.md](blog.md).

### Key Differences from 3b1b/ManimGL

| Feature | Manim Community | 3b1b/ManimGL |
|---------|-----------------|--------------|
| Import | `from manim import *` | `from manimlib import *` |
| CLI | `manim` (this repo: `render.sh`) | `manimgl` |
| Math text | `MathTex(r"\pi")` | `Tex(R"\pi")` |
| Scene | `Scene` | `InteractiveScene` |
| Package | `manim` (PyPI) | `manimgl` (PyPI) |

### Common Pitfalls to Avoid

1. **Version confusion.** `from manim import *` is Community. `from manimlib import *` is ManimGL. This repo is Community only.
2. **Host CLI.** There is no local `manim`. Docker via `render.sh`.
3. **GIF as the page asset.** Manim can write GIF. The blog ships WebP.
4. **`prefers-color-scheme`.** The toggle sets `data-theme`. Use `anim.html`, not `<picture>`.
5. **Default palette.** `BLUE`/`YELLOW` on a cream or charcoal page looks like a sticker. Use `C`.
6. **Empty last frame.** A looping clip that fades to nothing flashes every cycle.
7. **Transparent background.** Ink still needs a theme. Two full renders, not `-t`.
