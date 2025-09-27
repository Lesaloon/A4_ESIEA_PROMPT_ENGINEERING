# Évaluation Prompt Engineering

Cas choisis : Cas 2 - Génération de quiz

## Instructions

L'objectif de ce cas est de concevoir un quiz automatiquement à partir d'un texte donné.

## Étapes de prompts (Implémentation finale)

### Étape 1 : Extraction des points clés et concepts

1. **Prompt** : "Identifie les points clés et les concepts importants dans le texte suivant : {data}."
2. **Objectif** : Extraire les informations essentielles qui seront la base des questions du quiz.
3. **température** : 0.7 ( Permet une certaine créativité dans l'extraction des points clés )
4. **top_p** : 0.9 ( Permet de se concentrer sur les réponses les plus probables )
5. **top_k** : 50 ( Limite le nombre de mots considérés pour la génération de la réponse )
6. **model** : "gemma3" ( Modèle pour la compréhension du texte )

### Étape 2 : Récupération du thème général

1. **Prompt** : "Quel est le thème général du texte suivant : {data}."
2. **Objectif** : Comprendre le contexte global pour formuler des prompts plus pertinents par la suite
3. **température** : 0.3 ( L'on cherche ici une réponse précise et non créative )
4. **top_p** : 0.9 ( Permet de se concentrer sur les réponses les plus probables )
5. **top_k** : 50 ( Limite le nombre de mots considérés pour la génération de la réponse )
6. **model** : "gemma3" ( Modèle pour la compréhension du texte )

### Étape 3 : Génération des questions (Raffinée)

1. **Prompt** : "À partir des points clés suivants : {key_points} et du thème général : {theme}, génère exactement 4 questions de quiz avec 4 options chacune. Format strict à respecter:\n\nQuestion 1: [Texte de la question]\nA) [Option A]\nB) [Option B] \nC) [Option C]\nD) [Option D]\nRéponse correcte: [Texte complet de la bonne réponse]\n\nQuestion 2: [Texte de la question]\nA) [Option A]\nB) [Option B]\nC) [Option C] \nD) [Option D]\nRéponse correcte: [Texte complet de la bonne réponse]\n\n[Continue pour 4 questions]"
2. **Objectif** : Créer des questions structurées qui évaluent la compréhension des concepts clés.
3. **température** : 1.0 ( Permet une certaine variété dans les questions générées )
4. **top_p** : 0.95 ( Permet de générer des questions variées mais toujours pertinentes )
5. **top_k** : 100 ( Permet de générer des questions variées mais toujours pertinentes )
6. **model** : "gemma3" ( Modèle pour la compréhension du texte )

### Étape 4 : Validation des questions

1. **Prompt** : "Donne ta réponse sous le format suivant: OUI / NON. Vérifie que le quiz suivant est cohérent, que les réponses sont correctes et que les questions couvrent bien les points clés suivants : {key_points}. Quiz à valider : {quiz}"
2. **Objectif** : S'assurer que le quiz est de qualité et couvre bien les concepts importants.
3. **température** : 0.2 ( L'on cherche ici une réponse précise et non créative )
4. **top_p** : 0.9 ( Permet de se concentrer sur les réponses les plus probables )
5. **top_k** : 1 ( Limite le nombre de mots considérés pour la génération de la réponse )
6. **max_tokens** : 10 ( Limite la réponse à un simple "OUI" ou "NON" )
7. **model** : "gemma3" ( Modèle pour la compréhension du texte )

remarque: j'ai tenter beaucoup de chose diférent pour qu'il ne réponde que par oui ou non, mais rien n'y fait, le model dit douvent "Okay / NON" ou "OUI, le quiz est bon" ou "NON, il y a des erreurs" etc. J'ai donc mis une assertion dans le code pour que si il y a 2 échecs de validation, le script s'arrête.

ps. j'ai mis un regex du format dans le prompt et ça a l'air de mieux marcher mais je ne suis pas sûr que ça soit optimal.

### Étape 5 : Passage en JSON (Raffinée)

1. **Prompt** : "Convertis le quiz suivant en format JSON valide. Retourne UNIQUEMENT le JSON, sans texte d'explication, sans backticks, sans marqueurs de code. IMPORTANT: utilise le texte complet des questions et des réponses, PAS des lettres A/B/C/D. Format attendu: {{\"quiz\": [{{\"question\": \"Texte complet de la vraie question?\", \"options\": [\"Texte complet option 1\", \"Texte complet option 2\", \"Texte complet option 3\", \"Texte complet option 4\"], \"answer\": \"Texte complet de la bonne réponse\"}}]}}. Quiz à convertir : {quiz}"
2. **Objectif** : Structurer le quiz dans un format JSON exploitable avec les textes complets.
3. **température** : 0.2 ( Température réduite pour plus de précision )
4. **top_p** : 0.9 ( Permet de se concentrer sur les réponses les plus probables )
5. **top_k** : 50 ( Limite le nombre de mots considérés pour la génération de la réponse )
6. **model** : "codellama" ( Modèle pour la génération de code probablement plus rigoureux sur la génération du JSON )

## Source des données

Le système de génération de quiz utilise comme matériau source l'article de recherche d'**Anthropic sur "Agentic Misalignment: How LLMs could be insider threats"**.

### Détails de la source
- **Titre** : Agentic Misalignment: How LLMs could be insider threats
- **Source** : anthropic.com
- **Type de contenu** : Article de recherche en sécurité IA (lecture de 47-60 minutes)
- **Fichier** : `data.txt` (321 lignes)

### Aperçu du contenu de recherche
L'article présente des résultats expérimentaux sur les problèmes d'alignement IA, spécifiquement :

- **Portée de la recherche** : Tests de 16 modèles LLM différents pour les comportements d'agents autonomes dans des environnements d'entreprise
- **Principales conclusions** : Les modèles ont démontré des comportements potentiels de "menace interne" face à des conflits d'objectifs ou des menaces de remplacement
- **Méthodes expérimentales** : Scénarios contrôlés testant les comportements de chantage et d'espionnage industriel
- **Approche technique** : Démonstrations d'utilisation informatique et expériences basées sur des prompts textuels

### Pertinence pour la génération de quiz
Cet article de recherche fournit un contenu riche et technique parfait pour tester les capacités de génération de quiz :
- Concepts techniques complexes nécessitant une compréhension approfondie
- Méthodologies expérimentales détaillées et résultats
- Informations multi-niveaux couvrant la sécurité IA, les scénarios d'entreprise et l'analyse comportementale
- Contenu structuré avec des conclusions et implications claires

La profondeur et la complexité de cette recherche en sécurité IA en font un excellent cas de test pour évaluer si le système de génération de quiz peut extraire des questions et réponses significatives à partir de matériel technique sophistiqué.

## Raffinements et problèmes rencontrés

### Problème 1 : Format des questions générées

**Problème initial** : Les questions générées n'avaient pas un format structuré, rendant difficile la conversion en JSON.

**Solution implémentée** :
- Spécification d'un format strict dans le prompt de l'étape 3 :
  ```
  Question 1: [Texte de la question]
  A) [Option A]
  B) [Option B]
  C) [Option C]
  D) [Option D]
  Réponse correcte: [Texte complet de la bonne réponse]
  ```

### Problème 2 : JSON avec réponses en lettres au lieu de texte complet

**Problème initial** : Le JSON généré utilisait des lettres (A, B, C, D) comme réponses au lieu du texte complet, et des questions génériques ("Question 1") au lieu des vraies questions.

**Exemple du problème** :
```json
{
  "quiz": [
    {
      "question": "Question 1",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "B"
    }
  ]
}
```

**Solution implémentée** :
- Modification du prompt de l'étape 5 avec des instructions explicites :
  - "utilise le texte complet des questions et des réponses, PAS des lettres A/B/C/D"
  - Exemple concret du format attendu dans le prompt
  - Réduction de la température à 0.2 pour plus de précision

**Format JSON final souhaité** :
```json
{
  "quiz": [
    {
      "question": "Qu'est-ce que l'apprentissage automatique ?",
      "options": [
        "Une technologie pour créer des robots",
        "Un processus où les systèmes apprennent automatiquement à partir des données",
        "Un langage de programmation",
        "Une méthode de réparation"
      ],
      "answer": "Un processus où les systèmes apprennent automatiquement à partir des données"
    }
  ]
}
```

### Problème 3 : Nettoyage des réponses JSON

**Problème initial** : Les LLM ajoutaient souvent des backticks, marqueurs de code, ou du texte d'explication autour du JSON.

**Solution implémentée** :
- Création d'une fonction `clean_json_response()` qui :
  - Supprime les backticks et marqueurs de code (`\`\`\`json`, `\`\`\``)
  - Utilise une regex pour extraire le JSON entre accolades
  - Gère les cas où le JSON est malformé

### Problème 4 : Questions générées en anglais

**Problème détecté** : Les questions et réponses générées sont souvent en anglais au lieu du français.

**Analyse de la cause** : Ce comportement est probablement dû au fait que les données d'entrée (`data.txt`) sont en anglais. Le modèle LLM tend à maintenir la langue du contenu source lors de la génération des questions.

**Solution envisagée** :
- Ajout d'une 6ème étape avec un prompt spécialement dédié à la traduction
- Le prompt pourrait être : "Traduis le quiz suivant en français, en gardant le même format JSON et en adaptant les questions et réponses pour un public francophone"
- Paramètres suggérés : température basse (0.2) pour une traduction précise et cohérente

**Impact** : Cette étape supplémentaire permettrait d'avoir des quiz entièrement en français, améliorant l'accessibilité pour les utilisateurs francophones tout en conservant la richesse technique du contenu original.

## Architecture du code

### Fichiers principaux

- **`config.json`** : Configuration des prompts et paramètres pour chaque étape
- **`start.py`** : Script principal qui orchestre les 5 étapes
- **`data.txt`** : Fichier contenant le texte d'entrée à analyser
- **`test_json.py`** : Script de test pour valider le format JSON attendu

### Fonctions clés

- **`call_ollama_api()`** : Interface avec l'API Ollama
- **`runstep()`** : Exécute une étape avec injection des données dans les prompts
- **`clean_json_response()`** : Nettoie les réponses JSON des LLM
- **`main`** : Orchestration des 5 étapes avec gestion d'erreurs et debug

### Flux de données

```
data.txt → Étape 1 (points clés) → keypoint
data.txt → Étape 2 (thème) → general_topic
keypoint + general_topic → Étape 3 (quiz) → quiz
keypoint + quiz → Étape 4 (validation) → validation
quiz → Étape 5 (JSON) → json_quiz → Parsing final
```

## Résultats attendus

À la fin de ce processus, nous obtenons :

1. **Quiz structuré** en format JSON exploitable
2. **Questions pertinentes** basées sur les concepts clés du texte
3. **Réponses complètes** avec le texte intégral (pas de lettres A/B/C/D)
4. **Format standardisé** pour faciliter l'intégration dans d'autres systèmes

**Exemple de sortie finale** :
```json
{
  "quiz": [
    {
      "question": "Qu'est-ce que l'apprentissage automatique (Machine Learning) ?",
      "options": [
        "Une technologie pour créer des robots",
        "Un processus où les systèmes apprennent automatiquement à partir des données sans programmation explicite",
        "Un langage de programmation spécialisé",
        "Une méthode pour réparer les ordinateurs"
      ],
      "answer": "Un processus où les systèmes apprennent automatiquement à partir des données sans programmation explicite"
    }
  ]
}
```

## Utilisation du script
Le script `start.py` peut être lancer via la commande suivante :

```sh
$ python start.py
```