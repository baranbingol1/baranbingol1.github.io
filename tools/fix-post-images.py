#!/usr/bin/env python3
"""Normalise image markup in _posts before committing.

Write posts however is comfortable:

    ![Açıklama](/images/my-post/plot.png "Görsel başlığı")

then run this from the repo root and it fills in the tedious parts:

    python tools/fix-post-images.py           # apply changes
    python tools/fix-post-images.py --check   # report only, exit 1 if stale

What it does
------------
* **alt text** — if the alt is empty but the image has a title (the bit in
  quotes, which renders as the visible caption), the title is copied into the
  alt. Images with neither are reported, never invented.
* **width / height** — read from the actual file, so the browser reserves the
  right space and the page doesn't reflow as images arrive.
* **loading="lazy"** — on every image except each post's first, which is
  usually above the fold; lazy-loading that one would delay the LCP.

It is idempotent — running it twice changes nothing — and it preserves any
other kramdown attributes you added yourself, e.g. `{: .my-class}`.

It also warns when a post opens with an image and has no `description:` front
matter. Jekyll's excerpt would be empty in that case, and the meta description
silently falls back to the site tagline.

Only `description:` should ever go in a post's front matter. Adding `title:`
or `layout:` disables jekyll-titles-from-headings and jekyll-default-layout,
which this site relies on because posts have no front matter.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

try:
    from PIL import Image
except ImportError:
    Image = None

REPO = pathlib.Path(__file__).resolve().parent.parent
POSTS = REPO / "_posts"

# ![alt](src "title"){: ial}   — title and IAL both optional
IMAGE_RE = re.compile(
    r'!\[(?P<alt>[^\]]*)\]\('
    r'(?P<src>[^)\s]+)'
    r'(?:\s+"(?P<title>[^"]*)")?\)'
    r'(?P<ial>\{:[^}]*\})?'
)
FENCE_RE = re.compile(r'^\s*(```|~~~)')
ATTR_RE = re.compile(r'[\w-]+="[^"]*"|[.#][\w-]+|\S+')
MANAGED = {"loading", "width", "height"}


def split_front_matter(text: str) -> tuple[str, str]:
    """Return (front_matter, body). Front matter is '' when absent."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    end = text.find("\n", end + 1)
    return text[:end + 1], text[end + 1:]


def dimensions(src: str):
    if src.startswith(("http://", "https://", "//")):
        return None
    path = REPO / src.lstrip("/")
    if not path.is_file() or Image is None:
        return None
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def rebuild_ial(existing: str | None, width, height, lazy: bool) -> str:
    """Merge our managed attributes into any the author wrote by hand."""
    kept = []
    if existing:
        for tok in ATTR_RE.findall(existing[2:-1].strip()):
            name = tok.split("=", 1)[0] if "=" in tok else None
            if name not in MANAGED:
                kept.append(tok)
    managed = []
    if lazy:
        managed.append('loading="lazy"')
    if width and height:
        managed.append(f'width="{width}" height="{height}"')
    attrs = kept + managed
    return "{: " + " ".join(attrs) + "}" if attrs else ""


def process(path: pathlib.Path, problems: list[str]):
    original = path.read_text(encoding="utf-8")
    front, body = split_front_matter(original)

    counter = [0]
    in_fence = False
    out_lines = []

    for line in body.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:                      # never touch images inside code
            out_lines.append(line)
            continue

        def repl(m):
            counter[0] += 1
            alt, src, title = m["alt"], m["src"], m["title"]
            if not alt.strip():
                if title and title.strip() and not title.startswith("Kaynak:"):
                    alt = title
                else:
                    problems.append(
                        f"{path.name}: image {counter[0]} ({src.split('/')[-1]}) "
                        f"has no alt text and no caption to borrow — add one by hand"
                    )
            dims = dimensions(src)
            if dims is None and not src.startswith(("http", "//")):
                problems.append(f"{path.name}: cannot read {src} — is the path right?")
            w, h = dims if dims else (None, None)
            ial = rebuild_ial(m["ial"], w, h, lazy=counter[0] > 1)
            out = f"![{alt}]({src}" + (f' "{title}"' if title else "") + ")"
            return out + ial

        out_lines.append(IMAGE_RE.sub(repl, line))

    new_body = "\n".join(out_lines)

    # A post opening with an image has an empty excerpt, so its meta
    # description falls back to the site tagline.
    stripped = new_body.lstrip("\n")
    after_h1 = re.sub(r'\A#[^\n]*\n+', '', stripped)
    if after_h1.lstrip().startswith("![") and "description:" not in front:
        problems.append(
            f"{path.name}: opens with an image but has no `description:` front "
            f"matter — its meta description will fall back to the site tagline"
        )

    return original, front + new_body, counter[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report what would change without writing; exit 1 if stale")
    args = ap.parse_args()

    if Image is None:
        print("! Pillow is not installed, so width/height cannot be filled in.")
        print("  pip install Pillow\n")

    posts = sorted(POSTS.glob("*.md"))
    if not posts:
        print(f"No posts found in {POSTS}")
        return 1

    problems: list[str] = []
    changed = []
    total_images = 0

    for path in posts:
        original, updated, count = process(path, problems)
        total_images += count
        if updated != original:
            changed.append(path.name)
            if not args.check:
                path.write_text(updated, encoding="utf-8", newline="\n")

    verb = "would update" if args.check else "updated"
    print(f"{len(posts)} posts, {total_images} images.")
    if changed:
        print(f"{verb} {len(changed)}:")
        for name in changed:
            print(f"  - {name}")
    else:
        print("Everything already up to date.")

    if problems:
        print("\nNeeds your attention:")
        for p in problems:
            print(f"  ! {p}")

    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
