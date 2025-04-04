from src.controller import run_analysis

def main():
    repo_url = input("🔗 Enter GitHub repository URL: ").strip()
    result, error = run_analysis(repo_url)

    if error:
        print(error)
        return

    print(f"\n📄 JSON report saved: {result['json_filename']}")
    print(f"📄 PDF report saved: reports/{result['pdf_filename']}")
    print(f"✅ {result['total_issues']} issues found across {result['total_files']} files.")

if __name__ == "__main__":
    main()
