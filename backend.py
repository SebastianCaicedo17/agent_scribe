import json
from groq import Groq, APIError
from pathlib import Path

from config import GROQ_API_KEY, STT_MODEL, LLM_MODEL

HERE = Path(__file__).parent


def transcribe(audio_path: str | Path, language: str = "fr") -> str:
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier audio introuvable : {path}")

    client = Groq(api_key=GROQ_API_KEY)
    try:
        with open(path, "rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model=STT_MODEL,
                prompt="Transcris l'audio avec précision.",
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
                language=language,
                temperature=0.0,
            )
    except APIError as exc:
        raise RuntimeError(f"Erreur API Groq (transcription) : {exc}") from exc

    return response.text


def summarize(transcription: str) -> dict:
    system_prompt = (HERE / "system_prompt.txt").read_text(encoding="utf-8")

    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcription},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
    except APIError as exc:
        raise RuntimeError(f"Erreur API Groq (résumé) : {exc}") from exc

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    import sys

    audio = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "AudioTest.ogg"
    texte = transcribe(audio)
    print("--- Transcription ---")
    print(texte)
    print("\n--- Compte rendu ---")
    compte_rendu = summarize(texte)
    print(json.dumps(compte_rendu, ensure_ascii=False, indent=2))
