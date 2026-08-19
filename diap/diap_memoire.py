"""Mission 3 — Donner une mémoire à DIAP : une conversation qui se souvient."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── LA mémoire de DIAP : une simple liste qui va grandir ──
messages = []


def parler_a_diap(message_utilisateur):
    # 1. on ajoute le message de l'utilisateur à la mémoire
    messages.append({"role": "user", "content": message_utilisateur})

    # 2. on envoie TOUTE la mémoire (pas juste le dernier message)
    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=messages,
    )

    # 3. on récupère la réponse et on l'ajoute AUSSI à la mémoire
    texte = reponse.content[0].text
    messages.append({"role": "assistant", "content": texte})
    return texte


# ── petite conversation de test ──
print("DIAP :", parler_a_diap("Salut ! Je m'appelle Diapkuik."))
print("DIAP :", parler_a_diap("Quel est mon prénom ?"))
print("DIAP :", parler_a_diap("Peux-tu l'écrire à l'envers ?"))

print(f"\n[mémoire : {len(messages)} messages accumulés]")