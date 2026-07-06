from groq import Groq, APIError
from pathlib import Path

from config import GROQ_API_KEY, STT_MODEL


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


if __name__ == "__main__":
    import sys

    HERE = Path(__file__).parent
    audio = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "AudioTest.ogg"
    print(transcribe(audio))
