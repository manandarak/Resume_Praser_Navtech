import os
import re
import json
import PyPDF2
import docx
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from file_praser import parse_file
from cleaner import clean_text
from transformer import extract_entities_with_transformer
from json_formater import format_as_json

load_dotenv()


# Main Execution Pipeline
def run_resume_pipeline(file_path):
    print("\nStarting Pipeline...")
    
    raw_text = parse_file(file_path)
    text_cleaned = clean_text(raw_text)

    extracted_entities_str = extract_entities_with_transformer(text_cleaned)

    final_json = format_as_json(extracted_entities_str)
    
    print("\n=== FINAL OUTPUT ===")
    print(json.dumps(final_json, indent=2))
    return final_json


if __name__ == "__main__":
    run_resume_pipeline("Manan Darak Resume.pdf")
    pass