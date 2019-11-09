import os
import argparse
import json

from xdg import XDG_CONFIG_HOME
from git import Repo

LIFELOG_CONFIG_DIR = os.path.join(XDG_CONFIG_HOME, "lifelog/")
LIFELOG_CONFIG_FILE = os.path.join(LIFELOG_CONFIG_DIR, "config.json")


def save_config(config):
    if not os.path.exists(LIFELOG_CONFIG_DIR):
        os.makedirs(LIFELOG_CONFIG_DIR)

    with open(LIFELOG_CONFIG_FILE, "w") as fp:
        json.dump(config, fp)


def has_config() -> bool:
    return os.path.exists(LIFELOG_CONFIG_FILE)


def get_config():
    with open(LIFELOG_CONFIG_FILE, "r") as fp:
        return json.load(fp)


def syncronize():
    """Syncronize the life log with whatever backend is currently in use."""
    if not has_config():
        print("Could not find configuration file")
        return

    config = get_config()
    repo = Repo(config["local_path"])
    changed = False
    if repo.untracked_files:
        repo.index.add(repo.untracked_files)
        changed = True

    changed_files = [item.a_path for item in repo.index.diff(None)]
    if changed_files:
        repo.index.add(changed_files)
        changed = True

    if changed:
        repo.index.commit(f"Automated Commit from lifelog.")
        repo.remotes.origin.push()


def configure():
    """Run the configuration setup."""
    git_repo = input("What git repository should be syncronized? ")
    local_path = input("Where should local files live (~/lifelog)? ")
    if local_path == "":
        local_path = os.path.join(os.path.expanduser("~"), "lifelog/")

    save_config({"git_repo": git_repo, "local_path": local_path})


def main():
    parser = argparse.ArgumentParser(prog="lifelog")
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    syncronize_parser = subparsers.add_parser("sync", help="Syncronize life log")
    configure_parser = subparsers.add_parser("config", help="Configure life log")

    args = parser.parse_args()

    if args.command == "sync":
        syncronize()
    elif args.command == "config":
        configure()
    else:
        parser.print_usage()
