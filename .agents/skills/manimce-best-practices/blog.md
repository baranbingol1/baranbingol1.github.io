# This blog's Manim pipeline

Read this file before any other rule in this skill. The `rules/` and `examples/` files teach the Manim CE API. They do not describe how this site ships a clip.

`npx skills update manimce-best-practices` will restore upstream and wipe this overlay. Re-apply `blog.md` and the SKILL.md "This repository" section after an update.

## Where files go

| What | Where |
|---|---|
| Scene | `tools/manim/scenes/<name>.py` |
| Palette | `tools/manim/blog_theme.py` (`C["text"]`, `C["accent"]`, …) |
| Render | `./tools/manim/render.sh <scene.py> <SceneName> <output-stem>` |
| Outputs | `images/<post>/<stem>-light.webp` and `-dark.webp` |
| Embed | `{% include anim.html %}` |

Do not put scenes in the skill's `examples/` or `templates/` folders. Do not add Manim to `docker-compose.yml` (that is the Jekyll preview). Do not run `manim` on the host.

## Scene file

```python
from manim import *
from blog_theme import C


class GradientStep(Scene):
    def construct(self):
        title = Text("One step", color=C["text"], font_size=36)
        arrow = Arrow(LEFT, RIGHT, color=C["accent"])
        title.to_edge(UP)
        self.play(Write(title))
        self.play(GrowArrow(arrow))
        self.wait(1.5)
```

`from blog_theme import C` is required. Importing it sets the background from `BLOG_THEME`. `render.sh` runs the file twice with `BLOG_THEME=light` then `dark`.

## Colour

Chrome (text, axes, arrows, labels) uses `C` only:

- `C["bg"]` `C["bg_elevated"]` `C["text"]` `C["muted"]` `C["accent"]` `C["warn"]` `C["border"]`

Hexes match `assets/main.scss`. Do not use Manim's `BLUE`, `YELLOW`, `WHITE`, `BLACK` for chrome. Data series may use distinct hues if the meaning needs more than accent/warn.

The cream mat on static plots is for white matplotlib exports. Themed clips skip it (`figure.anim`). Do not render transparent (`-t`); ink has to change with the theme, not just the page background.

## Render

```bash
./tools/manim/render.sh gradient.py GradientStep images/my-post/gradient
./tools/manim/render.sh --quick gradient.py GradientStep images/my-post/gradient
```

`--quick` is `-ql` for iteration. The default is 1280×720, 24 fps, looped WebP.

Ignore `rules/cli.md` render recipes (`manim -pql`, `--format gif`, `-qh`). Those fight this pipeline. GIF is not the delivery format.

After a successful render, embed:

```liquid
{% include anim.html
   light="/images/my-post/gradient-light.webp"
   dark="/images/my-post/gradient-dark.webp"
   alt="A single gradient step moving toward a minimum"
   caption="One gradient step."
   width="1280"
   height="720"
%}
```

Pass `loading="eager"` if it is the post's first image. `tools/fix-post-images.py` does not see includes; write width/height yourself (1280×720 at default quality).

Do not use `<picture media="(prefers-color-scheme: dark)">`. The site toggle sets `data-theme` on `<html>`, which is what the CSS keys off.

## Taste

- 6–12 seconds. Loop-friendly.
- Last frame is the takeaway. Do not `FadeOut` everything at the end.
- Prefer 2D `Scene`. `ThreeDScene` / `MovingCameraScene` only if the user asks.
- One idea per clip. Put the explanation in the surrounding prose, not as a title card that lasts the whole animation.
- Column is 42rem (~672px). 720p is already more than enough; do not render 1080p or 4K.

## API lookup

After this file, read the matching `rules/*.md` for the mobject or animation you need. Skill examples use the default Manim palette on purpose (they test the API). Copy structure from them, not their colours, and not their `manim -pql` footer comments.
