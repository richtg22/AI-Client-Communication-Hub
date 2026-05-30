import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_summary(raw_update: str):
    prompt = f"""
You are an AI assistant for software delivery teams.

Convert this technical project update into structured client-ready communication.

Technical update:
{raw_update}

Return the answer exactly in this format:

SUMMARY:
<client friendly summary>

RISKS:
<risks and blockers>

NEXT_STEPS:
<recommended next steps>

EMAIL:
<professional client email draft>
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    return {
        "summary": extract_section(content, "SUMMARY:", "RISKS:"),
        "risks": extract_section(content, "RISKS:", "NEXT_STEPS:"),
        "next_steps": extract_section(content, "NEXT_STEPS:", "EMAIL:"),
        "email_draft": content.split("EMAIL:")[-1].strip()
    }


def extract_section(text: str, start: str, end: str):
    try:
        return text.split(start)[1].split(end)[0].strip()
    except IndexError:
        return ""