import os
import subprocess
import sys
import argparse
import re
import json

def run_cmd(cmd, check=True):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"Error executing: {cmd}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def get_current_version():
    try:
        # Try getting from git tags
        tags_output = subprocess.run("git describe --tags --abbrev=0", shell=True, text=True, capture_output=True)
        if tags_output.returncode == 0 and tags_output.stdout.strip():
            return tags_output.stdout.strip()
    except Exception:
        pass
    
    # Try getting from VERSION file
    if os.path.exists("VERSION"):
        with open("VERSION", "r", encoding="utf-8") as f:
            v = f.read().strip()
            if v: return v

    return "v0.0.0"

def bump_version(version, bump_type):
    # Remove 'v' if present
    clean_v = version.lstrip('v')
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", clean_v)
    if not match:
        # If version doesn't match standard semver, fallback to 1.0.0
        return "v1.0.0"
    
    major, minor, patch = map(int, match.groups())
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    else: # patch
        patch += 1
        
    return f"v{major}.{minor}.{patch}"

def main():
    parser = argparse.ArgumentParser(description="Automate Git Release Workflow")
    parser.add_argument('--type', choices=['patch', 'minor', 'major'], default='patch', help="Type of version bump (default: patch)")
    parser.add_argument('--message', type=str, default="", help="Commit message summary")
    args = parser.parse_args()

    current_version = get_current_version()
    new_version = bump_version(current_version, args.type)
    print(f"Bumping version: {current_version} -> {new_version}")

    # 1. Update VERSION file
    with open("VERSION", "w", encoding="utf-8") as f:
        f.write(new_version)
    print("Updated VERSION file.")

    # 2. Update package.json if exists
    if os.path.exists("package.json"):
        with open("package.json", "r", encoding="utf-8") as f:
            try:
                pkg = json.load(f)
            except json.JSONDecodeError:
                pkg = None
        if pkg and "version" in pkg:
            pkg["version"] = new_version.lstrip('v')
            with open("package.json", "w", encoding="utf-8") as f:
                json.dump(pkg, f, indent=2)
            print("Updated package.json.")

    # 3. Git Add
    run_cmd("git add .")

    # Check if there are changes to commit
    status = subprocess.run("git status --porcelain", shell=True, text=True, capture_output=True)
    if not status.stdout.strip():
        print("No changes to commit. Exiting.")
        sys.exit(0)

    # 4. Git Commit
    commit_msg = f"chore: release {new_version}"
    if args.message:
        commit_msg += f"\n\n{args.message}"
    
    # Escape quotes
    safe_msg = commit_msg.replace('"', '\\"')
    run_cmd(f'git commit -m "{safe_msg}"')

    # 5. Git Push
    print("Pushing to origin...")
    run_cmd("git push origin HEAD")

    # 6. Git Tag
    print(f"Creating and pushing tag {new_version}...")
    run_cmd(f"git tag {new_version}")
    run_cmd(f"git push origin {new_version}")

    # 7. GitHub Release
    print("Creating GitHub Release...")
    gh_check = subprocess.run("gh --version", shell=True, capture_output=True)
    if gh_check.returncode == 0:
        run_cmd(f'gh release create {new_version} --title "Release {new_version}" --generate-notes', check=False)
        print(f"Successfully created GitHub Release {new_version}!")
    else:
        print("GitHub CLI (gh) not found. Tag pushed, but release must be created manually on GitHub.")

if __name__ == "__main__":
    main()
