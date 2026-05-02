---
name: git-workflow
description: Automates git releases — version bump, commit, push, tag, and GitHub release. Use this skill whenever the user wants to release, publish updates, bump a version, or commit and push changes. Trigger even if the user says it casually ("push it", "ship it", "make a release", "commit everything").
---

# Git Release Workflow

Automates the full release cycle for any project (any language). Run `auto_release.py` — it handles everything.

## If `auto_release.py` is missing, download it first

```bash
python -c "import urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/yz1112/skill-for-committing-update-version-Releases/main/git-workflow/scripts/auto_release.py', 'auto_release.py')"
```

## Steps

1. Review what changed (from conversation context, or run `git status` / `git diff`) and decide the bump type — decide yourself, do not ask the user:
   - `patch` — bug fixes or small tweaks
   - `minor` — new features or screens
   - `major` — breaking changes or full restructure

2. Run the script:
   ```bash
   python auto_release.py --type <patch|minor|major> --message "<concise summary of changes>"
   ```

3. Read the output and tell the user the new version number that was released.
