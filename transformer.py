import os
import re
import json
import PyPDF2
import docx
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

import json
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


def extract_entities_with_transformer(cleaned_text):
    """Passes the cleaned text to the Transformer model for entity extraction."""
    print("-> Running [Transformer NLP Model] & [Entity Extraction]...")

    json_schema = """
    {
      "Contact Information": {"Name": "", "Email": "", "Phone Number": ""},
      "Education History": [{"Institution": "", "Degree": "", "Graduation Year": ""}],
      "Work Experience": [{"Company": "", "Position": "", "Description": "", "Duration": ""}],
      "Skills": []
    }
    """

    prompt = PromptTemplate(
        input_variables=["text", "schema"],
        template="""
You are an advanced resume parsing AI.

Extract structured information from the given resume text.

⚠️ STRICT RULES:
- Output ONLY valid JSON
- Follow the schema EXACTLY
- Do NOT add explanations or extra text
- If data is missing, return empty string "" or empty list []

Text:
{text}

Schema:
{schema}
"""
    )

    # ✅ Updated model (supported by Groq)
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.1-8b-instant"
    )

    formatted_prompt = prompt.format(
        text=cleaned_text,
        schema=json_schema
    )

    try:
        # ✅ Force JSON output
        response = llm.invoke(
            formatted_prompt,
            response_format={"type": "json_object"}
        )

        # ✅ Safely extract content
        content = response.content if hasattr(response, "content") else str(response)

        # ✅ Convert to Python dict
        parsed_json = json.loads(content)

        return parsed_json

    except json.JSONDecodeError:
        print("⚠️ Model returned invalid JSON. Returning raw output...")
        return content

    except Exception as e:
        print(f"❌ Error during entity extraction: {e}")
        return {}