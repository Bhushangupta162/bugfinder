import os
import json
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

bug_analysis_prompt = PromptTemplate(
    input_variables=["code_chunk"],  # ✅ Removed "user_id" (it was causing KeyError)
    template="""
    You are a software engineer reviewing code. Analyze the following Python code and return issues in **strict JSON format**.

    For each issue, include:
    - `description`: A brief explanation of the issue.
    - `severity`: Choose one of ["Critical", "Warning", "Minor"].
    - `recommendation`: How to fix it.

    Also include the **code snippet** related to the issue.

    Code:
    ```python
    {code_chunk}
    ```

    **Strictly return valid JSON** (without markdown formatting) like:
    [
        {{"description": "SQL Injection vulnerability", "severity": "Critical", "recommendation": "Use prepared statements", "code": "user_input = input()"}},
        {{"description": "Inefficient loop", "severity": "Warning", "recommendation": "Use list comprehensions", "code": "for i in range(len(lst)): print(lst[i])"}},
        {{"description": "Missing docstring", "severity": "Minor", "recommendation": "Add a docstring", "code": "def my_function(): pass"}}
    ]
    """
)

def analyze_code_chunk(code_chunk):
    """Analyzes a code chunk and ensures JSON output, including the related code snippet."""
    chain = bug_analysis_prompt | llm
    response = chain.invoke({"code_chunk": code_chunk})

    # 🛠 Remove markdown backticks if present
    cleaned_response = re.sub(r"```json\n(.*?)\n```", r"\1", response, flags=re.DOTALL).strip()

    # Debugging: Print cleaned response
    print("🔍 Cleaned Response:", cleaned_response)

    try:
        issues = json.loads(cleaned_response)  # Ensure it's valid JSON
        return issues
    except json.JSONDecodeError:
        return [{"error": "Failed to parse Gemini response", "raw_output": cleaned_response}]
