# Scribe

Scribe transcrit un fichier audio et génère un compte rendu structuré en utilisant l'API Groq (Speech-to-Text + LLM).

## Fonctionnement

```
Fichier audio → transcribe() → texte brut → summarize() → compte rendu JSON
```

## Structure du projet

```
agent_scribe/
├── backend.py          # Fonctions transcribe() et summarize()
├── config.py           # Chargement des secrets et noms de modèles
├── system_prompt.txt   # Prompt système du LLM (hors code, itérable)
├── .env                # Secrets locaux (non commité)
├── .env.example        # Template des variables attendues
├── requirements.txt    # Dépendances Python
└── AudioTest.ogg       # Fichier audio d'exemple
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

## Configuration

Copie `.env.example` en `.env` et renseigne ta clé :

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=gsk_...
```

La clé est disponible sur [console.groq.com](https://console.groq.com). Si elle est absente au démarrage, le programme échoue immédiatement avec un message explicite.

## Utilisation

```bash
# Avec le fichier audio par défaut (AudioTest.ogg)
python backend.py

# Avec un fichier personnalisé
python backend.py chemin/vers/audio.mp3
```

Sortie attendue :

```
--- Transcription ---
<texte brut retranscrit>

--- Compte rendu ---
{
  "titre": "...",
  "resume": "...",
  "points_cles": ["...", "..."],
  "decisions_actions": []
}
```

## Modèles utilisés

Les noms de modèles sont centralisés dans `config.py` — ils n'apparaissent qu'à un seul endroit du projet.

| Rôle | Modèle | Justification |
|------|--------|---------------|
| STT  | `whisper-large-v3-turbo` | Multilingue (français inclus), rapport qualité/vitesse optimal sur Groq. Plus rapide que `whisper-large-v3` pour une précision très proche. |
| LLM  | `llama-3.3-70b-versatile` | Meilleur modèle disponible sur Groq à date, bon niveau en français, inférence rapide grâce à l'infrastructure Groq. |

## Formats audio acceptés

`mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, `webm`, `ogg` — taille maximale : **25 Mo** par fichier.

## Choix techniques

**Q3 — Ce que l'API STT renvoie en plus du texte**

Avec `response_format="verbose_json"` et `timestamp_granularities=["word", "segment"]` :

- `language` — langue détectée automatiquement
- `duration` — durée totale de l'audio
- `segments[]` — chaque phrase avec `start`, `end`, `text`, `avg_logprob`, `no_speech_prob`
- `words[]` — chaque mot avec son horodatage `start` / `end`

Utile pour une évolution future : sous-titres synchronisés, détection de silences (`no_speech_prob`), navigation dans la transcription par segment.

**Q4 — Température pour le résumé : 0.1**

La tâche est une restitution factuelle, pas une création. Une température basse minimise les hallucinations et la variabilité. On évite 0.0 (risque de boucle sur des tokens identiques) ; 0.1 offre le bon équilibre rigueur/fluidité.

**Q5 — Prompt système et cache de tokens**

Le prompt système est identique à chaque requête. Les APIs LLM mettent en cache le préfixe invariant d'un contexte : si le début du prompt ne change pas entre deux appels, les tokens correspondants ne sont pas re-encodés et leur coût est réduit. Stocker le prompt dans `system_prompt.txt` (fichier fixe, lu à chaque appel) maximise ce taux de cache hit plutôt que de construire un prompt dynamique qui changerait à chaque fois.

## Branches

| Branche | Contenu |
|---------|---------|
| `main` | Code stable |
| `dev` | Intégration continue |
| `feature/transcription` | Étape 3 — fonction `transcribe()` |
| `feature/summary` | Étape 4 — fonction `summarize()` |
