# How a change reaches main

[← Back to the AI Operating Model](../README.md)

A short walkthrough of the gate this repository uses on GitHub: GitHub Actions runs the checks, and a GitHub ruleset enforces them.
Sources: [`.github/workflows/`](../.github/workflows/), [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md), and [`docs/ruleset.json`](ruleset.json).

## 1. Work on a branch

Make the change on a branch, not on main.
The ruleset only lets changes reach main through a pull request.

## 2. Open a pull request

The pull request template has two sections: **Summary** and **Definition of Done**.
Tick every Definition of Done item:

- Change is described above and scoped to one purpose
- No credentials, hostnames, paths, usernames, or personal details added
- Diagrams re-exported to PNG if an SVG changed
- Links checked
- Restore path: revert this pull request

## 3. Pass the required checks

Three checks must pass before merge:

| Check | Workflow | What it does |
|---|---|---|
| `dod` | `dod.yml` | Fails if the PR body has no `## Definition of Done` section or has any unticked item. Reruns when the PR is opened, edited, updated, reopened, or marked ready for review. |
| `gitleaks` | `secrets-scan.yml` | Runs a gitleaks secrets scan over the full history, with findings redacted. |
| `markdown` | `docs-lint.yml` | Runs Markdown lint on every `.md` file, then an offline link check. |

The gitleaks and Markdown lint checks also run on pushes to main.

A fourth check, Vale prose style, runs on pull requests as advice only.
It never fails the build, and the ruleset doesn't require it.

## 4. Merge through the ruleset

The `main-protection` ruleset applies to the default branch:

- **No deletion.** Main can't be deleted.
- **No force-push.** History on main can't be rewritten.
- **Pull request required.** No approving review count is set.
- **Required checks.** `dod`, `gitleaks`, and `markdown` must pass.
- **No bypass.** The bypass list is empty, so the rules apply to everyone, including the owner.

Once the required checks pass, the pull request can merge.
