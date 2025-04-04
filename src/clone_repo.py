import os
import git
from clean import clean_directories  

def clone_github_repo(repo_url, local_dir="repo_code"):
    """Clone a GitHub repo into a local directory with Windows-safe config."""
    clean_directories()

    try:
        print("Cloning fresh repo...")
        git.Repo.clone_from(
            repo_url,
            local_dir,
            multi_options=["--config", "core.protectNTFS=false"],
            allow_unsafe_options=True  # ✅ This is the fix!
        )
        return local_dir
    except Exception as e:
        print(f"❌ Git clone failed: {e}")
        return None

def extract_code_files(repo_path, extensions=None):
    """Extract code files from the cloned repo, skipping junk and non-essential files."""
    if extensions is None:
        extensions = [
            ".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rb", ".php", ".rs",
            ".html", ".css", ".swift", ".kt", ".sh", ".sql", ".dart"
        ]

    code_files = []
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.vscode', '.github', 'venv', 'dist', 'build', 'assets'}

    for root, dirs, files in os.walk(repo_path):
        # 🧹 Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            # ❌ Skip minified or test files
            if file.endswith(".min.js") or "test" in file.lower() or "mock" in file.lower():
                continue

            if any(file.endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)

                try:
                    # ✅ Skip tiny/useless files (<50 bytes)
                    if os.path.getsize(full_path) > 50:
                        code_files.append(full_path)
                except Exception:
                    continue

    return code_files
