"""Mission 5 — Donner des mains à DIAP : un outil qui AGIT sur le monde."""
import os
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ── L'OUTIL QUI AGIT (il ne lit pas : il écrit) ──
def sauvegarder_note(titre, contenu):
    """Crée un fichier. Cette action laisse une TRACE sur ton disque."""
    dossier = "notes_diap"
    os.makedirs(dossier, exist_ok=True)

    # nom de fichier sûr : on n'accepte pas n'importe quoi du LLM
    nom_propre = "".join(c for c in titre if c.isalnum() or c in " -_").strip()
    nom_propre = nom_propre.replace(" ", "_")[:50] or "note"
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(dossier, f"{horodatage}_{nom_propre}.md")

    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"# {titre}\n\n{contenu}\n")

    return f"Fichier créé : {chemin}"


# ── La description de l'outil pour DIAP ──
outils = [
    {
        "name": "sauvegarder_note",
        "description": (
            "Sauvegarde une note dans un fichier sur le disque de "
            "l'utilisateur. À utiliser quand il demande de sauvegarder, "
            "noter ou archiver quelque chose."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "titre": {"type": "string",
                          "description": "Titre court de la note"},
                "contenu": {"type": "string",
                            "description": "Le contenu complet de la note"},
            },
            "required": ["titre", "contenu"],
        },
    }
]

question = (
    "Fais-moi un résumé en 3 points de ce qu'est une API, "
    "et sauvegarde-le dans une note."
)
messages = [{"role": "user", "content": question}]

reponse = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    tools=outils,
    messages=messages,
)

if reponse.stop_reason == "tool_use":
    bloc = next(b for b in reponse.content if b.type == "tool_use")
    print(f"🔧 DIAP veut appeler : {bloc.name}")
    print(f"   titre   : {bloc.input['titre']}")
    print(f"   contenu : {bloc.input['contenu'][:80]}...")

    # ⚠️ LE GARDE-FOU : on demande confirmation AVANT d'agir
    accord = input("\n➡️  Autoriser cette action ? (o/n) : ")
    if accord.lower() != "o":
        print("❌ Action refusée. Rien n'a été écrit.")
    else:
        resultat = sauvegarder_note(bloc.input["titre"],
                                    bloc.input["contenu"])
        print(f"✅ {resultat}")

        messages.append({"role": "assistant", "content": reponse.content})
        messages.append({"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": bloc.id,
            "content": resultat,
        }]})
        finale = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=500,
            tools=outils, messages=messages,
        )
        print(f"\n💬 DIAP : {finale.content[0].text}")
else:
    print(f"💬 DIAP (sans outil) : {reponse.content[0].text}")