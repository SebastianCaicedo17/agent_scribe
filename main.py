import argparse
import sys
from datetime import datetime
from pathlib import Path

from backend import transcribe, summarize


def to_markdown(compte_rendu: dict, date: str) -> str:
    md = f"# {compte_rendu['titre']}\n\n"
    md += f"**Date :** {date}\n\n"
    md += f"## Résumé\n\n{compte_rendu['resume']}\n\n"

    md += "## Points clés\n\n"
    for point in compte_rendu["points_cles"]:
        md += f"- {point}\n"
    md += "\n"

    md += "## Décisions / Actions\n\n"
    if compte_rendu["decisions_actions"]:
        for action in compte_rendu["decisions_actions"]:
            md += f"- {action}\n"
    else:
        md += "*(aucune décision ou action identifiée)*\n"

    return md


def main():
    parser = argparse.ArgumentParser(
        description="Scribe — transcription et compte rendu d'un fichier audio"
    )
    parser.add_argument("audio", help="Chemin vers le fichier audio")
    parser.add_argument(
        "--language", "-l", default="fr", help="Langue de l'audio (défaut : fr)"
    )
    args = parser.parse_args()

    print("Transcription en cours...")
    try:
        texte = transcribe(Path(args.audio), language=args.language)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        sys.exit(1)

    print("Rédaction du compte rendu...")
    try:
        compte_rendu = summarize(texte)
    except RuntimeError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now()
    contenu_md = to_markdown(compte_rendu, now.strftime("%Y-%m-%d %H:%M"))
    output_path = Path(f"compte_rendu_{now.strftime('%Y%m%d_%H%M%S')}.md")
    output_path.write_text(contenu_md, encoding="utf-8")

    print("\n" + contenu_md)
    print(f"Compte rendu sauvegardé → {output_path}")


if __name__ == "__main__":
    main()
