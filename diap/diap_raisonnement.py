"""Mission 4 — Expérience : conclure d'abord VS décomposer d'abord."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

QUESTION = (
    "J'ai 3 réunions demain : 9h à Bruxelles, 14h à Anvers, 17h à Bruxelles. "
    "Est-ce réalisable ?"
)


def demander(question, methode):
    """Même modèle, même question. Seule la CONSIGNE change."""
    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=methode,          # ← la consigne de travail
        messages=[{"role": "user", "content": question}],
    )
    return reponse.content[0].text, reponse.usage.output_tokens


SANS = "Réponds directement et brièvement."

AVEC = (
    "Avant de conclure, décompose le problème étape par étape : "
    "liste les contraintes, examine-les une par une, puis seulement "
    "après, donne ta conclusion."
)

for nom, methode in [("SANS méthode", SANS), ("AVEC méthode", AVEC)]:
    print("═" * 60)
    print(nom)
    print("═" * 60)
    texte, tokens = demander(QUESTION, methode)
    print(texte)
    print(f"\n[tokens sortis : {tokens}]\n")