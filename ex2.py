import requests
import json
import dotenv

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

    PROMPTS = [
        "Propose moi le titre d'un film d'horreur et son synopsis.", # Prompt type 1
        "Propose moi le titre d'un film d'horreur et son synopsis. A destination de jeunes adultes. Il sera diffusé sur une plateforme de streaming.", # Prompt type 2
        "Tu est un scénariste dans le style de Kubrick. Propose moi le titre d'un film d'horreur et son synopsis.", # Prompt type 3
        "Propose moi le titre d'un film d'horreur et son synopsis. Le tout en français. Avec un style informel." # Prompt type 4 ( avec contrainte )
    ]
    try:
        TEMPERATURE = 0.8
        TOP_P = 0.9 # 0 to 1
        TOP_K = 50 # 0 to 100
        for prompt in PROMPTS:
            print(f"Prompt used: {prompt}")
            result = call_ollama_api(prompt, temperature=TEMPERATURE, top_p=TOP_P, top_k=TOP_K)
            response = result['response'].strip()
            print(f"Response: {response}")
            print("\n---\n")

    except Exception as e:
        print(f"Error: {e}")