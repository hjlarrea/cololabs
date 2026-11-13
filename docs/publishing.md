# Preview, merge, release

Articles, themes, pages and configuration changes all follow the same process:

1. Create a branch and open a PR in **hjlarrea/cololabs-preview**.
2. GitHub Actions builds and publishes https://preview.cololabs.com.ar whenever
   the PR is opened or updated. Branch names are unrestricted.
3. Review the preview, then merge the PR into preview **main** using GitHub or `gh`.
4. Fetch the merged preview main locally and push it to production **main**.
5. GitHub Actions builds and publishes https://cololabs.com.ar automatically.

There is one shared preview: the latest successful deployment replaces it. Check
its banner commit and `/preview.json` to identify the version being reviewed.
A merge into preview main also refreshes the preview with the merged result.
The preview is public. `noindex` discourages search engines; it does not make it private.

## One-time local setup

Both repositories are independent repositories with shared Git history. A GitHub
fork relationship is unnecessary: Git moves the reviewed commits between remotes.
Use the same checkout for both; its tracking remote is preview.

```sh
git clone git@github.com:hjlarrea/cololabs-preview.git
cd cololabs-preview
git remote rename origin preview
git remote add production git@github.com:hjlarrea/cololabs.git
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

For an existing checkout, run `git remote -v` first. If `origin` points to preview,
rename it with `git remote rename origin preview`. If it points to production,
rename it with `git remote rename origin production` and add preview instead:

```sh
git remote add preview git@github.com:hjlarrea/cololabs-preview.git
```

Keep main tracking preview, including in a checkout originally cloned from production:

```sh
git fetch preview
git branch --set-upstream-to=preview/main main
```

Authenticate Git and `gh` using your normal credentials. OpenClaw should use its
own identity or a token scoped **only to cololabs-preview**. A configured production
remote grants no write access by itself; only your credentials authorize a release.

## Make a change

Start with a clean working tree. Use any descriptive branch name:

```sh
git switch main
git pull --ff-only preview main
git switch -c improve-sidebar
```

Edit content, theme files, or other requested site files. For articles, use ordinary
Pelican metadata (Title, Date, Slug, Summary); no special draft status is needed.
Use a stable slug such as `my-article`, and put assets under `content/images/`.

To review locally:

```sh
PREVIEW_SITEURL=http://localhost:8000 make preview PELICAN=.venv/bin/pelican
python3 -m http.server 8000 --directory output
```

Open **http://localhost:8000** (HTTP). Build before serving. After editing, rebuild
in another terminal and refresh the browser; the HTTP server does not rebuild files.
Install requirements first if Pelican is missing (`make` error 127).

Commit your intended files and open a PR in preview:

```sh
git add themes/svbhack/  # or the specific content/files you changed
git commit -m "Improve sidebar"
git push -u preview HEAD
gh pr create --repo hjlarrea/cololabs-preview --base main --fill
```

You can create the PR through GitHub's UI instead. PR opening, reopening and new
commits trigger preview deployment, regardless of the source or target branch name.
Branches must belong to the preview repo: external-fork PRs run validation, but
cannot automatically deploy with a read-only fork token. This workflow uses no
`pull_request_target` execution of outside contributions.

Wait for **Deploy preview** and **Validate site** to pass. Review the page, images,
links and mobile layout. Changes requested during review go on the same branch;
push them and wait for the new preview. The preview shows the PR integrated with
its target branch; `/preview.json` records both source and rendered commit IDs.
A failed deployment leaves the preceding successful preview live.

## Merge in GitHub

Merge the reviewed PR into preview **main**. Use **Create a merge commit** (or
`gh pr merge --merge`) so shared Git history remains easy to synchronize.
Do not merge directly into production through a separate PR.

```sh
gh pr merge PR_NUMBER --repo hjlarrea/cololabs-preview --merge
```

You can perform the same action in the UI. Preview main requires successful
**Validate Pelican builds**, a PR, and no second approver, so the owner can merge
their own work. Only the human authorizes merges; AI agents stop at the review handoff.

## Release from your workstation

With a clean working tree:

```sh
git switch main
git pull --ff-only preview main
git push production main
```

**The final push releases everything merged into preview main since the last
release.** It does not select one PR. It triggers **Deploy production** in
hjlarrea/cololabs, which builds with production settings, checks the output, and
publishes through GitHub Pages. No local build, generated-HTML push, wrapper script,
or GitHub API command is part of releasing.

Wait for Deploy production to succeed, then inspect https://cololabs.com.ar.
If it fails, the last successful production deployment remains live. Fix the issue
through another preview PR and repeat. Keep repositories synchronized by making
changes in preview rather than editing production independently. Never force-push
production to resolve divergent history.

To roll back, revert the offending change through a preview PR, merge, then run the
same release commands. Updating source alone does not release until the production push.

## Repository configuration

Both Pages sites use **GitHub Actions** as publishing source. The production
workflow runs only in hjlarrea/cololabs on main; the preview workflow only in
hjlarrea/cololabs-preview. Identical source can therefore live in both repos.

- Production main accepts the owner's direct release pushes. PR/check prerequisites
  are applied in preview, not duplicated on production. Force pushes and deletion
  remain blocked.
- Preview's github-pages deployment environment allows all refs so any PR can deploy.
- Production's github-pages deployment environment allows only main.
- Pages custom domains remain cololabs.com.ar and preview.cololabs.com.ar respectively.
- Cloudflare's preview CNAME targets hjlarrea.github.io, **DNS only**. This hostname
  routes to the preview repository using GitHub's configured custom domain.
- Enable Enforce HTTPS once GitHub issues the certificate. If HTTPS is unavailable,
  check Pages DNS/certificate status; don't disable certificate verification.
- CI builds preview and production output separately, checking domain, feed and
  indexing isolation. Shared-preview workflows serialize deployments.

The old scripts/editorial.py promotion/start wrapper, check_publish.py, `make github`,
and Invoke's gh-pages deployment task have been removed. Use ordinary Git, `gh`, or
GitHub's UI for branches, PRs and merging.
