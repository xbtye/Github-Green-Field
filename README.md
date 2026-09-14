# GitHub Green Field

A small Python script that creates backdated empty Git commits to fill any user's GitHub contribution graph with green squares.

This project is built so anyone can easily use it or run it for another user's GitHub profile without configuring system-wide Git credentials.

## Important: How GitHub Attributes Contributions

GitHub **ONLY** awards green squares to a GitHub profile based on the **EMAIL ADDRESS** attached to the commits, not just the display username!

- If you enter `xbtye` as Username, but enter **your own email**, GitHub will credit the commits to **your account**!
- To credit commits to `xbtye`, you must use an email address linked to `xbtye`'s GitHub account (e.g., `vs1120204@gmail.com` or `xbtye@users.noreply.github.com`).
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

1. **Enter target GitHub Username**: `xbtye`
2. **Enter GitHub Email**: `vs1120204@gmail.com` (or press **Enter** to use `xbtye@users.noreply.github.com`).
3. **Configure Days & Commits**: Set days to backdate [default: 365] and commits per day [default: 4].

## Command Line Usage

Pass flags directly:

```powershell
py github.py --username "xbtye" --email "vs1120204@gmail.com"
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
git remote add origin https://github.com/xbtye/Github-Green-Field.git
git push -u origin main
```
