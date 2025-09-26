#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercice 4: Génération de code avec Ollama - Version fonctions simples
"""

import requests
import json
import dotenv

# Charger les variables d'environnement
dotenv.load_dotenv()

# Configuration par défaut
DEFAULT_MODEL = "codestral"
DEFAULT_TEMPERATURE = 0.2
OLLAMA_URL = dotenv.get_key('.env', 'OLLAMA_URL') or "http://localhost:11434"


def call_ollama_api(prompt: str, system: str = "", model: str = DEFAULT_MODEL) -> str:
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
            "temperature": DEFAULT_TEMPERATURE,
            "top_p": 0.9,
            "top_k": 40,
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


def generate_function(description: str) -> str:
    """
    Génère une fonction Python basée sur une description.

    Args:
        description (str): Description de la fonction à générer

    Returns:
        str: Code Python généré
    """
    system = """You are a Python expert. Generate ONLY valid Python code.
    No explanations, no comments, no markdown formatting.
    Return ONLY the function code, nothing else."""

    prompt = f"Write a Python function that {description}. Return only the code."

    code = call_ollama_api(prompt, system)
    return code


def generate_script(description: str) -> str:
    """
    Génère un script Python basé sur une description.

    Args:
        description (str): Description du script à générer

    Returns:
        str: Code Python généré
    """
    system = """You are a Python expert. Generate ONLY valid Python code.
    No explanations, no comments, no markdown formatting, no text descriptions.
    Return ONLY executable Python code, nothing else."""

    prompt = f"Write a Python script that {description}. Return only the code."

    code = call_ollama_api(prompt, system)
    return code


def demo_simple_generation():
    """Démonstration simple de génération de code."""
    print("=== Exercice 4: Génération de code avec Ollama ===\n")

    # Test 1: Génération de fonctions
    print("1. Génération de fonctions Python:")

    functions_to_generate = [
        "calcule le factoriel d'un nombre",
        "vérifie si un nombre est premier",
        "inverse une chaîne de caractères",
        "trouve le maximum dans une liste"
    ]

    for i, description in enumerate(functions_to_generate, 1):
        print(f"\n📝 Fonction {i}: {description}")
        print("-" * 50)
        code = generate_function(description)

        if code:
            print("Code généré:")
            print(code)
        else:
            print("❌ Erreur lors de la génération")

        print("-" * 50)

    print("\n" + "="*60 + "\n")

    # Test 2: Génération de scripts
    print("2. Génération de scripts Python:")

    scripts_to_generate = [
        "lit un fichier texte et compte les mots",
        "génère une liste de nombres aléatoires et les trie",
        "crée un dictionnaire à partir de deux listes",
        "lire un CSV et retourner une liste d'objets"
    ]

    for i, description in enumerate(scripts_to_generate, 1):
        print(f"\n📄 Script {i}: {description}")
        print("-" * 50)
        code = generate_script(description)

        if code:
            print("Code généré:")
            print(code)
        else:
            print("❌ Erreur lors de la génération")

        print("-" * 50)


if __name__ == "__main__":
    demo_simple_generation()