from flask import Flask, render_template, request, send_file
from src.controller import run_analysis
import os

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_url = request.form.get("repo_url")
        result, error = run_analysis(repo_url)

        if error:
            return render_template("index.html", error=error)

        # ✅ result.html expects 'report' and 'pdf_path'
        return render_template("result.html", 
                report=result["report"],
                pdf_path="/download/" + result["pdf_filename"],
                repo=result["repo_url"],
                repo_name=result["repo_name"],
                issues=result["total_issues"]
            )

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join("reports", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "❌ File not found", 404


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
