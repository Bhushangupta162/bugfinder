import os
import json
import datetime
from src.clone_repo import clone_github_repo, extract_code_files
from src.chunk_code import process_all_code_files
from src.analyze_code import analyze_code_chunk, detect_language_from_filename
from src.generate_pdf_report import generate_pdf_report

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
    print("\n🚀 Starting Bug Analysis...")
    reports = {}
    total_issues = 0

    for file_path, chunks in code_chunks.items():
        print(f"🔍 Analyzing {file_path}...")
        file_reports = []

        language = detect_language_from_filename(file_path)

        for chunk in chunks:
            analysis_result = analyze_code_chunk(chunk, language=language)
            file_reports.extend(analysis_result)

        reports[file_path] = file_reports
        total_issues += len(file_reports)
        print(f"✅ Completed: {file_path} ({len(file_reports)} issues found)")

    # 5️⃣ Save Report to JSON & PDF
    save_report(reports, total_files=len(code_chunks), total_issues=total_issues, repo_url=repo_url)

def save_report(reports, total_files, total_issues, repo_url):
    """Saves the bug analysis report in JSON and PDF format."""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    repo_name = repo_url.strip("/").split("/")[-1]

    # Save JSON
    json_path = f"reports/bug_report_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)

    print(f"\n📄 JSON report saved: {json_path}")

    # Save PDF
    generate_pdf_report(reports, repo_url)
    print(f"✅ Analysis complete — {total_files} files scanned, {total_issues} issues detected.")

if __name__ == "__main__":
    main()
