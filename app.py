import streamlit as st
from utils.generate import generate_email_content, generate_email_sequence
from utils.grade import grade_email_content

st.set_page_config(page_title="GenAI Email Writer", layout="wide")
st.title("📧 GenAI Email Writer for Basin Climbing")

# Upload style guide
st.sidebar.header("Upload Style Guide")
style_file = st.sidebar.file_uploader("Upload a style guide (.pdf or .docx)", type=["pdf", "docx"])

def extract_text(file):
    try:
        import fitz
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

# State variables
if "email_text" not in st.session_state:
    st.session_state.email_text = ""
if "email_html" not in st.session_state:
    st.session_state.email_html = ""

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
                    journey = generate_email_sequence(user_prompt, style_text, num_emails=num_emails)
                    st.markdown("### ✉️ Multi-Email Journey")
                    st.write(journey)
                else:
                    email_text, email_html = generate_email_content(user_prompt, style_text)
                    st.session_state.email_text = email_text
                    st.session_state.email_html = email_html
        except Exception as e:
            st.error(f"❌ Error generating email: {e}")

# If an email has been generated, show it
if st.session_state.email_text:
    st.subheader("🅰️ Email Copy")
    st.write(st.session_state.email_text)

    st.subheader("🅱️ HTML Structure")
    st.code(st.session_state.email_html, language='html')

    st.subheader("🖼️ Suggested Images")
    st.markdown("- `hero_image_placeholder.jpg`")
    st.markdown("- `climber_smiling_placeholder.jpg`")

    # Feedback box & regenerate
    st.markdown("---")
    st.subheader("💬 Feedback & Iteration")
    feedback_prompt = st.text_area("Give feedback on this email content", placeholder="e.g. The phrase 'time is running out' feels too gimmicky.")

    if st.button("Regenerate Email With Feedback ♻️"):
        if not feedback_prompt:
            st.warning("Please enter feedback before regenerating.")
        else:
            try:
                with st.spinner("Regenerating email with feedback..."):
                    feedback_prompt_combined = user_prompt + f"\n\nAlso consider this feedback: {feedback_prompt}"
                    new_email_text, new_email_html = generate_email_content(feedback_prompt_combined, style_text)
                    st.session_state.email_text = new_email_text
                    st.session_state.email_html = new_email_html
            except Exception as e:
                st.error(f"❌ Error regenerating: {e}")

# Optional: grading section (if you still want it)
st.markdown("---")
st.subheader("📊 Grade Any Email")
editable_email = st.text_area("Paste email content here to evaluate against the style guide:", height=200)

if st.button("Grade This Email 🧠"):
    try:
        with st.spinner("Grading..."):
            feedback = grade_email_content(editable_email, style_text)
            st.markdown(f"**Feedback:**\n\n{feedback}")

    except Exception as e:
        st.error(f"❌ Error during grading: {e}")