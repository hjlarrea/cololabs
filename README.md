# ColoLabs

ColoLabs is a creative umbrella and personal workspace where curiosity turns into output. It is a place for experimenting across formats: building tools and apps, creating AI-assisted content and short videos, exploring technical domains such as IT infrastructure, and writing down ideas worth developing. The site is intentionally flexible: a playground for iteration, learning, and expression where ideas can be tested, shaped, and sometimes turned into something real.

This repository contains the source for the ColoLabs website. It is a [Pelican](https://getpelican.com/) static site: source content lives under `content/`, Pelican renders it with the configured theme and settings, and generated HTML is written to `output/`.

## Preview and publish

1. Create a branch and PR in [cololabs-preview](https://github.com/hjlarrea/cololabs-preview).
2. Every PR opening/update builds [the shared preview](https://preview.cololabs.com.ar), with no branch-name restrictions.
3. Review and merge into preview main in GitHub.
4. Locally, pull preview main and run `git push production main`.
5. GitHub Actions builds and publishes [production](https://cololabs.com.ar).

Articles, theme and page changes use the same flow. See the
[complete procedure](docs/publishing.md) for the two-remotes setup, local preview,
review and releases, and [AI contributor instructions](docs/openclaw-editorial.md).

## Local build

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PREVIEW_SITEURL=http://localhost:8000 make preview PELICAN=.venv/bin/pelican
python3 -m http.server 8000 --directory output
```

Open http://localhost:8000. Rebuild after editing and refresh the browser.
`make html` builds development output; `make publish` builds production output.
Neither command deploys. Deployment happens automatically after the production push.
