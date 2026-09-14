# GitHub Green Field

A small Python script that creates backdated empty Git commits to fill any user's GitHub contribution graph with green squares.

This project is built so anyone can easily use it or run it for their own GitHub profile without configuring system-wide Git credentials.

## Features

- **Interactive User Prompt**: Prompts directly for your GitHub Email/Gmail and GitHub Username when run.
- **Custom Attribution**: Sets author and committer details on every commit so contributions register on your GitHub profile graph.
- **Flexible Options**: Custom days range, daily commit count, random commit patterns, and weekend skipping.
- **CLI Support**: Optional command-line flags (`--email` and `--username`) for automated scripts.

## How It Works

GitHub attributes contributions based on commits that are:

- Made with an email address connected to your verified GitHub account.
- Pushed to the repository's default branch (usually `main`).
- Inside the contribution graph date range.

This script creates empty commits for past dates by setting:

- `GIT_AUTHOR_NAME` & `GIT_AUTHOR_EMAIL`
- `GIT_COMMITTER_NAME` & `GIT_COMMITTER_EMAIL`
- `GIT_AUTHOR_DATE` & `GIT_COMMITTER_DATE`
- Git commit `--date`

Because the author details are bound directly to each commit, anyone can enter their details when running the script to boost their profile graph.

## Requirements

- Git installed on your system
- Python 3.x installed
- A GitHub repository (or new repository) linked to your account

## Quick Start (Interactive)

Simply run the script:

```powershell
py github.py
```

It will ask you interactively:

1. **Enter your GitHub Email / Gmail** (e.g. `yourname@gmail.com`)
2. **Enter your GitHub Username** (e.g. `your-github-username`)

Then it generates backdated empty commits for your profile!

## Command Line Usage

You can also pass your username and email directly using CLI arguments:

```powershell
py github.py --email "yourname@gmail.com" --username "yourusername"
```

### Advanced Customization

Change days and commit count:

```powershell
py github.py --days 200 --commits 3
```

Create a natural-looking random pattern:

```powershell
py github.py --days 365 --random --min-commits 2 --max-commits 7
```

Skip weekends:

```powershell
py github.py --days 365 --commits 5 --skip-weekends
```

Random commits while skipping weekends:

```powershell
py github.py --days 365 --random --min-commits 2 --max-commits 7 --skip-weekends
```

Non-interactive CI / Script Mode:

```powershell
py github.py --email "yourname@gmail.com" --username "yourusername" --non-interactive
```

## Push Contributions to GitHub

After running the script, push the commits to your GitHub repository:

If this is a new repository:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

If the repository is already connected to your remote:

```powershell
git push
```

## Troubleshooting & Notes

- **Commit Email**: Make sure the email you enter is added and verified in your GitHub account settings (`Settings` -> `Emails`).
- **Default Branch**: GitHub calculates contributions for commits on your repository's primary branch (`main`).
- **Processing Time**: GitHub contribution graphs usually update within a few minutes after pushing.
- **Empty Commits**: This script uses `--allow-empty` commits, so no project files are modified.
