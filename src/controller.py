import datetime
import os
import json
import re
from src.clone_repo import clone_github_repo, extract_code_files
from src.chunk_code import process_all_code_files
from src.analyze_code import analyze_code_chunk, detect_language_from_filename
from src.generate_pdf_report import generate_pdf_report

def is_valid_github_url(url):
    pattern = r'^https:\/\/github\.com\/[\w\-]+\/[\w\-]+$'
    return re.match(pattern, url)

def run_analysis(repo_url):
    if not is_valid_github_url(repo_url):
        return None, "❌ Invalid GitHub URL."

    repo_path = clone_github_repo(repo_url)
    if not repo_path:
        return None, "❌ Failed to clone repository."

    code_files = extract_code_files(repo_path)
    if not code_files:
        return None, "❌ No code files found."

    code_chunks = process_all_code_files(code_files)

    reports = {}
    total_issues = 0

    for file_path, chunks in code_chunks.items():
        language = detect_language_from_filename(file_path)
        file_reports = []

        for chunk in chunks:
            analysis_result = analyze_code_chunk(chunk, language=language)
            file_reports.extend(analysis_result)

        reports[file_path] = file_reports
        total_issues += len(file_reports)

    # Save reports
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    repo_name = repo_url.strip("/").split("/")[-1]

    json_filename = f"bug_report_{timestamp}.json"
    json_path = os.path.join("reports", json_filename)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)

    # Generate PDF
    pdf_filename = f"{repo_name}_bug_report.pdf"
    generate_pdf_report(reports, repo_url)

    # ✅ This matches what app.py needs to render result.html
    return {
        "report": reports,
        "total_issues": total_issues,
        "total_files": len(code_chunks),
        "repo_url": repo_url,
        "repo_name": repo_name,
        "pdf_filename": pdf_filename,
        "json_filename": json_filename
    }, None
