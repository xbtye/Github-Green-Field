# GitHub Green Field

A small Python script that creates backdated empty Git commits to fill any user's GitHub contribution graph with green squares.

This project is built so anyone can easily use it or run it for another user's GitHub profile without configuring system-wide Git credentials.

## Important: How GitHub Attributes Contributions

GitHub **ONLY** awards green squares to a GitHub profile based on the **EMAIL ADDRESS** attached to the commits, not just the display username!

- If you enter `ayanmukherjee-collab` as Username, but enter **your own email**, GitHub will credit the commits to **your account**!
- To credit commits to `ayanmukherjee-collab`, you must use an email address linked to `ayanmukherjee-collab`'s GitHub account.
- The script automatically offers the default GitHub no-reply email: `username@users.noreply.github.com` (simply press Enter when prompted).

## Features

- **Username-First Interactive Prompt**: Asks for the target GitHub username first.
- **Auto-Suggested GitHub Email**: Auto-suggests `username@users.noreply.github.com` if you don't know their personal Gmail.
- **Target Profile Confirmation Banner**: Displays `https://github.com/<username>` confirmation before generating commits.
- **Custom Options**: Flexible backdate days count, daily commit count, random patterns, and weekend skipping.

## Quick Start (Interactive)

Simply run:

```powershell
py github.py
```

Terminal workflow:

1. **Enter target GitHub Username**: `ayanmukherjee-collab`
2. **Enter GitHub Email**: Press **Enter** to use `ayanmukherjee-collab@users.noreply.github.com` (or type their personal Gmail).
3. **Configure Days & Commits**: Set days to backdate [default: 365] and commits per day [default: 4].

## Command Line Usage

Pass flags directly:

```powershell
py github.py --username "ayanmukherjee-collab" --email "ayanmukherjee-collab@users.noreply.github.com"
```

### Advanced Customization

```powershell
py github.py --days 200 --commits 3
```

Random commits pattern:

```powershell
py github.py --days 365 --random --min-commits 2 --max-commits 7
```

Skip weekends:

```powershell
py github.py --days 365 --commits 5 --skip-weekends
```

## Push Contributions to GitHub

After generating commits, push them to GitHub:

```powershell
git branch -M main
git remote add origin https://github.com/ayanmukherjee-collab/<repo-name>.git
git push -u origin main
```
