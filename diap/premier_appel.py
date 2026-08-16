"""Mission 1 — DIAP, premier souffle : faire répondre un LLM depuis mon code."""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()                                    # lit le fichier .env
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

reponse = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[
        {"role": "user",
         "content": "Explique-moi en 3 phrases ce qu'est un agent IA."}
    ],
)

print(reponse.content[0].text)
print("\n--- comptabilité ---")
print("tokens entrés  :", reponse.usage.input_tokens)
print("tokens sortis  :", reponse.usage.output_tokens)