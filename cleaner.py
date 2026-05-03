import os
import re
import json
import PyPDF2
import docx
from dotenv import load_dotenv

load_dotenv()

def clean_text(raw_text):
    """Removes messy formatting, extra spaces, and unreadable characters."""
    print("-> Running [Cleaned Text] module...")
    text = re.sub(r'\s+', ' ', raw_text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()