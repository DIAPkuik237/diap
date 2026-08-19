# Code de l'agent DIAP

Ce dossier contient le code de l'agent, qui grandit brique par brique.

- `premier_appel.py` — brique **LLM** : premier appel à un modèle de langage.
- `meteo.py` — brique **API** : appeler une API réelle (météo) depuis Python.
- `diap_meteo.py` — brique **API** : function calling — DIAP décide lui-même
  d'aller chercher l'information, le code exécute.
- `diap_memoire.py` — brique **Mémoire** : DIAP se souvient de la conversation.

Les prochaines briques (raisonnement, outils…) viendront enrichir
ce même agent — pas des exercices séparés, mais un DIAP qui évolue.