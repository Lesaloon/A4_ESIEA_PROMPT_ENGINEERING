import requests
import json

def call_ollama_api(prompt, model="gemma3"):
    """
    Call the Ollama API with the given prompt and model.
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use (default is "gemma3").
    """
    url = f"http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    prompt = "What is the capital of France?"
    try:
        print("Sending prompt to Ollama API...")
        result = call_ollama_api(prompt)
        print("Response from Ollama API:")
        print(result['response'])
    except Exception as e:
        print(f"Error: {e}")