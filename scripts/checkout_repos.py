import argparse
import json
import os
import subprocess
from pathlib import Path

from common import (
    ROOT,
    available_repos_manifest_path,
    load_repositories,
    load_promotion,
)

def bootstrap_mode_enabled():
    return os.environ.get("DOCS_BOOTSTRAP_MODE", "false").lower() == "true"

def get_promoted_ref(slug, promotion):
    repos = promotion.get("repositories", [])
    for repo in repos:
        if repo.get("slug") == slug:
            return repo.get("ref")
    return None

def build_authenticated_url(repository):
    token = os.environ.get("DOCS_READ_TOKEN", "").strip()

    if not token:
        return None

    return f"https://x-access-token:{token}@github.com/{repository}.git"

def clone_repo(url, target, ref=None):
    if target.exists():
        print(f"Repository already exists: {target}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)

    print(f"Cloning {url} -> {target}")

    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            url,
            str(target),
        ],
        check=True,
    )

    subprocess.run(
        [
            "git",
            "-C",
            str(target),
            "config",
            "advice.detachedHead",
            "false",
        ],
        check=True,
    )

    if ref:
        subprocess.run(
            [
                "git",
                "-C",
                str(target),
                "fetch",
                "--tags",
            ],
            check=True,
        )

        subprocess.run(
            [
                "git",
                "-C",
                str(target),
                "checkout",
                ref,
            ],
            check=True,
        )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()

    repos = load_repositories()
    promotion = load_promotion()

    available = []

    token = os.environ.get("DOCS_READ_TOKEN", "").strip()

    if token:
        print("DOCS_READ_TOKEN detected - authenticated checkout enabled")
    else:
        print("DOCS_READ_TOKEN not set - only public/example repositories can be checked out")

    for repo in repos:
        slug = repo["slug"]
        repository = repo.get("repository")
        required = repo.get("required", False)

        if args.from_examples:
            example_path = ROOT / repo["local_example_path"]
            if example_path.exists():
                print(f"Using example repository for {slug}: {example_path}")
                available.append(slug)
            continue

        ref = get_promoted_ref(slug, promotion)

        if not ref:
            msg = f"WARNING: No promoted ref declared for slug {slug} in promotion.yml"

            if required and not bootstrap_mode_enabled():
                raise SystemExit(msg)

            print(msg)
            continue

        checkout_path = ROOT / repo.get(
            "checkout_path",
            f".cache/repos/{slug}"
        )

        authenticated_url = None

        if repository and token:
            authenticated_url = build_authenticated_url(repository)

        if authenticated_url:
            try:
                clone_repo(authenticated_url, checkout_path, ref=ref)
                available.append(slug)
                continue
            except subprocess.CalledProcessError as e:
                msg = f"WARNING: Failed authenticated checkout for {repository}: {e}"

                if required and not bootstrap_mode_enabled():
                    raise SystemExit(msg)

                print(msg)
                continue

        remote_env = repo.get("remote_url_env")

        if remote_env:
            remote_url = os.environ.get(remote_env)

            if remote_url:
                try:
                    clone_repo(remote_url, checkout_path, ref=ref)
                    available.append(slug)
                    continue
                except subprocess.CalledProcessError as e:
                    msg = f"WARNING: Failed checkout via {remote_env}: {e}"

                    if required and not bootstrap_mode_enabled():
                        raise SystemExit(msg)

                    print(msg)
                    continue

        msg = (
            f"WARNING: No checkout method for {repository or slug}; "
            f"set DOCS_READ_TOKEN or {remote_env}"
        )

        if required and not bootstrap_mode_enabled():
            raise SystemExit(msg)

        print(msg)

    manifest_path = available_repos_manifest_path()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps({"available_slugs": sorted(set(available))}, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "Available repositories:",
        ", ".join(sorted(set(available))) if available else "none"
    )

if __name__ == "__main__":
    main()
