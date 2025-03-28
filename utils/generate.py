import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_email_content(prompt, style_text):
    system_prompt = f"""You are an expert copywriter for a climbing gym. You follow the brand voice and style guide below:

{style_text}

Now generate an email based on this instruction: {prompt}
Return both plain text copy and HTML structure."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # quick fallback if no GPT-4 access yet
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )

    content = response.choices[0].message.content

    # Just return plain content and dummy HTML for now
    return content, "<html><body><p>[HTML version of email here]</p></body></html>"