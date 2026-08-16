# 🏗️ Architecture de DIAP

Document vivant : il se densifie à chaque brique ajoutée.

## Vue d'ensemble

Un agent n'est pas un modèle : c'est une **architecture** autour d'un modèle.
DIAP orchestre plusieurs composants pour percevoir, se souvenir, raisonner et agir.

```
        Utilisateur
             |
             v
    +------------------+
    |   DIAP (agent)   |
    +------------------+
             |
     +-------+--------+---------+
     |       |        |         |
     v       v        v         v
    LLM   Mémoire  Raisonn.   Outils
                                 |
                                 v
                          APIs / monde réel
```

## État des briques

| Brique        | État        | Rôle                                              |
|---------------|-------------|---------------------------------------------------|
| LLM           | ✅ fait     | Comprendre et générer du langage                  |
| API           | ⬜ à venir  | Accéder au monde réel (function calling)          |
| Mémoire       | ⬜ à venir  | Se souvenir de la conversation                    |
| Raisonnement  | ⬜ à venir  | Décomposer un problème avant d'agir               |
| Outils        | ⬜ à venir  | Utiliser et choisir parmi plusieurs outils        |
| Backend       | ⬜ à venir  | Exposer DIAP comme un service                     |
| Déploiement   | ⬜ à venir  | Faire tourner DIAP en ligne                       |

## Notes de conception

- **Sécurité au point d'usage** : les secrets (clés API) vivent dans `.env`,
  jamais dans le code ni dans l'historique Git.
- **Coût maîtrisé** : chaque brique documente ce qu'elle coûte réellement
  (tokens, appels), pour garder l'agent économe.

*(Ce document s'étoffe à mesure que DIAP gagne des capacités.)*
