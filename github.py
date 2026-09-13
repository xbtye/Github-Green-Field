import argparse
import os
import random
import subprocess
from datetime import datetime, timedelta


GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
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


def make_commit(commit_date, index):
    formatted_date = commit_date.strftime("%Y-%m-%dT12:%M:%S")
    env = os.environ.copy()
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
    ensure_git_repo()

    start_date = datetime.now() - timedelta(days=args.days)
    total_commits = 0

    for day in range(args.days + 1):
        current_date = start_date + timedelta(days=day)

        if args.skip_weekends and current_date.weekday() >= 5:
            continue

        daily_commits = get_daily_commit_count(args)

        for commit_number in range(1, daily_commits + 1):
            make_commit(current_date, commit_number)
            total_commits += 1

        print(
            f"{GREEN}Planted {daily_commits} commits for "
            f"{current_date:%Y-%m-%d}{RESET}"
        )

    print(f"\n{GREEN}Done. Created {total_commits} empty commits.{RESET}")
    print(f"{YELLOW}Push with: git push -u origin main{RESET}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create backdated empty commits for a GitHub-style green field."
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
        print(
            f"{YELLOW}Make sure git is installed and your git user.name/user.email "
            f"are configured.{RESET}"
        )
