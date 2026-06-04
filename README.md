# ColoLabs

ColoLabs is a creative umbrella and personal workspace where curiosity turns into output. It is a place for experimenting across formats: building tools and apps, creating AI-assisted content and short videos, exploring technical domains such as IT infrastructure, and writing down ideas worth developing. The site is intentionally flexible: a playground for iteration, learning, and expression where ideas can be tested, shaped, and sometimes turned into something real.

This repository contains the source for the ColoLabs website. It is a [Pelican](https://getpelican.com/) static site: source content lives under `content/`, Pelican renders it with the configured theme and settings, and generated HTML is written to `output/`.

## Project Structure

- `content/articles/` - Blog posts and dated article content.
- `content/pages/` - Static pages such as about, projects, or other standalone site pages.
- `content/images/` - Images used by articles, pages, and site content.
- `themes/svbhack/` - The Pelican theme used to render the site.
- `output/` - Generated site output. This is rebuilt by Pelican and used for publishing.

## Local Workflow

The Makefile wraps the common Pelican commands:

- `make html` - Build the site into `output/` using `pelicanconf.py`.
- `make clean` - Remove the generated `output/` directory.
- `make regenerate` - Watch source files and rebuild when they change.
- `make publish` - Build the site using production settings from `publishconf.py`.
- `make serve PORT=8000` - Build and serve the site at `http://localhost:8000`.
- `make devserver PORT=8000` - Serve the site and regenerate it when files change.
- `make github` - Build with production settings, import `output/` into the `gh-pages` branch, and push it.

If `pelican` is not available on `PATH`, activate the local virtual environment first:

```sh
source .venv/bin/activate
```

Or pass the Pelican executable explicitly:

```sh
make html PELICAN=.venv/bin/pelican
```
