# Reproducible Manim CE renderer for this blog.
# Bump the FROM tag deliberately when you want a new engine.
FROM manimcommunity/manim:stable

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*
USER manimuser
