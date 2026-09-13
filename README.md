# GitHub Green Field

A small Python script that creates backdated empty Git commits to fill a GitHub contribution graph with green squares.

This project is meant for fun, demos, and harmless pranks with friends. It does not change any real project files because it uses empty commits.

## How It Works

GitHub shows contributions based on commits that are:

- made with an email address connected to your GitHub account
- pushed to the repository's default branch, usually `main`
- inside the contribution graph date range

This script creates empty commits for past dates by setting:

- `GIT_AUTHOR_DATE`
- `GIT_COMMITTER_DATE`
- Git commit `--date`

Because the dates are backdated, GitHub can place those commits on earlier days in your contribution graph after you push the repository.

## Requirements

- Git installed
- Python installed on your system
- A GitHub repository
- Your local Git email must match a verified email on your GitHub account

Check your Git email:

```powershell
git config user.email
```

Set your Git email:

```powershell
git config user.name "Your Name"
git config user.email "your-github-email@example.com"
```

## Usage

Run the script from this repository:

```powershell
py github.py
```

By default, it creates commits for the last `365` days with `4` commits per day.

You can customize it:

```powershell
py github.py --days 200 --commits 3
```

Create a more natural-looking random pattern:

```powershell
py github.py --days 365 --random --min-commits 2 --max-commits 7
```

This creates a different number of commits on each day. For example, one day may get `3` commits, another may get `6`, another may get `2`, and so on.

Skip weekends:

```powershell
py github.py --days 365 --commits 5 --skip-weekends
```

Random commits while skipping weekends:

```powershell
py github.py --days 365 --random --min-commits 2 --max-commits 7 --skip-weekends
```

## Push to GitHub

If this is a new repository:

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

If the repository is already connected:

```powershell
git push
```

## Why Contributions Might Not Show

If the green squares do not appear immediately, check these things:

- The commit email must be added and verified in your GitHub account.
- The commits must be on the default branch of the repository.
- The repository should not be a fork unless the commits were merged into the parent repository.
- GitHub can take some time to update the contribution graph.

## Reset the Repository

Reset commands rewrite Git history. Use them only if you are okay with replacing the current `main` branch on GitHub.

If you created a backup branch before generating commits, you can reset back to it:

```powershell
git reset --hard backup-before-email-fix
git push --force-with-lease origin main
```

If you want to create a fresh clean branch with only one empty reset commit:

```powershell
git checkout --orphan fresh-main
git rm -rf .
git commit --allow-empty -m "Reset repository"
git branch -D main
git branch -m main
git push --force-with-lease origin main
```

If you want to remove the generated green commits but keep the project files, create a fresh branch, add the files again, then force-push it:

```powershell
git checkout --orphan fresh-main
git add README.md github.py
git commit -m "Reset project files"
git branch -D main
git branch -m main
git push --force-with-lease origin main
```

## Notes

This script creates empty commits only. It is not meant to fake real work or mislead people in professional settings.
