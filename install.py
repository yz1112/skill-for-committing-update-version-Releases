import os
import sys
import shutil
import subprocess
import urllib.request

REPO_URL = "https://raw.githubusercontent.com/yz1112/skill-for-committing-update-version-Releases/main/"

# The text injected into IDE instruction files
AI_INSTRUCTION = """# --- Auto Release Skill ---
When the user asks to release, push updates, bump a version, commit, or publish changes, read `SKILL.md` in the project root and follow the instructions there. The workflow uses `auto_release.py` (downloaded automatically if missing) to handle versioning, tagging, and GitHub releases.
# --------------------------"""

# IDE definitions: name -> instruction file path (relative to project root)
IDE_FILES = {
    "claude":         "CLAUDE.md",
    "cursor":         ".cursorrules",
    "windsurf":       ".windsurfrules",
    "copilot":        os.path.join(".github", "copilot-instructions.md"),
    "antigravity":    None,  # handled separately (skill folder)
    "claude-global":  None,  # handled separately (global ~/.claude/skills/)
}

def detect_ide():
    """Detect the active IDE from environment variables and running processes."""
    env = os.environ

    if any(k.startswith("CURSOR") for k in env):
        return "cursor"
    if any(k.startswith("WINDSURF") for k in env):
        return "windsurf"
    if any(k.startswith("CLAUDE") for k in env):
        return "claude"
    if any(k.startswith("ANTIGRAVITY") or k.startswith("GEMINI") for k in env):
        return "antigravity"
    if "VSCODE_PID" in env or env.get("TERM_PROGRAM") == "vscode":
        return "copilot"

    # Fallback: check running processes
    try:
        if os.name == "nt":
            procs = subprocess.check_output("tasklist", shell=True, text=True, stderr=subprocess.DEVNULL).lower()
        else:
            procs = subprocess.check_output(["ps", "aux"], text=True, stderr=subprocess.DEVNULL).lower()

        if "cursor" in procs:
            return "cursor"
        if "windsurf" in procs:
            return "windsurf"
        if "antigravity" in procs:
            return "antigravity"
        if "code" in procs:
            return "copilot"
    except Exception:
        pass

    return None


def find_case_insensitive_path(file_path):
    directory = os.path.dirname(file_path) or "."
    filename = os.path.basename(file_path)
    if not os.path.exists(directory):
        return file_path
    for f in os.listdir(directory):
        if f.lower() == filename.lower():
            return os.path.join(directory, f)
    if filename.lower() == "claude.md":
        for f in os.listdir(directory):
            if f.lower() == "claud.md":
                return os.path.join(directory, f)
    return file_path


def append_instruction(file_path):
    file_path = find_case_insensitive_path(file_path)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "# --- Auto Release Skill" in content:
            print(f"  [Skipped] Already configured: {os.path.basename(file_path)}")
            return
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(AI_INSTRUCTION + "\n\n" + content)
        print(f"  [Updated] {os.path.basename(file_path)}")
    else:
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(AI_INSTRUCTION + "\n")
        print(f"  [Created] {os.path.basename(file_path)}")


def get_file_content(filename, target_path):
    try:
        local_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if os.path.exists(local_src) and not local_src.endswith("<stdin>"):
            if os.path.abspath(local_src) != os.path.abspath(target_path):
                shutil.copy2(local_src, target_path)
                print(f"  [Copied] {filename} (local)")
                return
    except NameError:
        pass  # __file__ not defined when piped from stdin

    url = REPO_URL + filename
    try:
        urllib.request.urlretrieve(url, target_path)
        print(f"  [Downloaded] {filename}")
    except Exception as e:
        print(f"  [Error] Could not get {filename}: {e}")


def install_antigravity(target_dir):
    skill_dir = os.path.join(target_dir, ".agents", "skills", "git-workflow")
    os.makedirs(skill_dir, exist_ok=True)
    get_file_content("git-workflow/SKILL.md", os.path.join(skill_dir, "SKILL.md"))
    print(f"  [Antigravity] Skill at .agents/skills/git-workflow/SKILL.md")


def install_claude_global():
    global_skill_dir = os.path.join(os.path.expanduser("~"), ".claude", "skills", "git-workflow")
    os.makedirs(global_skill_dir, exist_ok=True)
    get_file_content("git-workflow/SKILL.md", os.path.join(global_skill_dir, "SKILL.md"))
    print(f"  [Claude Global] Skill at {global_skill_dir}")


def install(target_dir, ide=None):
    # Always install the GitHub Actions workflow
    gh_dir = os.path.join(target_dir, ".github", "workflows")
    os.makedirs(gh_dir, exist_ok=True)
    get_file_content(".github/workflows/release.yml", os.path.join(gh_dir, "release.yml"))

    if ide == "all":
        ides = list(IDE_FILES.keys())
    elif ide:
        ides = [ide]
    else:
        detected = detect_ide()
        if detected:
            print(f"  Detected IDE: {detected}")
            ides = [detected]
        else:
            print("  Could not detect IDE — installing for all.")
            ides = list(IDE_FILES.keys())

    for name in ides:
        if name == "antigravity":
            install_antigravity(target_dir)
        elif name == "claude-global":
            install_claude_global()
        else:
            instruction_file = IDE_FILES.get(name)
            if instruction_file:
                append_instruction(os.path.join(target_dir, instruction_file))
            else:
                print(f"  [Unknown] IDE '{name}' not recognized.")

    print("\n✅ Installation completed successfully!")
    print("\nUsage:")
    print("  Auto-detect IDE:        python install.py")
    print("  Specific IDE:           python install.py --ide cursor|windsurf|claude|copilot|antigravity")
    print("  Claude Code (global):   python install.py --ide claude-global  # works in ALL projects")
    print("  All IDEs:               python install.py --all")
    print("\nOne-command install from anywhere:")
    print('  python -c "import urllib.request; exec(urllib.request.urlopen(\'https://raw.githubusercontent.com/yz1112/skill-for-committing-update-version-Releases/main/install.py\').read())"')


if __name__ == "__main__":
    print("🚀 Auto Release Skill Installer\n")

    args = sys.argv[1:]
    target = os.getcwd()
    ide_choice = None

    # Parse args: [target_dir] [--ide NAME] [--all]
    i = 0
    while i < len(args):
        if args[i] == "--ide" and i + 1 < len(args):
            ide_choice = args[i + 1]
            i += 2
        elif args[i] == "--all":
            ide_choice = "all"
            i += 1
        elif not args[i].startswith("--"):
            target = args[i]
            i += 1
        else:
            i += 1

    def is_skill_repo(directory):
        try:
            with open(os.path.join(directory, ".git", "config"), "r", encoding="utf-8") as f:
                return "skill-for-committing-update-version-Releases" in f.read()
        except Exception:
            return False

    if is_skill_repo(target):
        print("❌ You are running this inside the skill repository itself.")
        print("💡 Run from your other project's directory:")
        print('   python -c "import urllib.request; exec(urllib.request.urlopen(\'https://raw.githubusercontent.com/yz1112/skill-for-committing-update-version-Releases/main/install.py\').read())"')
        sys.exit(0)

    if not os.path.exists(target):
        print(f"Error: Directory '{target}' does not exist.")
        sys.exit(1)

    print(f"Installing to: {target}\n")
    install(target, ide=ide_choice)
