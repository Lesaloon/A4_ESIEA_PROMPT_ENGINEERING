import requests
import json
import dotenv
import argparse

dotenv.load_dotenv()

def call_ollama_api(prompt, model="mistral", temperature=0.7, top_p=0.9, top_k=40):
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
    parser = argparse.ArgumentParser(description="Call Ollama API with a prompt.")
    parser.add_argument("prompt", type=str, help="The prompt to send to the model.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature.")
    parser.add_argument("--top_p", type=float, default=0.9, help="Top-p sampling value (0 to 1).")
    parser.add_argument("--top_k", type=int, default=40, help="Top-k sampling value (0 to 100).")
    args = parser.parse_args()

    try:
        TEMPERATURE = args.temperature
        TOP_P = args.top_p # 0 to 1
        TOP_K = args.top_k # 0 to 100
        print(f"Using parameters: temperature={TEMPERATURE}, top_p={TOP_P}, top_k={TOP_K}")
        result = call_ollama_api(args.prompt, temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K)
        response = result['response'].strip()
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")