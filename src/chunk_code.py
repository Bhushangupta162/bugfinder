from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_all_code_files(code_files):
    """Reads code files and splits them into chunks using LangChain."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Each chunk will be ~1000 characters
        chunk_overlap=100  # Overlap between chunks to maintain context
    )

    chunked_code = {}

    for file_path in code_files:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        chunks = text_splitter.split_text(code)  # LangChain splits text
        chunked_code[file_path] = chunks

    return chunked_code
