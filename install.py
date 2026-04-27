import os
import sys
import shutil

# The text to append to AI instruction files
AI_INSTRUCTION = """
# --- Auto Release Skill Instructions ---
Whenever the user requests a version bump, a release, or to push updates (e.g. "ارفع التحديثات", "اعمل ريليس"), you must read the `SKILL.md` file in the root directory and execute the instructions found there exactly. The workflow requires running `python auto_release.py` to bump versions, create git tags, and trigger GitHub releases.
# ---------------------------------------
"""

def append_instruction(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "# --- Auto Release Skill Instructions ---" in content:
            print(f"  [Skipped] Instructions already exist in {os.path.basename(file_path)}")
            return
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n" + AI_INSTRUCTION)
        print(f"  [Appended] Added instructions to existing {os.path.basename(file_path)}")
    else:
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(AI_INSTRUCTION.strip() + "\n")
        print(f"  [Created] Created new file {os.path.basename(file_path)} with instructions")

def install(target_dir):
    source_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Copy core files
    core_files = ["auto_release.py", "SKILL.md"]
    for file in core_files:
        src = os.path.join(source_dir, file)
        dst = os.path.join(target_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  [Copied] {file} -> {target_dir}")
        else:
            print(f"  [Error] Cannot find {src} to copy.")

    # 2. Copy GitHub Actions workflow
    gh_workflow_dir = os.path.join(target_dir, ".github", "workflows")
    os.makedirs(gh_workflow_dir, exist_ok=True)
    src_workflow = os.path.join(source_dir, ".github", "workflows", "release.yml")
    dst_workflow = os.path.join(gh_workflow_dir, "release.yml")
    if os.path.exists(src_workflow):
        shutil.copy2(src_workflow, dst_workflow)
        print(f"  [Copied] release.yml -> {gh_workflow_dir}")
    else:
        print(f"  [Error] Cannot find {src_workflow} to copy.")

    # 3. Setup AI Assistant Instructions
    ai_files = [
        "CLAUDE.md",
        ".cursorrules",
        ".windsurfrules",
        os.path.join(".github", "copilot-instructions.md")
    ]
    for file in ai_files:
        append_instruction(os.path.join(target_dir, file))
        
    print("\n✅ Installation completed successfully!")

if __name__ == "__main__":
    print("🚀 Auto Release Skill Installer")
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.getcwd()
        if os.path.abspath(target) == os.path.dirname(os.path.abspath(__file__)):
            print("❌ You are running this inside the skill repository itself.")
            print("💡 To install this skill in another project, run:")
            print(f"   python install.py /path/to/your/other/project")
            sys.exit(0)
    
    if not os.path.exists(target):
        print(f"Error: Target directory '{target}' does not exist.")
        sys.exit(1)
        
    print(f"Installing to: {target}\n")
    install(target)
