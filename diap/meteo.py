"""Mission 2A — Donner des yeux à DIAP : appeler une API météo réelle."""
import requests

# 1. la "porte" du service météo (API gratuite, sans clé)
ville = "Brussels"
url = f"https://wttr.in/{ville}?format=j1"

# 2. on frappe à la porte : une requête
reponse = requests.get(url)

# 3. la réponse arrive en JSON -> on la transforme en dict Python
donnees = reponse.json()

# 4. on pioche ce qui nous intéresse dans la structure
actuel = donnees["current_condition"][0]
temp = actuel["temp_C"]
desc = actuel["weatherDesc"][0]["value"]

print(f"À {ville}, il fait {temp}°C — {desc}.")