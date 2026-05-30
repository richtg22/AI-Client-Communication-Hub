import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_summary(raw_update: str):
    prompt = f"""
You are an AI assistant for software delivery teams.

Convert this technical project update into:
1. Client-friendly summary
2. Risks/blockers
3. Next steps
4. Professional client email draft

Technical update:
{raw_update}

Return using these headings:
SUMMARY:
RISKS:
NEXT_STEPS:
EMAIL:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content