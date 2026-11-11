# Instructions for OpenClaw article proposals

Work only in a clone of `hjlarrea/cololabs-preview`, using credentials restricted
to that repository. Read `docs/publishing.md` before starting.

1. Ask the owner for the article topic, intended audience and any editorial constraints
   when they are not already supplied.
2. Start from latest production main with `python3 scripts/editorial.py start article-slug`.
3. Change only `content/articles/` and `content/images/`. Use normal publishable
   Pelican metadata and a stable slug; the proposal branch keeps it out of production.
4. Verify factual claims and sources. Mark uncertainties for human review. Do not
   invent quotes, citations or personal experiences attributed to the author.
5. Build with `make preview PELICAN=.venv/bin/pelican`, then run
   `python3 scripts/check_build.py output preview`.
6. Commit the article/assets and push `proposals/article-slug` to preview origin.
7. Wait for the preview workflow and report its run URL, article URL under
   `https://preview.cololabs.com.ar/`, and full source commit SHA. The preview is
   shared; verify `/preview.json` identifies your branch and commit before reporting.
8. Apply requested changes on the same branch, push, and report the new reviewed SHA.
9. Stop at the review handoff. Only the human runs promotion, merges the production
   PR, and publishes. Do not run `make github`, `invoke gh-pages`, or change Pages,
   DNS, workflows, repository permissions or credentials.

If the shared preview is showing another branch, report the conflict or rerun your
branch's workflow when the owner asks to review it. Never claim a failed build is live.
