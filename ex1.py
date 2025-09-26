import requests
import json
import dotenv

dotenv.load_dotenv()

def call_ollama_api(prompt, model="gemma3", temperature=0.7, top_p=0.9, top_k=40):
    """
    Call the Ollama API with the given prompt and model.
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use (default is "gemma3").
    """
    url = f"{dotenv.get_key('.env', 'OLLAMA_URL')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }
    }
    response = requests.post(url, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    PROMPT = "Propose un titre original de film d'horreur. Ne donne que le titre, sans autre texte."
    try:
        TEMPERATURE = 1.5
        TOP_P = 0.9 # 0 to 1
        TOP_K = 50 # 0 to 100
        print(f"Using parameters: temperature={TEMPERATURE}, top_p={TOP_P}, top_k={TOP_K}")
        for i in range(5):  # Generate 5 different titles
            result = call_ollama_api(PROMPT, temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K)
            response = result['response'].strip()
            print(f"Response {i+1}: {response}")
    except Exception as e:
        print(f"Error: {e}")