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
    "Tu réponds en français, de manière claire et pédagogique. "
    "Tu expliques toujours le POURQUOI avant le COMMENT. "
    "Si on te demande explicitement quel modèle te fait fonctionner, "
    "réponds honnêtement que tu es propulsé par Claude (Anthropic), "
    "mais que DIAP est l'agent construit autour."
)


# ── PREMIÈRE URL : vérifier que DIAP est vivant ──
@app.get("/")
def accueil():
    return {"agent": "DIAP", "statut": "en ligne"}


# ── DEUXIÈME URL : parler à DIAP ──
@app.post("/demander")
def demander(question: Question):
    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEME_DIAP,          # ← l'identité de DIAP
        messages=[{"role": "user", "content": question.message}],
    )
    return {
        "question": question.message,
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
  body{background:#0e1116;color:#e8e8e8;font-family:system-ui,sans-serif;
       max-width:640px;margin:0 auto;padding:32px 20px;}
  h1{color:#4da6ff;font-size:2.4rem;margin:0;}
  .sub{color:#8a93a6;margin:6px 0 28px;}
  textarea{width:100%;background:#161b24;color:#e8e8e8;border:1px solid #2a3240;
           border-radius:10px;padding:14px;font-size:1rem;min-height:90px;
           box-sizing:border-box;}
  button{margin-top:12px;background:#4da6ff;color:#0e1116;border:0;
         border-radius:10px;padding:12px 22px;font-size:1rem;font-weight:700;
         cursor:pointer;}
  button:disabled{opacity:.5;cursor:wait;}
  #rep{margin-top:26px;background:#161b24;border-left:3px solid #2ecc71;
       border-radius:8px;padding:16px;white-space:pre-wrap;min-height:20px;}
  .note{color:#6b7488;font-size:.85rem;margin-top:22px;}
</style>
</head>
<body>
  <h1>DIAP</h1>
  <div class="sub">Agent IA construit brique par brique — diapkuik</div>
  <textarea id="q" placeholder="Pose ta question a DIAP..."></textarea>
  <button id="btn" onclick="envoyer()">Envoyer</button>
  <div id="rep"></div>
  <div class="note">Le premier message peut prendre jusqu'a une minute :
    le service se reveille.</div>
<script>
async function envoyer(){
  const q = document.getElementById('q').value.trim();
  if(!q) return;
  const rep = document.getElementById('rep');
  const btn = document.getElementById('btn');
  btn.disabled = true;
  rep.textContent = "DIAP reflechit...";
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
    btn.disabled = false;
  }
}
</script>
</body>
</html>
"""