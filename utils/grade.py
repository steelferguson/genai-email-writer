from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def grade_email_content(email_text, style_text, reviewer_feedback=None):
    prompt = f"""
You are an expert copywriter and branding strategist. Grade the following email for how well it follows the style guide.

STYLE GUIDE:
{style_text}

EMAIL:
{email_text}
"""

    if reviewer_feedback:
        prompt += f"\n\nAdditional reviewer feedback to consider:\n{reviewer_feedback}"

    prompt += "\n\nReturn a grade out of 10 and actionable feedback in a chart form showing which areas are strong and which could be improved"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional copywriter and branding expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
