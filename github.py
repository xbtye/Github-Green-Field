import argparse
import os
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


def plant_green_field(days_back, commits_per_day, skip_weekends):
    ensure_git_repo()

    start_date = datetime.now() - timedelta(days=days_back)
    total_commits = 0

    for day in range(days_back + 1):
        current_date = start_date + timedelta(days=day)

        if skip_weekends and current_date.weekday() >= 5:
            continue

        for commit_number in range(1, commits_per_day + 1):
            make_commit(current_date, commit_number)
            total_commits += 1

        print(
            f"{GREEN}Planted {commits_per_day} commits for "
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
        "--skip-weekends",
        action="store_true",
        help="Skip Saturdays and Sundays.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        plant_green_field(args.days, args.commits, args.skip_weekends)
    except subprocess.CalledProcessError as error:
        print(f"{RED}Git command failed: {error}{RESET}")
        print(
            f"{YELLOW}Make sure git is installed and your git user.name/user.email "
            f"are configured.{RESET}"
        )
