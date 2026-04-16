# 📚 Enterprise Knowledge Assistant (RAG)

## 🚀 Project Overview

This project is an AI-powered **Enterprise Knowledge Assistant** built using **Retrieval-Augmented Generation (RAG)**.

It allows users to upload multiple PDF documents and ask questions. The system retrieves relevant information and generates accurate answers using Google Gemini.

---

## 🧠 Key Features

* 📄 Multi-PDF Upload
* 🤖 RAG-based Question Answering
* 🔍 Semantic Search using FAISS
* 💬 Chat Interface (Streamlit)
* 📊 Document Summarization
* 📄 Source Citation (Page Numbers)
* 🔐 Secure API Key Handling

---

## 🏗️ Tech Stack

* Python
* Streamlit
* LangChain
* Google Gemini API
* FAISS Vector Database

---

## ⚙️ How It Works

1. Upload PDF documents
2. Text is split into chunks
3. Embeddings are created
4. Stored in FAISS vector database
5. User asks a question
6. Relevant chunks retrieved
7. Gemini generates answer

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 API Key Setup

Add your API key using Streamlit secrets:

```toml
GOOGLE_API_KEY = "your_api_key_here"
```

---

## 🌐 Deployment

This app is deployed using **Streamlit Community Cloud**.

---

## 🎯 Use Cases

* Enterprise knowledge search
* Document QA systems
* Research assistance
* Internal company assistants

---

## 👨‍💻 Author

Your Name

---
