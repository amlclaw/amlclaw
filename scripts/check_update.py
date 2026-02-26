#!/usr/bin/env python3
"""
check_update.py
---------------
Lightweight update checker for AMLClaw skills.
Compares local git HEAD against remote origin to detect available updates.

Usage:
    python3 scripts/check_update.py          # Check and print notification
    python3 scripts/check_update.py --quiet  # Only print if update available

Non-blocking: exits 0 even if check fails (network down, not a git repo, etc.)
Opt-out: set AMLCLAW_CHECK_UPDATES=false in .env to skip entirely.

Designed to be called from run_screening.py or directly by the LLM agent.
"""

import os
import subprocess
import sys
from pathlib import Path


def get_repo_root():
    """Find the amlclaw repo root (where VERSION file lives)."""
    # Walk up from this script's location
    current = Path(__file__).resolve().parent
    for _ in range(5):
        if (current / "VERSION").exists():
            return current
        current = current.parent
    return None


def read_local_version(repo_root):
    """Read the local VERSION file."""
    version_file = repo_root / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "unknown"


def check_for_updates(quiet=False):
    """
    Check if the local repo is behind the remote.

    Returns:
        dict with keys: update_available, local_version, behind_count, message
    """
    result = {
        "update_available": False,
        "local_version": "unknown",
        "behind_count": 0,
        "message": "",
    }

    # Check opt-out
    if os.environ.get("AMLCLAW_CHECK_UPDATES", "").lower() == "false":
        return result

    repo_root = get_repo_root()
    if not repo_root:
        return result

    result["local_version"] = read_local_version(repo_root)

    # Check if this is a git repo
    git_dir = repo_root / ".git"
    if not git_dir.exists():
        return result

    try:
        # Fetch latest remote state (fast, no merge)
        subprocess.run(
            ["git", "-C", str(repo_root), "fetch", "origin", "--quiet"],
            capture_output=True, timeout=10
        )

        # Count how many commits we're behind
        behind = subprocess.run(
            ["git", "-C", str(repo_root), "rev-list", "--count", "HEAD..origin/main"],
            capture_output=True, text=True, timeout=5
        )
        behind_count = int(behind.stdout.strip()) if behind.returncode == 0 else 0

        if behind_count > 0:
            result["update_available"] = True
            result["behind_count"] = behind_count

            # Get summary of new commits
            log = subprocess.run(
                ["git", "-C", str(repo_root), "log", "--oneline", "HEAD..origin/main", "--max-count=5"],
                capture_output=True, text=True, timeout=5
            )
            commit_summary = log.stdout.strip() if log.returncode == 0 else ""

            result["message"] = (
                f"\n{'='*60}\n"
                f"  UPDATE AVAILABLE — AMLClaw v{result['local_version']}\n"
                f"  {behind_count} new commit(s) on origin/main\n"
                f"{'='*60}\n"
            )
            if commit_summary:
                result["message"] += f"\n  Recent changes:\n"
                for line in commit_summary.split("\n"):
                    result["message"] += f"    {line}\n"
            result["message"] += (
                f"\n  Update now:  cd {repo_root} && git pull origin main\n"
                f"{'='*60}\n"
            )

            print(result["message"], file=sys.stderr)

        elif not quiet:
            pass  # Silent when up-to-date

    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, OSError):
        # Non-blocking: if anything fails, just skip the check
        pass

    return result


def main():
    quiet = "--quiet" in sys.argv
    result = check_for_updates(quiet=quiet)

    if not result["update_available"] and not quiet:
        version = result["local_version"]
        print(f"AMLClaw v{version} — up to date.")


if __name__ == "__main__":
    main()
