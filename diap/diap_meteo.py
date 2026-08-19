"""Mission 2B — DIAP décide seul d'appeler la météo (function calling)."""
import os, requests
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ── 1. l'outil : ton code de 2A, rangé dans une fonction ──
def get_meteo(ville):
    url = f"https://wttr.in/{ville}?format=j1"
    donnees = requests.get(url).json()
    actuel = donnees["current_condition"][0]
    return f"{actuel['temp_C']}°C, {actuel['weatherDesc'][0]['value']}"


# ── 2. la description de l'outil pour le LLM (le "menu") ──
outils = [
    {
        "name": "get_meteo",
        "description": "Donne la météo actuelle d'une ville.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ville": {"type": "string",
                          "description": "Le nom de la ville, ex: Lyon"}
            },
            "required": ["ville"],
        },
    }
]

# ── 3. on pose la question, en présentant l'outil ──
question = "quel est la question que je t'ai posé hier?"
messages = [{"role": "user", "content": question}]

reponse = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    tools=outils,
    messages=messages,
)

# ── 4. le LLM a-t-il demandé un outil ? ──
if reponse.stop_reason == "tool_use":
    bloc_outil = next(b for b in reponse.content if b.type == "tool_use")
    ville_demandee = bloc_outil.input["ville"]
    print(f"🔧 DIAP a décidé d'appeler get_meteo(ville='{ville_demandee}')")

    # TON code exécute réellement la fonction
    resultat = get_meteo(ville_demandee)
    print(f"🌡️  Résultat de l'outil : {resultat}")

    # on renvoie le résultat au LLM pour la réponse finale
    messages.append({"role": "assistant", "content": reponse.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": bloc_outil.id,
            "content": resultat,
        }],
    })

    finale = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        tools=outils,
        messages=messages,
    )
    print(f"\n💬 DIAP : {finale.content[0].text}")
else:
    print(f"💬 DIAP (sans outil) : {reponse.content[0].text}")