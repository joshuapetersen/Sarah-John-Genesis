import sys
from docx import Document

def extract_text(docx_path):
    doc = Document(docx_path)
    for para in doc.paragraphs:
        print(para.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_docx_memory.py <path_to_docx>")
        sys.exit(1)
    extract_text(sys.argv[1])
