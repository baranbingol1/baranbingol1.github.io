"""Colour tokens for blog Manim scenes.

Hex values must match `:root[data-theme]` in assets/main.scss.
`render.sh` sets BLOG_THEME to `light` or `dark` before each pass.
Importing this module also sets Manim's background colour.
"""

from __future__ import annotations

import os

from manim import config

LIGHT = {
    "bg": "#fcfbf9",
    "bg_elevated": "#f3f1ec",
    "text": "#17161a",
    "muted": "#635f57",
    "accent": "#805b00",
    "warn": "#a2401f",
    "border": "#e4e0d6",
}

DARK = {
    "bg": "#141416",
    "bg_elevated": "#1c1c1f",
    "text": "#e6e3dd",
    "muted": "#a49f96",
    "accent": "#d8ab52",
    "warn": "#e0876f",
    "border": "#2b2b2f",
}

THEME = os.environ.get("BLOG_THEME", "light")
if THEME not in ("light", "dark"):
    raise RuntimeError(f"BLOG_THEME must be 'light' or 'dark', got {THEME!r}")

C = DARK if THEME == "dark" else LIGHT
config.background_color = C["bg"]
