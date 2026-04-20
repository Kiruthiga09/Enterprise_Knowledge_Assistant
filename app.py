import streamlit as st
import os
from rag import process_pdf, create_rag_chain, get_answer, summarize_document

st.set_page_config(page_title="Enterprise Knowledge Assistant", layout="wide")

st.title("📚 Enterprise Knowledge Assistant")
st.caption("Chat with your documents using RAG")

------------------- API KEY -------------------
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
elif os.getenv("GOOGLE_API_KEY"):
    pass
else:
    os.environ["GOOGLE_API_KEY"] = "your api key here"

# ------------------- SESSION -------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "ready" not in st.session_state:
    st.session_state.ready = False

if "skipped_files" not in st.session_state:
    st.session_state.skipped_files = []


# ------------------- SIDEBAR -------------------
st.sidebar.header("📂 Upload PDFs")
pdf_files = st.sidebar.file_uploader("Upload", type="pdf", accept_multiple_files=True)

# 🔥 ADD: Select file (for correct retrieval)
selected_file = None
if pdf_files:
    selected_file = st.sidebar.selectbox(
        "📄 Select document to query",
        [pdf.name for pdf in pdf_files]
    )


# 🔥 RESET WHEN FILE REMOVED
if not pdf_files:
    st.session_state.ready = False
    st.session_state.chat = []
    st.session_state.vector_store = None
    st.session_state.rag_chain = None
    st.session_state.retriever = None
    st.session_state.skipped_files = []


# ------------------- PROCESS -------------------
if pdf_files and not st.session_state.ready:
    with st.spinner("Processing..."):
        try:
            paths = []

            for pdf in pdf_files:
                path = f"/tmp/{pdf.name}"
                with open(path, "wb") as f:
                    f.write(pdf.read())
                paths.append(path)

            # 🔥 process + get skipped files
            vector_store, skipped_files = process_pdf(paths)

            st.session_state.skipped_files = skipped_files

            rag_chain, retriever = create_rag_chain(vector_store)

            st.session_state.vector_store = vector_store
            st.session_state.rag_chain = rag_chain
            st.session_state.retriever = retriever
            st.session_state.ready = True

            st.sidebar.success("✅ Ready!")

        except ValueError as e:
            st.warning(str(e))

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")


# 🔥 ALWAYS SHOW WARNING
if st.session_state.skipped_files:
    st.warning(f"⚠️ Skipped large files (>50 pages): {', '.join(st.session_state.skipped_files)}")


# ------------------- BUTTONS -------------------
col1, col2 = st.sidebar.columns(2)

if col1.button("📊 Summary"):
    if st.session_state.ready:
        with st.spinner("Generating summary..."):
            summary = summarize_document(
                st.session_state.vector_store,
                selected_file   # 🔥 PASS SELECTED FILE
            )
            st.sidebar.write(summary)

if col2.button("🗑 Clear"):
    st.session_state.chat = []
    st.session_state.ready = False
    st.session_state.vector_store = None
    st.session_state.rag_chain = None
    st.session_state.retriever = None
    st.session_state.skipped_files = []


# ------------------- CHAT -------------------
query = st.chat_input("Ask question...")

if query:
    if not st.session_state.ready:
        st.warning("⚠️ Please upload and process a PDF first.")
    else:
        answer, sources = get_answer(
            st.session_state.rag_chain,
            st.session_state.retriever,
            query,
            selected_file   # 🔥 IMPORTANT FIX
        )

        st.session_state.chat.append((query, answer, sources))


# ------------------- DISPLAY -------------------
for q, a, s in st.session_state.chat:
    with st.chat_message("user"):
        st.write(q)

    with st.chat_message("assistant"):
        st.write(a)
        st.caption("📄 " + ", ".join(s))
