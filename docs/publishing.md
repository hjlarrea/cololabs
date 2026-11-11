# Article review and publishing

Production source is `hjlarrea/cololabs`, with generated production HTML in its
`gh-pages` branch. `hjlarrea/cololabs-preview` is a separate public repository with
shared Git history. Its Actions workflow deploys to its own GitHub Pages site at
https://preview.cololabs.com.ar. No cross-repository deployment credentials or
production secrets are stored there.

Both you and OpenClaw use the same proposal procedure. Only you promote and publish.
The preview is public; robots exclusions and noindex discourage indexing, but do
not provide access control. Do not put confidential material in either repository.

## First-time workstation setup

Install Git, Python 3.12 and GitHub CLI. Authenticate GitHub CLI as your own account
on your workstation; never copy that credential to OpenClaw.

```sh
gh auth login
gh auth setup-git
gh repo clone hjlarrea/cololabs-preview
cd cololabs-preview
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The repos share history but are independent GitHub repositories: GitHub cannot fork
a repository into the same owning account. Production PRs therefore use a temporary
branch in the production repository, created by the human promotion command.

## 1. Start and write an article

Run inside your preview clone:

```sh
python3 scripts/editorial.py start my-article
```

This fetches current production `main` and creates `proposals/my-article` directly
from it. Start every proposal this way; preview `main` is a bootstrap/control branch,
not the authority for published articles. The working tree must be clean.

Create `content/articles/my-article.md` with normal Pelican metadata:

```text
Title: My article
Date: 2026-11-11 10:00
Category: Technology
Slug: my-article
Authors: Hernan J. Larrea
Summary: A short description.

