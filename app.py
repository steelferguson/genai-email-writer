import streamlit as st
from utils.generate import generate_email_content  # ✅ Add this import

st.set_page_config(page_title="GenAI Email Writer", layout="wide")
st.title("📧 GenAI Email Writer for Basin Climbing")

# Upload style guide
st.sidebar.header("Upload Style Guide")
style_file = st.sidebar.file_uploader("Upload a style guide (.pdf or .docx)", type=["pdf", "docx"])

def extract_text(file):
    try:
        import fitz  # PyMuPDF
        from docx import Document

        if file.name.endswith(".pdf"):
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            return "\n".join([page.get_text() for page in pdf])
        elif file.name.endswith(".docx"):
            doc = Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            return None
    except Exception as e:
        return f"⚠️ Failed to extract text: {e}"

style_text = None
if style_file:
    style_text = extract_text(style_file)
    if style_text:
        st.sidebar.success("Style guide loaded!")
        st.sidebar.text_area("Extracted Style Guide", style_text, height=200)

# Prompt input
st.header("📨 Generate Email")
user_prompt = st.text_area("What do you want the email to say or accomplish?", placeholder="e.g. Write a referral email encouraging members to invite a friend.")

# Generate button
if st.button("Generate Email ✨"):
    if not style_text:
        st.error("Please upload a style guide first.")
    elif not user_prompt:
        st.warning("Please enter a prompt.")
    else:
        try:
            with st.spinner("Generating content using GPT-4..."):
                email_text, email_html = generate_email_content(user_prompt, style_text)

            st.success("Generation complete!")

            # Output
            st.subheader("🅰️ Email Copy")
            st.write(email_text)

            st.subheader("🅱️ HTML Structure")
            st.code(email_html, language='html')

            st.subheader("🖼️ Suggested Images")
            st.markdown("- `hero_image_placeholder.jpg`")
            st.markdown("- `climber_smiling_placeholder.jpg`")

        except Exception as e:
            st.error(f"❌ Error generating email: {e}")