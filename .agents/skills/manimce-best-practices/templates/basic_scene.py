"""2D scene template for this blog.

Save under tools/manim/scenes/ and render with:

    ./tools/manim/render.sh your_file.py YourScene images/my-post/your-clip
"""

from manim import *
from blog_theme import C


class YourScene(Scene):
    def construct(self):
        title = Text("Your title", color=C["text"], font_size=40)
        shape = Circle(color=C["accent"], fill_opacity=0.35)
        title.to_edge(UP)
        shape.move_to(ORIGIN)

        self.play(Write(title))
        self.wait(0.4)
        self.play(Create(shape))
        self.wait(0.4)
        self.play(shape.animate.scale(1.4).set_color(C["warn"]))
        self.wait(1.2)
