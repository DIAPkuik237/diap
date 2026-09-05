# 🎥 Correspondance épisodes ⇄ code

Chaque épisode de la série **« De zéro à Architecte IA »** ajoute une capacité
à DIAP. Ce tableau relie chaque vidéo au fichier de code correspondant.

| Épisode | Brique | Fichier | Vidéo |
|---------|--------|---------|-------|
| **Ép. 1** — On démonte un agent IA | *Anatomie (étape)* | – | [regarder](https://youtu.be/ALQ734wucYc) |
| **Ép. 2** — Comment parler à une IA ? | 🟩 **LLM** | [`premier_appel.py`](../diap/premier_appel.py) | [regarder](https://youtu.be/9U1OrD1HkxY) |
| **Ép. 3** — On donne des yeux à une IA | 🟩 **API** | [`meteo.py`](../diap/meteo.py) · [`diap_meteo.py`](../diap/diap_meteo.py) | [regarder](https://youtu.be/YOokoooXgvo) |
| **Ép. 4** — DIAP oublie tout | 🟩 **Mémoire** | [`diap_memoire.py`](../diap/diap_memoire.py) | [regarder](https://youtu.be/UrDavH1GViY) |
| **Ép. 5** — DIAP répond trop vite (réparons ça) | 🟩 Raisonnement | [`diap_raisonnement.py`](../diap/diap_raisonnement.py) | [regarder](https://youtu.be/ZllNQHJTifs) |
| **Ép. 6** — DIAP passe à l'action | 🟩 **Outils** | `diap_outils.py` | [regarder](LIEN_VIDEO) |

## 📂 Les fichiers, dans l'ordre de construction
- **`premier_appel.py`** — le premier appel à un modèle de langage.
  DIAP prononce ses premiers mots.

- **`meteo.py`** — appeler une API réelle (météo) depuis Python.
  On découvre qu'une API n'est pas réservée aux IA.

- **`diap_meteo.py`** — le *function calling* : DIAP décide **lui-même**
  d'aller chercher l'information. Le LLM décide, le code exécute.

- **`diap_memoire.py`** — la mémoire de conversation : une liste de messages
  qu'on accumule et qu'on renvoie en entier à chaque appel.

- **`diap_raisonnement.py`** — *Chain of Thought* : DIAP décompose un problème avant de conclure, grâce au rôle *system* qui lui impose une méthode de travail.
- **`diap_outils.py`** — un outil qui **agit** au lieu de lire : DIAP écrit un vrai fichier sur le disque, avec une confirmation humaine avant chaque action (*human in the loop*).

---

📺 **Playlist complète** : https://www.youtube.com/playlist?list=PLX1O_iVn_fzc
