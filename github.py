import argparse
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta

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


def run(command, env=None):
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
        print(f"{YELLOW}No git repo found. Initializing one here...{RESET}")
        run(["git", "init"])


def prompt_user_credentials(args):
    print(f"\n{CYAN}{BOLD}==========================================================={RESET}")
    print(f"{GREEN}{BOLD}  GITHUB GREEN FIELD CONTRIBUTION BOOSTER{RESET}")
    print(f"{CYAN}{BOLD}==========================================================={RESET}\n")

    username = args.username.strip() if args.username else ""
    email = args.email.strip() if args.email else ""

    if not email:
        print(f"{YELLOW}{BOLD}[Step 1/2] Account Details:{RESET}")
        while not email:
            try:
                email = input(f"  {CYAN}> Enter your GitHub Email / Gmail: {RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{RED}Aborted.{RESET}")
                sys.exit(1)

            if not email:
                print(f"     {RED}Email cannot be empty. Please try again.{RESET}")
            elif "@" not in email:
                print(f"     {RED}Please enter a valid email address (e.g. user@gmail.com).{RESET}")
                email = ""

    if not username:
        while not username:
            try:
                username = input(f"  {CYAN}> Enter your GitHub Username: {RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{RED}Aborted.{RESET}")
                sys.exit(1)

            if not username:
                print(f"     {RED}Username cannot be empty. Please try again.{RESET}")

    # Immediately display profile confirmation banner on terminal!
    print(f"\n{GREEN}-----------------------------------------------------------{RESET}")
    print(f"{BOLD}[+] TARGET GITHUB PROFILE CONFIRMED:{RESET}")
    print(f"    {CYAN}GitHub Username:{RESET} {BOLD}{username}{RESET}")
    print(f"    {CYAN}Gmail / Email:  {RESET} {BOLD}{email}{RESET}")
    print(f"    {CYAN}GitHub Profile: {RESET} {BOLD}https://github.com/{username}{RESET}")
    print(f"{GREEN}[*] All contributions will be credited to: https://github.com/{username}{RESET}")
    print(f"{GREEN}-----------------------------------------------------------{RESET}\n")

    return username, email


def prompt_configuration(args):
    # If user provided explicit flags via CLI, use them directly
    if args.cli_provided_options:
        return args

    print(f"{YELLOW}{BOLD}[Step 2/2] Configure Commit Generation:{RESET}")

    # Days prompt
    while True:
        try:
            days_input = input(f"  {CYAN}> Days to backdate? [default: {args.days}]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Aborted.{RESET}")
            sys.exit(1)

        if not days_input:
            break
        try:
            val = int(days_input)
            if val > 0:
                args.days = val
                break
            print(f"     {RED}Days must be greater than 0.{RESET}")
        except ValueError:
            print(f"     {RED}Please enter a valid integer number.{RESET}")

    # Commits per day prompt
    while True:
        try:
            commits_input = input(f"  {CYAN}> Commits per day? [default: {args.commits}]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Aborted.{RESET}")
            sys.exit(1)

        if not commits_input:
            break
        try:
            val = int(commits_input)
            if val > 0:
                args.commits = val
                break
            print(f"     {RED}Commits count must be greater than 0.{RESET}")
        except ValueError:
            print(f"     {RED}Please enter a valid integer number.{RESET}")

    # Random commits prompt
    try:
        random_input = input(f"  {CYAN}> Use random commits per day? (y/N) [default: N]: {RESET}").strip().lower()
        if random_input in ("y", "yes"):
            args.random = True
            try:
                min_c = input(f"     {CYAN}> Min commits per day [default: {args.min_commits}]: {RESET}").strip()
                if min_c and int(min_c) >= 0:
                    args.min_commits = int(min_c)
                max_c = input(f"     {CYAN}> Max commits per day [default: {args.max_commits}]: {RESET}").strip()
                if max_c and int(max_c) >= args.min_commits:
                    args.max_commits = int(max_c)
            except ValueError:
                pass
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}Aborted.{RESET}")
        sys.exit(1)

    # Skip weekends prompt
    try:
        skip_input = input(f"  {CYAN}> Skip weekends? (y/N) [default: N]: {RESET}").strip().lower()
        if skip_input in ("y", "yes"):
            args.skip_weekends = True
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}Aborted.{RESET}")
        sys.exit(1)

    return args


def make_commit(commit_date, index, username, email):
    formatted_date = commit_date.strftime("%Y-%m-%dT12:%M:%S")
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
            f"green field {commit_date:%Y-%m-%d} #{index}",
            "--date",
            formatted_date,
        ],
        env=env,
    )


def get_daily_commit_count(args):
    if not args.random:
        return args.commits

    return random.randint(args.min_commits, args.max_commits)


def plant_green_field(args):
    username, email = prompt_user_credentials(args)
    args = prompt_configuration(args)
    ensure_git_repo()

    print(f"\n{CYAN}{BOLD}==========================================================={RESET}")
    print(f"{GREEN}{BOLD}[*] Generating commits for profile '{username}' ({email})...{RESET}")
    print(f"{CYAN}{BOLD}==========================================================={RESET}\n")

    start_date = datetime.now() - timedelta(days=args.days)
    total_commits = 0

    for day in range(args.days + 1):
        current_date = start_date + timedelta(days=day)

        if args.skip_weekends and current_date.weekday() >= 5:
            continue

        daily_commits = get_daily_commit_count(args)

        for commit_number in range(1, daily_commits + 1):
            make_commit(current_date, commit_number, username, email)
            total_commits += 1

        print(
            f"{GREEN}Planted {daily_commits} commits for "
            f"{current_date:%Y-%m-%d}{RESET}"
        )

    print(f"\n{GREEN}-----------------------------------------------------------{RESET}")
    print(
        f"{GREEN}{BOLD}[+] Success! Created {total_commits} empty commits for profile '{username}'.{RESET}"
    )
    print(f"{GREEN}-----------------------------------------------------------{RESET}")

    print(f"\n{YELLOW}{BOLD}Next Steps to publish contributions to GitHub profile '{username}':{RESET}")
    print(f"  1. git branch -M main")
    print(
        f"  2. git remote add origin https://github.com/{username}/<your-repo-name>.git"
    )
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
        help="GitHub username for commit author attribution.",
    )
    parser.add_argument(
        "--email",
        "--gmail",
        type=str,
        default="",
        help="Gmail/Email associated with your GitHub account.",
    )
    parser.add_argument("--days", type=int, default=365, help="Days to fill.")
    parser.add_argument(
        "--commits",
        type=int,
        default=4,
        help="Empty commits to create per day.",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Create a random number of commits each day.",
    )
    parser.add_argument(
        "--min-commits",
        type=int,
        default=2,
        help="Minimum commits per day when using --random.",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=7,
        help="Maximum commits per day when using --random.",
    )
    parser.add_argument(
        "--skip-weekends",
        action="store_true",
        help="Skip Saturdays and Sundays.",
    )

    sys_argv = sys.argv[1:]
    args = parser.parse_args()

    args.cli_provided_options = any(
        arg.startswith("--days") or arg.startswith("--commits") or arg == "--random" or arg == "--skip-weekends"
        for arg in sys_argv
    )

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
