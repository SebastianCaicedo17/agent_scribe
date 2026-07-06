# Scribe

Scribe est un outil qui transforme un enregistrement audio (réunion, cours, note vocale) en compte rendu écrit et structuré.

## Fonctionnement

1. L'utilisateur fournit un fichier audio.
2. Un modèle de transcription (Speech-to-Text) convertit l'audio en texte brut.
3. Un LLM reformule ce texte en compte rendu structuré : titre, résumé, points clés, décisions/actions.

Les modèles sont appelés via l'API serverless de [Groq](https://console.groq.com/docs/overview).

## Modèles utilisés

- **STT (transcription)** : `whisper-large-v3-turbo`
- **LLM (compte rendu)** : `llama-3.3-70b-versatile`

> Justification (Q2) : `[À COMPLÉTER — qualité / vitesse / coût, à motiver par vous deux]`

Les noms de modèles sont centralisés dans `config.py`, à un seul endroit du projet.

## Fonctionnalités actuelles

### Transcription (`backend.py`)

La fonction `transcribe(audio_path, language="fr")` :
- vérifie que le fichier audio existe (sinon lève `FileNotFoundError`) ;
- appelle le modèle STT de Groq (`whisper-large-v3-turbo`) en `verbose_json` avec horodatage par mot et par segment ;
- gère les erreurs d'API Groq en levant une erreur explicite plutôt qu'un plantage silencieux ;
- retourne le texte transcrit.

Test rapide en ligne de commande :

```bash
python backend.py chemin/vers/audio.mp3
```

## Dépendances

| Librairie | Rôle |
|---|---|
| `groq` | appels à l'API Groq (STT + LLM) |
| `dotenv` | chargement de la clé API depuis `.env` |
| `requests` | `[À COMPLÉTER — usage précis dans le projet]` |
| `mistralai` | `[À COMPLÉTER — usage précis]` |
| `pillow` | `[À COMPLÉTER — usage précis]` |
| `plotly` | `[À COMPLÉTER — usage précis]` |
| `streamlit` | interface utilisateur |

## Installation

```bash
git clone https://github.com/SebastianCaicedo17/agent_scribe.git
cd agent_scribe
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
```
