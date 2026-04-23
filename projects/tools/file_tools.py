from langchain.tools import tool
import os

BASE_DIR = "./data"

@tool
def write_file(path: str, content: str) -> str:
    """파일에 데이터를 저장한다."""
    full_path = os.path.join(BASE_DIR, path.strip("/"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return f"WRITE:{path}"

@tool
def read_file(path: str) -> str:
    """파일을 읽는다."""
    full_path = os.path.join(BASE_DIR, path.strip("/"))
    
    if not os.path.exists(full_path):
        return "FILE_NOT_FOUND"
    
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()
