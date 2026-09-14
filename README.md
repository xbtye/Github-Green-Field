# GitHub Green Field

A small Python script that creates backdated empty Git commits to fill any user's GitHub contribution graph with green squares.

This project is built so anyone can easily run it without interactive prompts or complex configuration.

## Features

- **100% Automated Execution**: Runs instantly without blocking interactive prompts.
- **Auto-Detected Credentials**: Defaults to username `xbtye` and email `vs1120204@gmail.com` (or your local Git config).
- **Random Commit Density**: Creates realistic variations of daily commits (1–6 commits/day) automatically.
- **Authentic Timestamps**: Spreads commits naturally across daytime hours (09:00–22:00).
- **Flexible Options**: Custom year (`--year 2025`), date ranges, backdate days, and weekend skipping.

## Quick Start (Automated)

Simply run:

```powershell
py github.py
```

The script will automatically detect your profile (`xbtye`), auto-select your email (`vs1120204@gmail.com`), enable random commit mode, and generate commits instantly!

## Command Line Usage

Override credentials or parameters directly:

```powershell
py github.py --username "xbtye" --email "vs1120204@gmail.com"
```

### Advanced Customization

Target a specific calendar year:

```powershell
py github.py --year 2025
```

Custom date range:

```powershell
py github.py --start-date 2026-01-01 --end-date 2026-06-30
```

Custom backdate days & random commit bounds:

```powershell
py github.py --days 200 --min-commits 2 --max-commits 8
```

Skip weekends:

```powershell
py github.py --days 365 --skip-weekends
```

## Push Contributions to GitHub

After generating commits, push them to GitHub:

```powershell
git branch -M main
git remote add origin https://github.com/xbtye/Github-Green-Field.git
git push -u origin main
```
