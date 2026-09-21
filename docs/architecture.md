# 🏗️ Architecture de DIAP

Document vivant : il se densifie à chaque brique ajoutée.

## Vue d'ensemble

Un agent n'est pas un modèle : c'est une **architecture** autour d'un modèle.
DIAP orchestre plusieurs composants pour percevoir, se souvenir, raisonner et agir.

```
          Utilisateur
               |
               v
        Navigateur (HTTP)
               |
               v
  +---------------------------+
  |  Uvicorn (le serveur)     |
  |  +---------------------+  |
  |  |  FastAPI (routes)   |  |
  |  +---------------------+  |
  +---------------------------+
               |
               v
        +--------------+
        | DIAP (agent) |
        +--------------+
               |
     +------+--+-----+------+
     |      |        |      |
     v      v        v      v
    LLM  Mémoire  Raisonn. Outils
                            |
                            v
                   APIs / monde réel
```

## État des briques

| Brique        | État        | Rôle                                              |
|---------------|-------------|---------------------------------------------------|
| LLM           | ✅ fait     | Comprendre et générer du langage                  |
| API           | ✅ fait     | Accéder au monde réel (function calling)          |
| Mémoire       | ✅ fait     | Se souvenir de la conversation                    |
| Raisonnement  | ✅ fait     | Décomposer un problème avant de conclure          |
| Outils        | ✅ fait     | Utiliser et choisir parmi plusieurs outils        |
| Backend       | ✅ fait     | Exposer DIAP comme un service                     |
| Déploiement   | ⬜ à venir  | Faire tourner DIAP en ligne                       |

## Ce qu'on a appris, brique par brique

- **LLM** — le modèle reste chez son fournisseur ; on lui parle par une API,
  et la clé d'API est un badge personnel qui ne quitte jamais le `.env`.
- **API** — une API n'est pas réservée aux IA : c'est le moyen standard pour
  deux programmes de se parler. Avec le *function calling*, **le LLM décide,
  le code exécute**.
- **Mémoire** — un LLM est sans état : il ne se souvient de rien. La mémoire
  n'est pas dans le modèle, elle est **dans notre code** — une liste de
  messages qu'on accumule et qu'on renvoie en entier à chaque appel.
- **Raisonnement** — faire raisonner DIAP, ce n'est pas le rendre plus intelligent : c'est lui **imposer une méthode** (décomposer avant de   conclure), via le rôle `system`.
- **Outils** — lire ≠ agir. Un outil qui agit laisse une trace : toute action irréversible passe par une confirmation humaine (*human in the  loop*), et on ne fait jamais confiance aux paramètres d'un LLM sans les filtrer.
- **Backend** — un script s'exécute puis meurt ; un serveur **écoute**. Uvicorn fait tourner le serveur, FastAPI définit les routes. `GET` pour lire, `POST` pour envoyer.

## Notes de conception

- **Sécurité au point d'usage** : les secrets (clés API) vivent dans `.env`,
  jamais dans le code ni dans l'historique Git.
- **Coût maîtrisé** : chaque brique documente ce qu'elle coûte réellement
  (tokens, appels). La mémoire, notamment, fait grandir le coût de chaque
  appel puisqu'on renvoie tout l'historique.

*(Ce document s'étoffe à mesure que DIAP gagne des capacités.)*
