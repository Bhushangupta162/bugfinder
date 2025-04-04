from flask import Flask, render_template, request, send_file
from src.controller import run_analysis
import os
from flask import Flask

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_url = request.form.get("repo_url")
        result, error = run_analysis(repo_url)

        if error:
            return render_template("index.html", error=error)

        return render_template("result.html", 
                               filename=result["pdf_filename"],
                               issues=result["total_issues"],
                               repo=result["repo_url"],
                               repo_name=result["repo_name"])

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join("reports", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "❌ File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