Article text goes here.
```

Use an appropriate current date. Add assets under `content/images/`, referenced
with Pelican links such as `![Description]({static}/images/my-image.png)`.
Avoid `Status: draft` for this flow: ordinary articles let you review homepage,
category and feed behavior before publishing. Branch isolation is the review gate.
Do not merge unfinished articles to production `main`.

For a local preview, with no deployment:

```sh
PREVIEW_SITEURL=http://localhost:8000 make preview PELICAN=.venv/bin/pelican
python3 -m http.server 8000 --directory output
```

Build before running the HTTP server. Stop the server with Ctrl-C. `make serve`
uses development settings; the explicit command above serves the preview output.

## 2. Deploy and review

```sh
git add content/articles/my-article.md content/images/
git commit -m "Propose my article"
git push -u origin HEAD
gh run list --repo hjlarrea/cololabs-preview --workflow preview.yml --branch proposals/my-article
```

The `Deploy preview` workflow runs automatically for pushes to `proposals/**`.
Wait for its deployment job to succeed, then open https://preview.cololabs.com.ar.
Review the article, homepage, navigation, images and mobile layout. The banner
shows the full source commit. `/preview.json` records commit, branch and Actions run.
You can open a PR in the preview repository for discussion; merging it is not
required. The branch push already creates the preview.

There is **one shared preview**, so the most recent successful deployment wins.
Never identify it only by its URL: check the banner commit. To select an existing
proposal again, use the Actions tab's Run workflow branch selector, or:

```sh
gh workflow run preview.yml --repo hjlarrea/cololabs-preview --ref proposals/my-article
```

Commit and push requested edits to the same branch, wait for deployment and review
again. Keep the full reviewed SHA for promotion. If production main changes, update
the proposal, redeploy and review the integrated result:

```sh
git fetch https://github.com/hjlarrea/cololabs.git main
git merge FETCH_HEAD
git push
```

Resolve any merge conflicts before committing. Do not force-push shared proposals.

## 3. Promote the reviewed commit (human only)

From the preview clone, authenticated with your personal GitHub credentials:

```sh
python3 scripts/editorial.py promote proposals/my-article FULL_40_CHARACTER_REVIEWED_SHA
```

The command checks that the remote proposal and live deployment match the reviewed
SHA, that the proposal includes current production main, and that its changes are
limited to article files and images. It pushes that exact commit into a uniquely
named `review/` branch in production and opens a PR against production `main`.
It neither merges nor publishes. Repeating it reuses the open PR.

Review the production PR's diff and `Validate site` check, then merge it yourself.
Infrastructure changes follow a separate PR and are intentionally rejected by the
article promotion command. If a proposal changes after promotion, review the new
preview and promote its new SHA into a new PR; close the superseded PR.

## 4. Publish (human only)

Run in a separate clone of **production** (`hjlarrea/cololabs`), with a clean
working tree. Confirm the article PR is merged and its checks pass:

```sh
git switch main
git pull --ff-only origin main
.venv/bin/python -m pip install -r requirements.txt
make publish PELICAN=.venv/bin/pelican
python3 scripts/check_build.py output production
PATH="$PWD/.venv/bin:$PATH" make github
```

`make publish` only builds; `make github` builds and pushes generated HTML to
production `gh-pages`. GitHub Pages then updates https://cololabs.com.ar. Inspect
the live article after the Pages build finishes. Production publishing remains
manual: no preview workflow can publish to the production repository.
The publishing command refuses a preview clone, a dirty tree, a branch other than
`main`, or a commit that differs from remote production main. `invoke gh-pages`
uses the same guarded command. These checks prevent mistakes; repository-scoped
credentials provide the actual authorization boundary.

To withdraw an article, revert its source change through a production PR, merge,
and publish again. Reverting source alone does not update the live site.

## OpenClaw access and instructions

Give OpenClaw a separate GitHub identity with write access **only** to
`hjlarrea/cololabs-preview`. Alternatively, use a fine-grained token restricted to
that repository, with Contents read/write and Pull requests read/write if opening
review PRs. Do not grant Administration, production repository access, or your
personal SSH key/token. Public production source is readable without credentials.
The preview workflow uses its own repository-scoped `GITHUB_TOKEN` to deploy.

Use [openclaw-editorial.md](openclaw-editorial.md) as the agent task instructions.
The same isolation applies if the token belongs to your own account: its repository
selection must include only the preview repository. A separate identity is easier
to audit. Provision the identity/token on the OpenClaw machine yourself; never put
credentials in Git or the prompt. No bot username has been assumed or invited.

## Repository and DNS configuration

The preview repo needs:

- Pages publishing source: **GitHub Actions**, not a branch.
- Custom domain: `preview.cololabs.com.ar`.
- Environment `github-pages` configured to allow `main` and `proposals/*` branches.
- Actions enabled, using the provided `preview.yml` workflow.
- DNS CNAME record: host `preview`, target `hjlarrea.github.io` (no repository path).
- HTTPS enforcement after DNS resolves and GitHub finishes issuing the certificate.

Configure the GitHub Pages custom domain **before** adding its DNS record. Avoid
copying production's `content/extra/CNAME` into preview output: preview settings
exclude it. Actions deployments obtain their domain from Pages settings.
See [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

For production, retain existing Pages source `gh-pages` and domain
`cololabs.com.ar`. The preview workflow has an explicit repository guard and skips
all its jobs in production. `Validate site` runs read-only builds on PRs.

## Maintenance and troubleshooting

- For theme/workflow/config updates, merge an infrastructure PR into production,
  then start new proposals from production main. Update preview `main` from
  production main periodically with a regular merge and push; don't overwrite
  article branches. A push to preview main also replaces the shared preview.
- Failed build: inspect the Actions run; the previous successful preview stays
  live. Check the banner or `/preview.json` before assuming your latest edit is live.
- Deployment rejected: check `github-pages` allows the proposal branch. Environment
  branch patterns use `proposals/*` for the one-level slugs generated by the helper.
- Wrong article visible: rerun the desired branch's workflow and wait for completion.
- Domain/certificate pending: check DNS and Pages settings; use the Pages-reported
  address while troubleshooting, and do not point preview at the production domain.
- Permissions denied during promotion is expected for OpenClaw. The human must run
  promotion with credentials that can create production branches and PRs.
- To retire a preview proposal, delete its branch after merge. This does not remove
  its already deployed HTML; redeploy preview main or another proposal to replace it.
