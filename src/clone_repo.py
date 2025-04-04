import os
import git

def clone_github_repo(repo_url, local_dir="repo_code"):
    """Clone a GitHub repo into a local directory."""
    if os.path.exists(local_dir):
        print("Repo already exists. Pulling latest changes...")
        repo = git.Repo(local_dir)
        repo.remotes.origin.pull()
    else:
        print("Cloning repo...")
        git.Repo.clone_from(repo_url, local_dir)

    return local_dir

def extract_code_files(repo_path, extensions=[".py", ".js", ".java", ".go"]):
    """Extract only code files from the cloned repo."""
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))
    return code_files