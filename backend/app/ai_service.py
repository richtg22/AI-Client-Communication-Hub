import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_summary(raw_update: str):
    prompt = f"""
You are a senior project manager preparing client-facing communications.

Convert the following technical project update into professional business communication.

Project Update:
{raw_update}

Requirements:

- Summary: 3-5 detailed sentences
- Risks: Clearly identify blockers, dependencies, or risks. If none exist, explain why.
- Next Steps: Provide 3 actionable next steps
- Email Draft:
    - 2-3 well-structured paragraphs
    - Professional client-facing communication
    - Summarize project progress
    - Mention risks or blockers if applicable
    - Include next steps and expected actions
    - Use proper email formatting with line breaks
    - Start with "Dear Client,"
    - End with:

      Best regards,
      [Your Name]
- Email Draft Example:

  Dear Client,

  We are pleased to provide an update on the project. [Project progress summary].

  At this stage, [risks if applicable]. Our next steps include [next steps].

  Please let us know if you have any questions or require additional information.

  Best regards,
  [Your Name]

Return ONLY valid JSON:

{{
  "summary": "",
  "risks": "",
  "next_steps": "",
  "email_draft": ""
}}
"""
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You must respond with valid JSON only."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.3,
    response_format={"type": "json_object"}
)

    content = response.choices[0].message.content
    
    try:
        data = json.loads(content)
        
        return {
            "summary": data["summary"],
            "risks": data["risks"],
            "next_steps": data["next_steps"],
            "email_draft": data["email_draft"]
            }
    except json.JSONDecodeError:
        return {
            "summary": content,
            "risks": "Could not parse risks from AI response.",
            "next_steps": "Review the generated summary and refine manually if needed.",
            "email_draft": content
            }