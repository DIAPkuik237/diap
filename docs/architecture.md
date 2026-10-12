# 🏗️ Architecture de DIAP

Document vivant : il se densifie à chaque brique ajoutée.

## Vue d'ensemble

Un agent n'est pas un modèle : c'est une **architecture** autour d'un modèle.
DIAP orchestre plusieurs composants pour percevoir, se souvenir, raisonner et agir.

```
     Utilisateur (n'importe où)
               |
               v
   https://diap.onrender.com/chat
               |
               v
+-----------------------------------+
|  Machine allumée 24/7 (Render)    |
|                                   |
|  +-----------------------------+  |
|  |  Uvicorn (le serveur)       |  |
|  |  +-----------------------+  |  |
|  |  |  FastAPI (routes)     |  |  |
|  |  +-----------------------+  |  |
|  +-----------------------------+  |
|                |                  |
|                v                  |
|         +--------------+          |
|         | DIAP (agent) |          |
|         +--------------+          |
|                |                  |
|      +------+--+-----+------+     |
|      |      |        |      |     |
|      v      v        v      v     |
|     LLM  Mémoire  Raisonn. Outils |
+-----------------------------------+
         |                  |
         v                  v
   API Anthropic     APIs / monde réel
   (le modèle)
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
| Déploiement   | ✅ fait     | Faire tourner DIAP en ligne                       |

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
- **Déploiement** — déployer, c'est faire tourner son code sur l'ordinateur de
  quelqu'un d'autre, allumé en permanence. `localhost` n'existe que sur ma
  machine : en ligne, le serveur écoute sur `0.0.0.0`, sur le port imposé par
  l'hébergeur, et la clé API devient une variable d'environnement de
  l'hébergeur. Un service public peut être appelé par n'importe qui : il lui
  faut des garde-fous.

## Notes de conception

- **Sécurité au point d'usage** : les secrets (clés API) vivent dans `.env`,
  jamais dans le code ni dans l'historique Git.
- **Coût maîtrisé** : chaque brique documente ce qu'elle coûte réellement
  (tokens, appels). La mémoire, notamment, fait grandir le coût de chaque
  appel puisqu'on renvoie tout l'historique.
- **Garde-fous du service public** : messages limités à 2000 caractères ;
  10 appels par visiteur toutes les 5 minutes (réponse HTTP 429 au-delà) ;
  plafond de dépenses fixé dans la console Anthropic. La limitation des appels
  est gardée en mémoire : elle repart à zéro quand le service redémarre.
  À plus grande échelle, il faudrait un stockage partagé (Redis, par exemple).
- **Identité** : DIAP sait qui il est grâce au rôle `system`. Un LLM ne connaît
  que ce qu'on lui donne : le prompt système, l'historique et ses outils.

*(Fin de la saison 1 : les 7 briques sont posées. La saison 2 fera évoluer cette architecture.)*