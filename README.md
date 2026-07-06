# Scribe

Scribe transcrit un fichier audio et génère un compte rendu structuré en utilisant l'API Groq (Speech-to-Text + LLM).

## Fonctionnement

```
Fichier audio → transcribe() → texte brut → summarize() → compte rendu Markdown daté
```

## Structure du projet

```
agent_scribe/
├── main.py             # Point d'entrée CLI
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
python main.py <fichier_audio> [--language LANGUE]
```

### Exemple complet

```bash
python main.py AudioTest.ogg
```

```
Transcription en cours...
Rédaction du compte rendu...

# Réunion de lancement du projet Scribe

**Date :** 2026-07-06 14:32

## Résumé

L'équipe a présenté les objectifs du projet Scribe, un outil de transcription
et de synthèse automatique de réunions. Les grandes étapes du développement
ont été passées en revue et les responsabilités réparties entre les membres.

## Points clés

- Le projet utilise l'API Groq pour la transcription et la génération de texte
- La livraison de la v0.1.0 est prévue avant la fin du sprint
- Un fichier audio d'exemple sera commité pour faciliter les tests

## Décisions / Actions

- Sébastien prend en charge l'intégration Streamlit
- Les tests seront réalisés avec des enregistrements de 30 secondes maximum

Compte rendu sauvegardé → compte_rendu_20260706_143201.md
```

Le fichier Markdown est automatiquement créé dans le répertoire courant avec un nom horodaté (`compte_rendu_YYYYMMDD_HHMMSS.md`).

### Changer la langue

```bash
python main.py interview.mp3 --language en
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
| `main` | Code stable — v0.1.0 |
| `dev` | Intégration continue |
| `feature/transcription` | Étape 3 — fonction `transcribe()` |
| `feature/summary` | Étape 4 — fonction `summarize()` |
| `feature/cli` | Étape 5 — CLI `main.py`, sortie Markdown datée |
