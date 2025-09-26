import requests
import json
import dotenv
import argparse

dotenv.load_dotenv()

def call_ollama_api(prompt, system="", model="mistral", temperature=0.7, top_p=0.9, top_k=40):
    """
    Call the Ollama API with the given prompt and model.
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use (default is "mistral").
    """
    url = f"{dotenv.get_key('.env', 'OLLAMA_URL')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "system": system,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }
    }
    response = requests.post(url, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Call Ollama API with custom parameters.")
    parser.add_argument("--format", type=str, default="JSON", help="Output format: JSON or CSV")

    try:
        TEMPERATURE = 0.1
        TOP_P = 0.5 # 0 to 1
        TOP_K = 40 # 0 to 100
        FORMAT = parser.parse_args().format.upper()
        SYSTEM = "LOW VERBOSE. ONLY ANSWER WITH WHAT IS ASKED. DO NOT ADD BACKTICKS. DO NOT PROTECT THE ANSWER WITH CODE BLOCK."
        PROMPT = f"As a {FORMAT} describe 5 European countries with the following data : Country, Capital, Population (in millions floating point number with 2 digits)"
        print(f"Using parameters: temperature={TEMPERATURE}, top_p={TOP_P}, top_k={TOP_K}")
        result = call_ollama_api(PROMPT, system=SYSTEM, temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K)
        response = result['response'].strip()
        print("="*40)
        print(f"System:\n{SYSTEM}\n")
        print(f"Prompt:\n{PROMPT}\n")
        print("="*40)
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"Error: {e}")