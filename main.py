import os
import json
import datetime
from src.clone_repo import clone_github_repo, extract_code_files
from src.chunk_code import process_all_code_files
from src.analyze_code import analyze_code_chunk  # ✅ Uses updated analysis

def main():
    """Main function to execute the BugFinder process."""
    repo_url = input("🔗 Enter GitHub repository URL: ").strip()

    if not repo_url:
        print("❌ No URL provided. Exiting...")
        return
    
    # 1️⃣ Clone GitHub Repo
    repo_path = clone_github_repo(repo_url)
    
    if not repo_path:
        print("❌ Failed to clone repository. Exiting...")
        return

    # 2️⃣ Extract Code Files
    code_files = extract_code_files(repo_path)

    if not code_files:
        print("❌ No code files found in repository. Exiting...")
        return

    # 3️⃣ Process & Chunk Code Using LangChain
    code_chunks = process_all_code_files(code_files)

    # 4️⃣ Analyze Code Using LangChain + Gemini
    print("\n🚀 **Starting Bug Analysis...**")
    reports = {}

    for file_path, chunks in code_chunks.items():
        print(f"🔍 Analyzing {file_path}...")
        file_reports = []

        for chunk in chunks:
            analysis_result = analyze_code_chunk(chunk)  # ✅ Now includes buggy code snippets
            file_reports.extend(analysis_result)  # Append all issues
        
        reports[file_path] = file_reports

    # 5️⃣ Save Report to JSON
    save_report(reports)

def save_report(reports):
    """Saves the bug analysis report in the 'reports' folder with a timestamp."""
    os.makedirs("reports", exist_ok=True)  # ✅ Ensure 'reports' folder exists
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"reports/bug_report_{timestamp}.json"

    with open(report_filename, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)
    
    print(f"\n✅ **Bug Report Saved:** {report_filename}")

if __name__ == "__main__":
    main()