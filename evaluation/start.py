import requests
import json
import os
import dotenv
import re
from typing import Optional, Dict, Any

# Charger les variables d'environnement
dotenv.load_dotenv()

# Configuration par défaut
DEFAULT_MODEL = "gemma3"
DEFAULT_TEMPERATURE = 0.7
# J'utilise un autre ordinateur pour Ollama pour avoir de meilleures performances. Vérifier que l'URL est correcte dans le .env
OLLAMA_URL = os.getenv('OLLAMA_URL', "http://localhost:11434")
CONFIG = json.load(open("config.json"))

def call_ollama_api(prompt: str, system: str = "", model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, top_p: float = 0.9, top_k: int = 40) -> str:
    """
    Appelle l'API Ollama pour générer du contenu.

    Args:
        prompt (str): Le prompt à envoyer
        system (str): Instructions système
        model (str): Modèle à utiliser

    Returns:
        str: La réponse générée
    """
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "system": system,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }
    }

    try:
        response = requests.post(url, data=json.dumps(payload))

        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        else:
            print(f"Erreur API: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Erreur lors de l'appel à Ollama: {e}")
        return ""

def clean_json_response(response: str) -> str:
    """
    Nettoie la réponse pour extraire le JSON valide.
    
    Args:
        response (str): Réponse brute contenant potentiellement du JSON
        
    Returns:
        str: JSON nettoyé
    """
    # Supprimer les backticks et marqueurs de code
    response = re.sub(r'```json\n?', '', response)
    response = re.sub(r'```\n?', '', response)
    response = re.sub(r'`', '', response)
    
    # Chercher le JSON entre accolades
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        return json_match.group(0).strip()
    
    # Si pas de match, retourner la réponse nettoyée
    return response.strip()

def runstep(step: str, data: Optional[Dict[str, Any]] = None) -> str:
    """
    Exécute une étape avec injection des données dans le prompt

    Args:
        step (str): Le nom de l'étape (step1, step2, etc.)
        data (dict): Dictionnaire contenant les données à injecter

    Returns:
        str: La réponse générée
    """
    if data is None:
        data = {}

    # Récupérer la configuration de l'étape
    step_config = CONFIG[step]
    prompt_template = step_config['prompt']

    # Injecter les données dans le prompt
    try:
        prompt = prompt_template.format(**data)
    except KeyError as e:
        print(f"Erreur: placeholder manquant dans les données: {e}")
        prompt = prompt_template

    temperature = step_config['temperature']
    top_p = step_config['top_p']
    top_k = step_config['top_k']
    model = step_config['model']

    # Récupérer max_tokens si disponible
    max_tokens = step_config.get('max_tokens', None)

    response = call_ollama_api(
        prompt=prompt,
        system="",
        model=model,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k
    )
    return response

if __name__ == "__main__":
    # Lire le fichier de données
    input_text = open("data.txt", "r", encoding="utf-8").read()
    print(f"Texte lu ({len(input_text)} caractères)")

    # Step 1: Extraction des points clés
    print("\n=== STEP 1: Extraction des points clés ===")
    keypoint = runstep("step1", {"data": input_text})
    print("Points clés extraits:")
    print(keypoint)
    print(f"Longueur réponse: {len(keypoint)} caractères")

    # Step 2: Récupération du thème général
    print("\n=== STEP 2: Thème général ===")
    general_topic = runstep("step2", {"data": input_text})
    print("Sujet général:")
    print(general_topic)
    print(f"Longueur réponse: {len(general_topic)} caractères")

    # Step 3: Génération des questions
    print("\n=== STEP 3: Génération du quiz ===")
    quiz = runstep("step3", {"data": input_text, "key_points": keypoint, "theme": general_topic})
    print("Quiz généré:")
    print(quiz)
    print(f"Longueur réponse: {len(quiz)} caractères")

    # Step 4: Validation du quiz avec retry
    print("\n=== STEP 4: Validation ===")
    max_retries = 3
    validation_failures = 0
    validation_success = False

    for attempt in range(1, max_retries + 1):
        print(f"\nTentative de validation {attempt}/{max_retries}")
        validation = runstep("step4", {"key_points": keypoint, "quiz": quiz})
        print("Validation du quiz:")
        print(validation)
        print(f"Longueur réponse: {len(validation)} caractères")

        if "OUI" in validation.upper():
            print(f"\n✅ Le quiz est valide (tentative {attempt}).")
            validation_success = True
            break
        else:
            validation_failures += 1
            print(f"\n❌ Validation échouée (tentative {attempt}).")
            if attempt < max_retries:
                print("Nouvelle tentative de validation...")
            else:
                print("Toutes les tentatives de validation ont échoué.")

    # Vérifier le nombre d'échecs et décider si on continue
    if validation_failures >= 2 and not validation_success:
        print(f"\n🚫 ERREUR: La validation a échoué {validation_failures} fois sur {max_retries} tentatives.")
        assert False, f"La validation du quiz a échoué {validation_failures} fois. Quiz non valide."
    elif not validation_success:
        print("\n⚠️ Validation échouée mais on continue pour tester le JSON...")

    # Step 5: Conversion en JSON
    print("\n=== STEP 5: Conversion JSON ===")
    json_quiz_raw = runstep("step5", {"quiz": quiz})
    print("Quiz en format JSON (brut):")
    print(json_quiz_raw)

    # Nettoyer la réponse JSON
    json_quiz = clean_json_response(json_quiz_raw)
    print("\nQuiz en format JSON (nettoyé):")
    print(json_quiz)

    # Parse the json to make sure it's valid
    try:
        quiz_data = json.loads(json_quiz)
        print("\n✅ Le quiz JSON est valide.")
        print(f"Nombre de questions: {len(quiz_data.get('quiz', []))}")
        # save to file
        with open("quiz.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        assert False, f"❌ Le quiz JSON n'est pas valide: {e}"