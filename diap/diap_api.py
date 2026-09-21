"""Mission 6 — Le corps de DIAP : un backend qui ne s'arrête jamais."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── on crée l'application (le "corps" de DIAP) ──
app = FastAPI(title="DIAP", description="Agent IA — De zéro à Architecte IA")


# ── la forme des données qu'on attend ──
class Question(BaseModel):
    message: str


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