# 🧱 DIAP — De zéro à Architecte IA

Construction d'un agent IA **brique par brique**, en public et en français.
Chaque capacité est ajoutée, comprise, puis expliquée dans la série vidéo
**« De zéro à Architecte IA »**.

> DIAP n'est pas une collection d'exercices : c'est **un seul agent qui grandit**.
> L'historique des commits raconte sa construction, capacité après capacité.

---

## 🎯 Objectif

Comprendre *pourquoi* avant *comment*. On ne branche pas une techno par mode :
à chaque étape, on part d'un **problème réel** de l'agent, et la brique qui le
résout devient une nouvelle capacité de DIAP.

## 🗺️ Roadmap — les 7 briques de DIAP

- [x] **LLM** — faire parler DIAP (premier appel à un modèle de langage)
- [x] **API** — donner des yeux à DIAP (accès au monde réel + function calling)
- [x] **Mémoire** — DIAP se souvient de la conversation
- [x] **Raisonnement** — DIAP décompose un problème avant de conclure
- [x] **Outils** — DIAP utilise plusieurs outils et choisit le bon
- [x] **Backend** — DIAP devient un vrai service
- [x] **Déploiement** — DIAP tourne en ligne, accessible à tous

✅ **Saison 1 terminée : les 7 briques sont posées.**

*(« Anatomie » est l'étape de compréhension initiale — pas une brique.)*

📎 **Quel code correspond à quelle vidéo ?** → [`docs/episodes.md`](docs/episodes.md)

---

## 🌐 Parler à DIAP en ligne

👉 **https://diap.onrender.com/chat**

- DIAP est hébergé sur Render (offre gratuite) : après un moment sans visite,
  le service **s'endort**. Le premier message peut donc mettre jusqu'à une
  minute à arriver, le temps qu'il se réveille. Les suivants sont rapides.
- Pour protéger le service, chaque visiteur est limité à **10 questions toutes
  les 5 minutes**, et à **2000 caractères** par message.

---

## 🚀 Démarrer

```bash
# 1. cloner puis entrer dans le dossier
git clone https://github.com/DIAPkuik237/diap.git
cd diap

# 2. créer et activer l'environnement virtuel
python -m venv venv
# Windows :
venv\Scripts\activate
# macOS / Linux :
source venv/bin/activate

# 3. installer les dépendances
pip install -r requirements.txt

# 4. configurer sa clé API
#    copier .env.example en .env, puis y mettre sa vraie clé Anthropic

# 5. lancer DIAP comme un service (brique Backend)
uvicorn diap.diap_api:app --reload
#    puis ouvrir http://127.0.0.1:8000/chat  (la page de discussion)
#    ou          http://127.0.0.1:8000/docs  (la documentation de l'API)
```

### Déployer sa propre copie (brique Déploiement)

Réglages utilisés sur Render (*Web Service* relié à ce dépôt GitHub) :

| Réglage | Valeur |
|---------|--------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn diap.diap_api:app --host 0.0.0.0 --port $PORT` |
| Variable d'environnement | `ANTHROPIC_API_KEY` = ta clé (saisie dans Render, jamais dans le code) |

- `--host 0.0.0.0` : le serveur accepte les connexions venant de l'extérieur,
  pas seulement de ta propre machine.
- `--port $PORT` : c'est l'hébergeur qui choisit le port, pas nous.
- Pense aussi à fixer une **limite de dépenses** dans la console Anthropic :
  un service public peut être appelé par n'importe qui.

⚠️ **Sécurité** : ta clé API va dans `.env` (ignoré par Git). Ne la mets
**jamais** dans le code ni dans un fichier versionné.

---

## 📂 Structure

```
diap/
├── diap/                     # le code de l'agent (grandit à chaque brique)
│   ├── premier_appel.py      # brique LLM  — DIAP parle
│   ├── meteo.py              # brique API  — appeler une API réelle
│   ├── diap_meteo.py         # brique API  — function calling : DIAP décide
│   ├── diap_memoire.py       # brique Mémoire — DIAP se souvient
│   ├── diap_raisonnement.py  # brique Raisonnement — décomposer avant de conclure
│   ├── diap_outils.py        # brique Outils — agir, avec human in the loop
│   └── diap_api.py           # briques Backend + Déploiement — le service en ligne (FastAPI, /chat)
├── docs/
│   ├── architecture.md       # schéma et notes d'architecture de DIAP
│   └── episodes.md           # correspondance épisodes ⇄ code
├── .env.example              # modèle de configuration (sans secrets)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📺 La série

- 🎥 **YouTube** — *De zéro à Architecte IA* : chaque épisode = une brique
  https://www.youtube.com/playlist?list=PLX1O_iVn_fzc
- 💻 **Ce dépôt** — le code réel derrière chaque démonstration

## ➡️ Et maintenant ?

La saison 1 a construit DIAP à la main, brique par brique, pour comprendre
chaque pièce. La **saison 2** confrontera ce DIAP aux outils du métier :
frameworks d'agents, MCP, systèmes multi-agents.

*Projet en construction publique. Le dépôt évolue au rythme de la série.*