# Auto Version Release Skill 🚀

This repository contains a dedicated **Skill** for AI Coding Assistants (like Cursor, Claude Code, Windsurf, Copilot, Gemini). Its goal is to fully automate the versioning lifecycle, committing, pushing, and creating GitHub Releases for any project, regardless of the programming language or framework.

## 🎯 Project Goals
- **Save Time & Effort:** Instead of manually running multiple Git commands, tracking version numbers, and writing release notes, the AI does it all for you.
- **Standardization:** Ensure a consistent and stable Git Workflow across all your different projects.
- **Local Version Clarity:** The skill automatically creates and updates a `VERSION` file in the root directory so the current version is always clear to all developers.
- **Professional Updates:** Automates the creation of a `Git Tag` and a `GitHub Release` complete with release notes seamlessly.

## 💎 The Golden Feature (Token Efficiency)
This project relies on a "Lazy Loading" architecture to minimize token consumption in AI assistants to the absolute minimum:
- **Routing Files** (`.cursorrules`, `CLAUDE.md`, etc.) contain only 3 lines of text. Their sole job is to tell the AI where to find the skill when asked. (Consuming ~30 tokens instead of hundreds of permanent tokens).
- **The Core Skill** (`SKILL.md`) is never read and consumes **zero tokens** from your context window until the exact moment you actually ask to create a new release. This represents the **Gold Standard** in prompt engineering to ensure the AI remains focused and cost-efficient!

## ⚙️ How It Works
Once the skill is invoked, the AI assistant will automatically execute the included Python script `auto_release.py`, which does the following behind the scenes:
1. **Query Current Version:** Reads previous Tags or project files (like `VERSION`).
2. **Determine New Version:** Applies Semantic Versioning (Patch, Minor, Major) based on the size of the recent changes.
3. **Local Versioning:** Updates or creates the `VERSION` file with the new number.
4. **Automated Save & Push:** Executes `git add`, `git commit` with a clear summary message, and `git push`.
5. **Tag Push:** Creates a `git tag` and pushes it to GitHub.
6. **Cloud Release:** Once the tag is pushed, a GitHub Actions workflow (in `release.yml`) automatically triggers on GitHub's servers to convert the Tag into a full-fledged Release with Release Notes.

## 🛠️ Installation & Usage (One-Click)

This repository is built as a plug & play Tool that can be installed into any of your projects with a single click using the `install.py` script.

**Quick Installation via Internet:**

1. Open the Terminal inside your project folder.
2. Copy and paste the following command to download and install the skill directly from the internet:

   **For Windows (PowerShell):**
   ```powershell
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/yz1112/skill-for-committing-update-version-Releases/main/install.py" -OutFile "install.py"; python install.py .; Remove-Item install.py
   ```

   **For Mac / Linux / Git Bash:**
   ```bash
   curl -s https://raw.githubusercontent.com/yz1112/skill-for-committing-update-version-Releases/main/install.py | python - .
   ```

*(With this single command, all necessary files will be downloaded and configured automatically in your current project!)*

**What does the installation script do?**
- Copies `SKILL.md` and `auto_release.py` into your project.
- Creates a `.github/workflows` folder and copies the `release.yml` Action into it.
- Scans for AI assistant configuration files (`CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`). If a file doesn't exist, it creates it. If it exists, it safely appends the trigger instructions without erasing your previous settings!

*(Once the script finishes, the skill is immediately ready to be used by the AI in your new project!)*

## 🚀 Execution (Usage)
When you have finished your code modifications and are ready to publish a new release, simply tell your AI assistant in natural language:
- *"Bump version"*
- *"Create a new release"*
- *"Push updates and run the release skill"*
- *"Release this version"*

The assistant will automatically figure out what to do, execute the command sequence behind the scenes, and provide a simple report of the result.

## ⚠️ Prerequisites
- [Git](https://git-scm.com/) installed on your machine and the project is linked to a repository.
- Python 3 installed to run the automation script.
- *Note:* You do NOT need to install any additional tools (like GitHub CLI) because the Release process is handled entirely in the cloud via GitHub Actions!
