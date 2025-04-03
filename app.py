import streamlit as st
from utils.generate import generate_email_content, generate_email_sequence
from utils.grade import grade_email_content

st.set_page_config(page_title="GenAI Email Writer", layout="wide")
st.title("📧 GenAI Email Writer for Basin Climbing")

# --- Upload Style Guide ---
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

# --- Prompt Input ---
st.header("📨 Generate Email or Journey")
generate_sequence = st.checkbox("Generate a multi-email journey", value=False)
num_emails = st.selectbox("How many emails?", [2, 3, 4, 5], index=2) if generate_sequence else 1

user_prompt = st.text_area(
    "What should the email or journey accomplish?",
    placeholder="e.g. Encourage day pass visitors to buy a membership."
)

# Session state for single email content
if "latest_email_text" not in st.session_state:
    st.session_state.latest_email_text = ""

# --- Generate Button ---
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
                    st.session_state.latest_email_text = email_text  # Save for grading/editing

                    st.subheader("🅰️ Email Copy")
                    st.write(email_text)

                    st.subheader("🅱️ HTML Structure")
                    st.code(email_html, language='html')

                    st.subheader("🖼️ Suggested Images")
                    st.markdown("- `hero_image_placeholder.jpg`")
                    st.markdown("- `climber_smiling_placeholder.jpg`")

        except Exception as e:
            st.error(f"❌ Error generating email: {e}")

# --- Email Editing and Grading ---
# Editable Email Input Before Grading
st.markdown("---")
st.subheader("✏️ Paste or Edit Email for Grading")

default_email = st.session_state.get("latest_email_text", "")
editable_email = st.text_area(
    "Edit or paste your email content here:", 
    value=default_email, 
    height=300,
    placeholder="Paste your email copy here for grading..."
)

# Feedback input
feedback_prompt = st.text_area("Optional: Add any reviewer feedback or context", placeholder="e.g. The phrase 'time is running out' sounds too gimmicky")

# Grade Button
if st.button("Grade This Email 🧠"):
    if not style_text:
        st.error("Please upload a style guide first.")
    elif not editable_email.strip():
        st.warning("Please enter or paste an email to grade.")
    else:
        try:
            with st.spinner("Grading..."):
                graded_feedback = grade_email_content(editable_email, style_text, feedback_prompt)
            st.markdown("### 🔍 Grade & Suggestions")
            st.write(graded_feedback)
        except Exception as e:
            st.error(f"❌ Error during grading: {e}")
            