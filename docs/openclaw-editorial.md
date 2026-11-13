# Instructions for AI contributors

Read [publishing.md](publishing.md). Articles, pages, themes and configuration
changes use the same preview PR flow. Work in cololabs-preview with credentials
scoped only to that repository. Do not use the owner's credentials.

1. With a clean tree, switch to main and pull `preview main` with `--ff-only`.
2. Create a descriptive branch with `git switch -c BRANCH`. No name prefix is required.
3. Make only the changes requested. For articles, verify claims and sources; flag
   uncertainty and never invent quotes, references or the author's experiences.
4. Install requirements if needed, then build using `make preview PELICAN=.venv/bin/pelican`
   and run `python3 scripts/check_build.py output preview`. For localhost rendering,
   prefix the build with `PREVIEW_SITEURL=http://localhost:8000`.
5. Commit the intended files, push with `git push -u preview HEAD`, and open a PR:
   `gh pr create --repo hjlarrea/cololabs-preview --base main --fill`.
6. Wait for deployment, check the banner and /preview.json identify your change,
   and report the PR URL, preview URL, commit SHA and any review concerns.
7. Apply feedback on the same branch and push updates; the PR preview rebuilds.
8. Stop at the human review handoff. Do not merge, push to production, deploy
   production, or change permissions/DNS unless explicitly instructed by the owner.

Use ordinary Git and gh; there are no promotion wrappers. The human merges the
preview PR, pulls preview main locally, and releases with `git push production main`.
The production workflow then builds and publishes automatically.
