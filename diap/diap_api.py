"""Mission 6 & 7 — Le corps de DIAP : un backend qui ne s'arrête jamais."""
import os
import time
from collections import defaultdict, deque

from dotenv import load_dotenv
from anthropic import Anthropic
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── on crée l'application (le "corps" de DIAP) ──
app = FastAPI(title="DIAP", description="Agent IA — De zéro à Architecte IA")


# ── la forme des données qu'on attend ──
class Question(BaseModel):
    message: str


# ── l'IDENTITÉ de DIAP (le rôle system, vu à l'épisode 5) ──
SYSTEME_DIAP = (
    "Tu es DIAP, un agent IA construit brique par brique par diapkuik "
    "dans la série « De zéro à Architecte IA ». "
    "DIAP signifie : Démystifier L'Intelligence Artificielle et la "
    "Programmation — pour tous. La chaîne diapkuik enseigne l'IA en la "
    "construisant réellement, étape par étape : parler, voir, mémoriser, "
    "raisonner, utiliser des outils, agir dans le monde réel. "
    "Tu réponds en français, de manière claire et pédagogique. "
    "Tu expliques toujours le POURQUOI avant le COMMENT. "
    "Réponds en texte simple, sans Markdown : pas d'astérisques, "
    "pas de dièses, pas de mise en forme. "
    "Si on te demande explicitement quel modèle te fait fonctionner, "
    "réponds honnêtement que tu es propulsé par Claude (Anthropic), "
    "mais que DIAP est l'agent construit autour."
)

# garde-fou 1 : on refuse les messages démesurés (protection du budget)
LONGUEUR_MAX = 2000

# ── garde-fou 2 : LIMITATION DU NOMBRE D'APPELS (rate limiting) ──
# On mémorise, pour chaque visiteur, l'heure de ses derniers appels.
# Si le quota est dépassé, on refuse AVANT d'appeler l'API : 0 token consommé.
APPELS_MAX = 10          # nombre d'appels autorisés…
FENETRE_SECONDES = 300   # …sur cette durée (ici : 10 appels / 5 minutes)

_historique = defaultdict(deque)   # {adresse_ip: [horodatages]}


def identifier_visiteur(request: Request) -> str:
    """L'IP du visiteur. Derrière un hébergeur, la vraie IP est dans
    l'en-tête X-Forwarded-For (sinon on ne verrait que celle du proxy)."""
    transmis = request.headers.get("x-forwarded-for")
    if transmis:
        return transmis.split(",")[0].strip()
    return request.client.host if request.client else "inconnu"


def quota_depasse(visiteur: str) -> bool:
    """Fenêtre glissante : on oublie les appels trop anciens, on compte le reste."""
    maintenant = time.time()
    appels = _historique[visiteur]
    while appels and maintenant - appels[0] > FENETRE_SECONDES:
        appels.popleft()
    if len(appels) >= APPELS_MAX:
        return True
    appels.append(maintenant)
    return False


# ── PREMIÈRE URL : vérifier que DIAP est vivant ──
@app.get("/")
def accueil():
    return {"agent": "DIAP", "statut": "en ligne"}


# ── DEUXIÈME URL : parler à DIAP ──
@app.post("/demander")
def demander(question: Question, request: Request):
    # le garde-fou passe AVANT tout appel au modèle
    visiteur = identifier_visiteur(request)
    if quota_depasse(visiteur):
        return JSONResponse(
            status_code=429,          # 429 = Too Many Requests
            content={
                "question": "",
                "reponse": ("Tu vas un peu vite pour moi. "
                            f"Maximum {APPELS_MAX} questions toutes les "
                            f"{FENETRE_SECONDES // 60} minutes. Reviens dans un instant."),
                "tokens": {"entres": 0, "sortis": 0},
            },
        )

    texte = question.message.strip()
    if not texte:
        return {"question": "", "reponse": "Pose-moi une question.",
                "tokens": {"entres": 0, "sortis": 0}}
    if len(texte) > LONGUEUR_MAX:
        return {"question": texte[:80] + "...",
                "reponse": f"Message trop long (max {LONGUEUR_MAX} caracteres).",
                "tokens": {"entres": 0, "sortis": 0}}

    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEME_DIAP,          # ← l'identité de DIAP
        messages=[{"role": "user", "content": texte}],
    )
    return {
        "question": texte,
        "reponse": reponse.content[0].text,
        "tokens": {
            "entres": reponse.usage.input_tokens,
            "sortis": reponse.usage.output_tokens,
        },
    }


