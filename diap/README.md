# Code de l'agent DIAP

Ce dossier contient le code de l'agent, qui grandit brique par brique.

- `premier_appel.py` — brique **LLM** : premier appel à un modèle de langage.
- `meteo.py` — brique **API** : appeler une API réelle (météo) depuis Python.
- `diap_meteo.py` — brique **API** : function calling — DIAP décide lui-même
  d'aller chercher l'information, le code exécute.
- `diap_memoire.py` — brique **Mémoire** : DIAP se souvient de la conversation.
- `diap_raisonnement.py` — brique **Raisonnement** : Chain of Thought — le rôle
  `system` impose à DIAP de décomposer un problème avant de conclure.
- `diap_outils.py` — brique **Outils** : un outil qui **agit** au lieu de lire.
  DIAP écrit un vrai fichier, après confirmation humaine (*human in the loop*).
- `diap_api.py` — brique **Backend** : DIAP devient un service. Un serveur (Uvicorn) qui **écoute** en continu, et des routes (FastAPI) accessibles depuis un navigateur.
La dernière brique (déploiement) viendra enrichir ce même agent — pas des exercices séparés, mais un DIAP qui évolue.