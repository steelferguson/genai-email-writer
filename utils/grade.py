from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def grade_email_against_style(final_email_text, style_text):
    """
    Uses GPT to evaluate how well the final email aligns with the style guide.
    Returns a summary grade and feedback.
    """
    system_prompt = f"""You are a brand tone and voice expert. Based on the style guide below, score how well the final email adheres to the guide.
Return a grade from A+ to F, and offer specific feedback for improvements.

STYLE GUIDE:
{style_text}

FINAL EMAIL:
{final_email_text}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )

    return response.choices[0].message.content