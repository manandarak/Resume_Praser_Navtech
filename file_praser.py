import os
import re
import json
import PyPDF2
import docx
from dotenv import load_dotenv

load_dotenv()

def parse_file(file_path):
    """Extracts raw text from the resume file."""
    print(f"-> Running [File Parser] on {file_path}...")
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    elif ext == '.docx':
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        raise ValueError("Unsupported file type. Please use .pdf or .docx")
        
    return text