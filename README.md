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
- [ ] **API** — donner des yeux à DIAP (accès au monde réel + function calling)
- [ ] **Mémoire** — DIAP se souvient de la conversation
- [ ] **Raisonnement** — DIAP décompose un problème avant d'agir
- [ ] **Outils** — DIAP utilise plusieurs outils et choisit le bon
- [ ] **Backend** — DIAP devient un vrai service
- [ ] **Déploiement** — DIAP tourne en ligne

*(« Anatomie » est l'étape de compréhension initiale — pas une brique.)*

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
├── diap/                 # le code de l'agent (grandit à chaque brique)
│   └── premier_appel.py  # brique LLM : premier appel à un modèle
├── docs/
│   └── architecture.md   # schéma et notes d'architecture de DIAP
├── .env.example          # modèle de configuration (sans secrets)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📺 La série

- 🎥 **YouTube** — *De zéro à Architecte IA* : chaque épisode = une brique
- 💻 **Ce dépôt** — le code réel derrière chaque démonstration

*Projet en construction publique. Le dépôt évolue au rythme de la série.*
