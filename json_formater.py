import re
import json

def format_as_json(raw_model_output, output_file="output.json"):
    """Validates, formats, and saves the model output into a strict JSON file."""
    print("-> Running [JSON Formatter]...")

    try:
        # ✅ Case 1: Already a dict → no processing needed
        if isinstance(raw_model_output, dict):
            parsed_json = raw_model_output

        # ✅ Case 2: String → clean + parse
        elif isinstance(raw_model_output, str):
            cleaned_output = raw_model_output.strip()

            # Remove ```json ``` or ``` wrappers
            cleaned_output = re.sub(r'```json\n|```', '', cleaned_output)

            # Fix common LLM issues
            cleaned_output = re.sub(r",\s*}", "}", cleaned_output)
            cleaned_output = re.sub(r",\s*]", "]", cleaned_output)

            parsed_json = json.loads(cleaned_output)

        else:
            raise ValueError("Unsupported data type from model")

        # ✅ Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=4, ensure_ascii=False)

        print(f"✅ JSON successfully saved to {output_file}")

        return parsed_json

    except Exception as e:
        print(f"❌ Error: {e}")

        fallback = {
            "error": "Failed to format JSON",
            "raw_output": str(raw_model_output)
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(fallback, f, indent=4)

        return fallback