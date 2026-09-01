#!/usr/bin/env bash
# Render a scene once per theme and write looped WebPs for the blog.
#
#   ./tools/manim/render.sh [--quick] <scene.py> <SceneName> <output-stem>
#
# scene.py lives in tools/manim/scenes/.
# output-stem is relative to the repo root, with no suffix:
#   images/my-post/gradient
# writes
#   images/my-post/gradient-light.webp
#   images/my-post/gradient-dark.webp
set -euo pipefail

QUICK=0
if [[ "${1:-}" == "--quick" ]]; then
  QUICK=1
  shift
fi

if [[ $# -ne 3 ]]; then
  sed -n '2,14p' "$0" | sed 's/^# \?//'
  exit 2
fi

SCENE_FILE=$1
SCENE_NAME=$2
STEM=$3

MANIM_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$MANIM_DIR/../.." && pwd)"
SCENE_PATH="$MANIM_DIR/scenes/$SCENE_FILE"
IMAGE_NAME="${MANIM_IMAGE:-baran-blog-manim:latest}"
QUALITY="m"
[[ "$QUICK" -eq 1 ]] && QUALITY="l"

if [[ ! -f "$SCENE_PATH" ]]; then
  echo "No scene at $SCENE_PATH" >&2
  exit 1
fi

if [[ "$STEM" == /* || "$STEM" == *..* ]]; then
  echo "output-stem must be a relative path with no .." >&2
  exit 1
fi

if ! command -v docker >/dev/null; then
  echo "Docker is required to render (manimcommunity/manim)." >&2
  exit 1
fi

docker build -q -t "$IMAGE_NAME" "$MANIM_DIR" >/dev/null

mkdir -p "$ROOT/$(dirname "$STEM")"

run_theme() {
  local theme=$1
  local dest="$ROOT/${STEM}-${theme}.webp"
  local tmp_webp=".render-${theme}.webp"

  echo "Rendering $SCENE_NAME ($theme)"
  docker run --rm \
    --user "$(id -u):$(id -g)" \
    -e HOME=/tmp \
    -e PYTHONPATH=/manim \
    -e BLOG_THEME="$theme" \
    -v "$MANIM_DIR:/manim" \
    "$IMAGE_NAME" \
    bash -c "
      set -euo pipefail
      manim render --quality $QUALITY --fps 24 --format mp4 --media_dir /tmp/m \
        -o clip --disable_caching 'scenes/$SCENE_FILE' '$SCENE_NAME'
      mp4=\$(find /tmp/m -name 'clip.mp4' | head -n1)
      test -n \"\$mp4\"
      ffmpeg -y -i \"\$mp4\" -vf 'fps=24,scale=1280:-2:flags=lanczos' \
        -an -loop 0 -c:v libwebp -q:v 60 '/manim/$tmp_webp'
    "

  mv -f "$MANIM_DIR/$tmp_webp" "$dest"
  echo "Wrote $dest"
}

run_theme light
run_theme dark
echo "Done. Embed with {% include anim.html light=\"/${STEM}-light.webp\" dark=\"/${STEM}-dark.webp\" ... %}"
