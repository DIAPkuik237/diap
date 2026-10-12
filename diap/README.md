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
- `diap_api.py` — briques **Backend** et **Déploiement** : DIAP devient un
  service. Un serveur (Uvicorn) qui **écoute** en continu, des routes (FastAPI)
  accessibles depuis un navigateur, une page publique `/chat`, et les garde-fous
  nécessaires à un service en ligne (identité via le rôle `system`, longueur
  maximale des messages, limitation du nombre d'appels par visiteur).
  Ce même fichier tourne en ligne : https://diap.onrender.com/chat

Les 7 briques sont posées. Ce n'étaient pas des exercices séparés, mais un
seul DIAP qui a grandi.