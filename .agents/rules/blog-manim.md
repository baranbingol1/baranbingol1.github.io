---
description: Dual-theme Manim clips for this Jekyll blog. Read on any animation, GIF, or in-post diagram request.
alwaysApply: true
---

# Blog animations

If the user wants a Manim clip, animated GIF, WebP, or an in-post animation, do not improvise a pipeline. Read `.agents/skills/manimce-best-practices/blog.md` first, then the matching files under that skill's `rules/` for API.

- Scenes live in `tools/manim/scenes/`. Import `from blog_theme import C`. Chrome colours come from `C`, not `BLUE`/`YELLOW`.
- Render with `./tools/manim/render.sh <scene.py> <SceneName> images/<post>/<stem>`. That writes `<stem>-light.webp` and `<stem>-dark.webp`.
- Embed with `{% include anim.html %}`. Do not use `![...](file.gif)`, `<picture>`, or `prefers-color-scheme`.
- Do not run `manim` on the host. Do not add Manim to `docker-compose.yml`. Do not `FadeOut` the last frame.

Full rules, the include snippet, and taste notes are in `blog.md`.