# ── TROISIÈME URL : la page publique, pour tout le monde ──
@app.get("/chat", response_class=HTMLResponse)
def page_chat():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DIAP</title>
<style>
  :root{
    --bg:#0e1116; --panneau:#161b24; --bord:#2a3240;
    --texte:#e8e8e8; --gris:#8a93a6; --bleu:#4da6ff; --vert:#2ecc71;
  }
  *{box-sizing:border-box;}
  body{background:var(--bg);color:var(--texte);
       font-family:system-ui,-apple-system,sans-serif;
       max-width:640px;margin:0 auto;padding:32px 20px 60px;}
  h1{color:var(--bleu);font-size:2.4rem;margin:0;letter-spacing:.02em;}
  .sub{color:var(--gris);margin:6px 0 28px;font-size:.95rem;}
  textarea{width:100%;background:var(--panneau);color:var(--texte);
           border:1px solid var(--bord);border-radius:10px;padding:14px;
           font-size:1rem;min-height:90px;font-family:inherit;resize:vertical;}
  textarea:focus{outline:none;border-color:var(--bleu);}
  button{margin-top:12px;background:var(--bleu);color:var(--bg);border:0;
         border-radius:10px;padding:12px 22px;font-size:1rem;font-weight:700;
         cursor:pointer;}
  button:disabled{opacity:.45;cursor:wait;}

  /* ── LES YEUX DE DIAP : etat de chargement ── */
  #penseur{display:none;align-items:center;gap:14px;margin-top:26px;
           padding:16px;background:var(--panneau);border-radius:10px;
           border-left:3px solid var(--bleu);}
  #penseur.actif{display:flex;}
  .oeil{fill:#fff;}
  /* Pas d'animation en boucle : tout est piloté en JS, au hasard,
     pour que le regard ne soit jamais deux fois identique. */
  .pupille{fill:#2563eb;transform-origin:center;
           transition:transform .28s cubic-bezier(.34,1.3,.64,1);}
  #yeux{transform-origin:center;transition:transform .09s ease-in-out;}
  #yeux.ferme{transform:scaleY(.08);}
  #etat{color:var(--gris);font-size:.95rem;}

  #rep{margin-top:26px;background:var(--panneau);border-left:3px solid var(--vert);
       border-radius:8px;padding:16px;white-space:pre-wrap;line-height:1.55;}
  #rep:empty{display:none;}
  .note{color:#6b7488;font-size:.85rem;margin-top:22px;line-height:1.5;}
</style>
</head>
<body>
  <h1>DIAP</h1>
  <div class="sub">Agent IA construit brique par brique &mdash; diapkuik</div>

  <textarea id="q" placeholder="Pose ta question a DIAP..."></textarea>
  <button id="btn" onclick="envoyer()">Envoyer</button>

  <!-- les yeux de DIAP pendant qu'il travaille -->
  <div id="penseur">
    <svg id="yeux" width="74" height="40" viewBox="0 0 200 100" aria-hidden="true">
      <ellipse class="oeil"    cx="58"  cy="50" rx="42" ry="30"/>
      <ellipse class="oeil"    cx="142" cy="50" rx="42" ry="30"/>
      <ellipse class="pupille" cx="58"  cy="50" rx="13" ry="17"/>
      <ellipse class="pupille" cx="142" cy="50" rx="13" ry="17"/>
    </svg>
    <span id="etat">DIAP observe...</span>
  </div>

  <div id="rep"></div>

  <div class="note">Le premier message peut prendre jusqu'a une minute :
    le service se reveille.</div>

<script>
const ETATS = ["DIAP observe...", "DIAP reflechit...",
               "DIAP formule sa reponse..."];
let minuteur = null, timerRegard = null, timerClin = null;

function hasard(min, max){ return min + Math.random() * (max - min); }

/* ── LE REGARD : une nouvelle direction, a intervalles irreguliers ── */
function prochainRegard(){
  const pupilles = document.querySelectorAll('.pupille');
  // parfois il fixe droit devant, parfois il regarde ailleurs
  let dx = 0, dy = 0;
  if (Math.random() > 0.28) {
    dx = hasard(-14, 14);
    dy = hasard(-7, 6);
  }
  pupilles.forEach(function(p){
    p.style.transform = 'translate(' + dx.toFixed(1) + 'px,' +
                                       dy.toFixed(1) + 'px)';
  });
  // il tient ce regard entre 0,6 s et 2,8 s : jamais la meme duree
  timerRegard = setTimeout(prochainRegard, hasard(600, 2800));
}

/* ── LE CLIGNEMENT : parfois simple, parfois double ── */
function clignerUneFois(apres){
  const yeux = document.getElementById('yeux');
  yeux.classList.add('ferme');
  setTimeout(function(){
    yeux.classList.remove('ferme');
    if (apres) setTimeout(apres, 110);
  }, 95);
}

function prochainClin(){
  const double = Math.random() < 0.22;   // ~1 fois sur 5 : double clignement
  clignerUneFois(double ? function(){ clignerUneFois(null); } : null);
  // intervalle irregulier, comme un vrai oeil
  timerClin = setTimeout(prochainClin, hasard(1800, 5200));
}

function demarrerPenseur(){
  const p = document.getElementById('penseur');
  const e = document.getElementById('etat');
  let i = 0;
  e.textContent = ETATS[0];
  p.classList.add('actif');
  minuteur = setInterval(function(){
    i = Math.min(i + 1, ETATS.length - 1);
    e.textContent = ETATS[i];
  }, 3500);
  prochainRegard();
  timerClin = setTimeout(prochainClin, hasard(700, 2000));
}

function arreterPenseur(){
  clearInterval(minuteur);
  clearTimeout(timerRegard);
  clearTimeout(timerClin);
  const yeux = document.getElementById('yeux');
  if (yeux) yeux.classList.remove('ferme');
  document.querySelectorAll('.pupille').forEach(function(p){
    p.style.transform = 'translate(0,0)';
  });
  document.getElementById('penseur').classList.remove('actif');
}

async function envoyer(){
  const q = document.getElementById('q').value.trim();
  if(!q) return;
  const rep = document.getElementById('rep');
  const btn = document.getElementById('btn');
  btn.disabled = true;
  rep.textContent = "";
  demarrerPenseur();
  try{
    const r = await fetch('/demander', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: q})
    });
    const data = await r.json();
    rep.textContent = data.reponse || ("Erreur : " + JSON.stringify(data));
  }catch(e){
    rep.textContent = "Erreur : " + e;
  }finally{
    arreterPenseur();
    btn.disabled = false;
  }
}

document.getElementById('q').addEventListener('keydown', function(e){
  if(e.key === 'Enter' && (e.ctrlKey || e.metaKey)) envoyer();
});
</script>
</body>
</html>
"""