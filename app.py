import streamlit as st
from utils.generate import generate_email_content, generate_email_sequence
from utils.grade import grade_email_content  # For style grading

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
st.header("📨 Generate Email or Journey")
generate_sequence = st.checkbox("Generate a multi-email journey", value=False)
num_emails = st.selectbox("How many emails?", [2, 3, 4, 5], index=2) if generate_sequence else 1

user_prompt = st.text_area("What should the email or journey accomplish?", placeholder="e.g. Encourage day pass visitors to buy a membership.")

# Generate button
if st.button("Generate Email ✨"):
    if not style_text:
        st.error("Please upload a style guide first.")
    elif not user_prompt:
        st.warning("Please enter a prompt.")
    else:
        try:
            with st.spinner("Generating content using GPT-4..."):
                if generate_sequence:
                    email_output = generate_email_sequence(user_prompt, style_text, num_emails=num_emails)
                    st.markdown("### ✉️ Multi-Email Journey")
                    st.write(email_output)
                else:
                    email_text, email_html = generate_email_content(user_prompt, style_text)
                    st.subheader("🅰️ Email Copy")
                    st.write(email_text)

                    st.subheader("🅱️ HTML Structure")
                    st.code(email_html, language='html')

                    st.subheader("🖼️ Suggested Images")
                    st.markdown("- `hero_image_placeholder.jpg`")
                    st.markdown("- `climber_smiling_placeholder.jpg`")

                    st.markdown("---")
                    st.subheader("🧠 Style Guide Feedback")
                    feedback_prompt = st.text_area("Optional: Give feedback on the generated content", placeholder="e.g. The phrase 'time is running out' sounds too gimmicky")

                    if st.button("Grade Final Email ✏️"):
                        with st.spinner("Grading email against style guide..."):
                            graded_feedback = grade_email_content(email_text, style_text, feedback_prompt)
                            st.markdown("### 🔍 Grade & Suggestions")
                            st.write(graded_feedback)

        except Exception as e:
            st.error(f"❌ Error generating email: {e}")
