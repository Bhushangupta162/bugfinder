import shutil
import os
import stat

def handle_remove_readonly(func, path, exc_info):
    """
    Clear the readonly bit and reattempt the removal.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_directories():
    paths_to_clean = ['repo_code', 'reports']

    for path in paths_to_clean:
        if os.path.exists(path):
            print(f"Cleaning: {path}")
            shutil.rmtree(path, onerror=handle_remove_readonly)
        else:
            print(f"{path} not found. Skipping...")

    print("✅ Cleanup completed.")

if __name__ == "__main__":
    clean_directories()
