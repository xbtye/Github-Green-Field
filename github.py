import argparse
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta, time

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def run(command, env=None, capture=False):
    if capture:
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        return result.stdout.strip()
    subprocess.run(command, check=True, env=env)


def is_git_repo():
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def ensure_git_repo():
    if not is_git_repo():
        print(f"{YELLOW}No git repo found. Initializing git repository...{RESET}")
        run(["git", "init"])


def get_git_config(key):
    try:
        val = run(["git", "config", "--get", key], capture=True)
        return val if val else ""
    except Exception:
        return ""


def get_user_credentials(args):
    detected_name = get_git_config("user.name") or "xbtye"
    detected_email = get_git_config("user.email") or "vs1120204@gmail.com"

    username = args.username.strip() if args.username else detected_name
    email = args.email.strip() if args.email else detected_email

    print(f"\n{CYAN}{BOLD}==========================================================={RESET}")
    print(f"{GREEN}{BOLD}  GITHUB GREEN FIELD CONTRIBUTION BOOSTER (AUTOMATED){RESET}")
    print(f"{CYAN}{BOLD}==========================================================={RESET}\n")

    print(f"{GREEN}-----------------------------------------------------------{RESET}")
    print(f"{BOLD}[+] TARGET GITHUB PROFILE CONFIRMED:{RESET}")
    print(f"    {CYAN}GitHub Username:{RESET} {BOLD}{username}{RESET}")
    print(f"    {CYAN}Commit Email:   {RESET} {BOLD}{email}{RESET}")
    print(f"    {CYAN}GitHub Profile: {RESET} {BOLD}https://github.com/{username}{RESET}")
    print(f"{GREEN}[*] All generated commits will be authored by & credited to: {BOLD}{username}{RESET}")
    print(f"{GREEN}-----------------------------------------------------------{RESET}\n")

    return username, email


def make_commit(commit_datetime, index, username, email):
    formatted_date = commit_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = username
    env["GIT_AUTHOR_EMAIL"] = email
    env["GIT_COMMITTER_NAME"] = username
    env["GIT_COMMITTER_EMAIL"] = email
    env["GIT_AUTHOR_DATE"] = formatted_date
    env["GIT_COMMITTER_DATE"] = formatted_date

    run(
        [
            "git",
            "commit",
            "--allow-empty",
            "-m",
            f"green field {commit_datetime:%Y-%m-%d} #{index}",
            "--date",
            formatted_date,
        ],
        env=env,
    )


def get_daily_commit_count(args):
    if not args.random:
        return args.commits

    return random.randint(args.min_commits, args.max_commits)


def calculate_date_range(args):
    now = datetime.now()
    if args.year:
        start_date = datetime(args.year, 1, 1)
        end_date = datetime(args.year, 12, 31)
        if end_date > now:
            end_date = now
    elif args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        if args.end_date:
            end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        else:
            end_date = now
    else:
        end_date = now
        start_date = now - timedelta(days=args.days)

    return start_date, end_date


def plant_green_field(args):
    username, email = get_user_credentials(args)
    ensure_git_repo()

    start_date, end_date = calculate_date_range(args)
    total_days = (end_date - start_date).days + 1

    print(f"{CYAN}{BOLD}[*] Planting contribution commits...{RESET}")
    print(f"    Date Range: {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d} ({total_days} days)")
    print(f"    Random Mode: {'Enabled (' + str(args.min_commits) + '-' + str(args.max_commits) + ' commits/day)' if args.random else 'Fixed (' + str(args.commits) + ' commits/day)'}\n")

    total_commits = 0

    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)

        if current_date > datetime.now():
            break

        if args.skip_weekends and current_date.weekday() >= 5:
            continue

        daily_commits = get_daily_commit_count(args)

        for commit_number in range(1, daily_commits + 1):
            random_hour = random.randint(9, 21)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            commit_datetime = datetime.combine(
                current_date.date(), time(random_hour, random_minute, random_second)
            )

            make_commit(commit_datetime, commit_number, username, email)
            total_commits += 1

        print(
            f"{GREEN}Planted {daily_commits} commits for {current_date:%Y-%m-%d}{RESET}"
        )

    print(f"\n{GREEN}-----------------------------------------------------------{RESET}")
    print(
        f"{GREEN}{BOLD}[+] Success! Created {total_commits} empty commits for profile '{username}'.{RESET}"
    )
    print(f"{GREEN}-----------------------------------------------------------{RESET}")

    print(f"\n{YELLOW}{BOLD}Next Steps to publish contributions to GitHub profile '{username}':{RESET}")
    print(f"  1. git branch -M main")
    print(f"  2. git remote add origin https://github.com/{username}/<repo-name>.git")
    print(f"  3. git push -u origin main\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create backdated empty commits for a GitHub-style green field."
    )
    parser.add_argument(
        "--username",
        "--name",
        type=str,
        default="",
        help="GitHub username for commit author attribution (default: xbtye).",
    )
    parser.add_argument(
        "--email",
        "--gmail",
        type=str,
        default="",
        help="Gmail/Email associated with your GitHub account (default: vs1120204@gmail.com).",
    )
    parser.add_argument("--days", type=int, default=365, help="Days to fill (default: 365).")
    parser.add_argument("--year", type=int, default=None, help="Fill commits for a specific calendar year (e.g. 2025).")
    parser.add_argument("--start-date", type=str, default=None, help="Start date (YYYY-MM-DD).")
    parser.add_argument("--end-date", type=str, default=None, help="End date (YYYY-MM-DD).")
    parser.add_argument(
        "--commits",
        type=int,
        default=4,
        help="Empty commits to create per day (when random mode is disabled).",
    )
    parser.add_argument(
        "--no-random",
        dest="random",
        action="store_false",
        help="Disable random daily commits count and use fixed --commits count.",
    )
    parser.set_defaults(random=True)

    parser.add_argument(
        "--min-commits",
        type=int,
        default=1,
        help="Minimum commits per day when using random mode (default: 1).",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=6,
        help="Maximum commits per day when using random mode (default: 6).",
    )
    parser.add_argument(
        "--skip-weekends",
        action="store_true",
        help="Skip Saturdays and Sundays.",
    )

    args = parser.parse_args()

    if args.min_commits < 0 or args.max_commits < 0:
        parser.error("--min-commits and --max-commits cannot be negative.")

    if args.min_commits > args.max_commits:
        parser.error("--min-commits cannot be greater than --max-commits.")

    return args


if __name__ == "__main__":
    args = parse_args()

    try:
        plant_green_field(args)
    except subprocess.CalledProcessError as error:
        print(f"{RED}Git command failed: {error}{RESET}")
        sys.exit(1)
