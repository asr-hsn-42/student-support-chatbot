import streamlit as st
import chatbot.rag as rag
from pathlib import Path

st.set_page_config(
    page_title="Student Support Chatbot",
    page_icon="🎓",
    layout="wide"
)

@st.cache_resource
def load_rag():
    return rag.initialize_rag()

rag.store = load_rag()

st.title("🎓 AI Student Support Chatbot")
st.info(
    "👋 Welcome! Ask me anything about attendance, syllabus, "
    "academic calendar, examinations, or college FAQs."
)
st.caption("AI-powered Student Support using RAG + Gemini")

# ---------------- Sidebar ----------------

with st.sidebar:

    st.header("📚 Knowledge Base")

    pdfs = list(Path("data").glob("*.pdf"))

    for pdf in pdfs:
        st.success(pdf.name)

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.header("ℹ About")

st.write("""
This chatbot can answer questions related to:

• Academic Calendar

• FAQs

• Syllabus

It uses:

✅ Gemini AI

✅ Retrieval-Augmented Generation (RAG)

✅ FAISS Vector Search

✅ PDF Knowledge Base
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    avatar = "👨‍🎓" if message["role"] == "user" else "🎓"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask your question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message(
    "user",
    avatar="👨‍🎓"
):
        st.markdown(prompt)

    with st.chat_message(
    "assistant",
    avatar="🎓"
):
        with st.spinner("Searching documents and generating answer..."):
            try:

                answer, sources = rag.ask_rag(prompt)

                st.markdown(answer)

                st.info("📚 Source(s): " + ", ".join(sources))

                reply = answer + "\n\nSources: " + ", ".join(sources)

            except Exception:

                reply = "❌ Sorry, something went wrong."

                st.error(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

st.divider()

st.caption(
    "Built with ❤️ using Streamlit • Gemini • FAISS • Sentence Transformers"
)

if len(st.session_state.messages) == 0:

    st.markdown("### 💡 Try asking:")

    st.markdown("""
- What is SGPA?

- What is the attendance policy?

- When do exams begin?

- What are the subjects of Third Year?
""")