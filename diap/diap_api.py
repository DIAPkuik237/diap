"""Mission 6 & 7 — Le corps de DIAP : un backend qui ne s'arrête jamais."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

# garde-fou simple : on refuse les messages démesurés (protection du budget)
LONGUEUR_MAX = 2000


# ── PREMIÈRE URL : vérifier que DIAP est vivant ──
@app.get("/")
def accueil():
    return {"agent": "DIAP", "statut": "en ligne"}


# ── DEUXIÈME URL : parler à DIAP ──
@app.post("/demander")
def demander(question: Question):
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
  .pupille{fill:#2563eb;transform-origin:center;
           animation:regarder 2.6s ease-in-out infinite;}
  #yeux{animation:cligner 3.4s ease-in-out infinite;transform-origin:center;}
  @keyframes regarder{
    0%,14%   {transform:translateX(0)     translateY(0);}
    22%,36%  {transform:translateX(-13px) translateY(2px);}
    44%,58%  {transform:translateX(13px)  translateY(2px);}
    66%,78%  {transform:translateX(0)     translateY(-7px);}
    86%,100% {transform:translateX(0)     translateY(0);}
  }
  @keyframes cligner{
    0%,92%,100%{transform:scaleY(1);}
    95%        {transform:scaleY(.08);}
  }
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
let minuteur = null;

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
}

function arreterPenseur(){
  clearInterval(minuteur);
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