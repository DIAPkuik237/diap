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
- [ ] **Outils** — DIAP utilise plusieurs outils et choisit le bon
- [ ] **Backend** — DIAP devient un vrai service
- [ ] **Déploiement** — DIAP tourne en ligne

*(« Anatomie » est l'étape de compréhension initiale — pas une brique.)*

📎 **Quel code correspond à quelle vidéo ?** → [`docs/episodes.md`](docs/episodes.md)

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
```

⚠️ **Sécurité** : ta clé API va dans `.env` (ignoré par Git). Ne la mets
**jamais** dans le code ni dans un fichier versionné.

---

## 📂 Structure

```
diap/
├── diap/                   # le code de l'agent (grandit à chaque brique)
│   ├── premier_appel.py    # brique LLM  — DIAP parle
│   ├── meteo.py            # brique API  — appeler une API réelle
│   ├── diap_meteo.py       # brique API  — function calling : DIAP décide
│   └── diap_memoire.py     # brique Mémoire — DIAP se souvient
├── docs/
│   ├── architecture.md     # schéma et notes d'architecture de DIAP
│   └── episodes.md         # correspondance épisodes ⇄ code
├── .env.example            # modèle de configuration (sans secrets)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📺 La série

- 🎥 **YouTube** — *De zéro à Architecte IA* : chaque épisode = une brique
  https://www.youtube.com/playlist?list=PLX1O_iVn_fzc
- 💻 **Ce dépôt** — le code réel derrière chaque démonstration

*Projet en construction publique. Le dépôt évolue au rythme de la série.*