# app.py
import streamlit as st
from Load_Document import load_documents
from Type_Detection import file_type_detector
from Model_File import create_model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain

import os
import tempfile
import json

st.set_page_config(page_title="📚 Chat with Document", layout="wide")
st.title("📚 Chat with Your Document or Link")

uploaded_file = st.file_uploader("Upload a file", type=["pdf", "csv", "xlsx", "txt"])
link_input = st.text_input("Or paste a link to a webpage")

if uploaded_file or link_input:
    if uploaded_file:
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name
        file_type = file_type_detector(uploaded_file.name)
    else:
        file_path = link_input.strip()
        file_type = file_type_detector(file_path)

    st.success(f"Detected file type: {file_type}")
    with st.spinner("Loading and processing document..."):
        docs = load_documents(file_type, file_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)

        embedding_model = OllamaEmbeddings(model="llama3.1:8b")
        vectorstore = FAISS.from_documents(splits, embedding_model)

        # Enhanced Prompt
        prompt_template = PromptTemplate.from_template(
            """You are an intelligent assistant that answers user questions using the given context.
Always try to understand the intent and provide informative, complete, and concise answers.

If the question is too vague (like "What is this about?"), try to infer the main topic or summarize the content based on the context.

Context:
{context}

Question:
{question}

Answer:"""
        )

        llm = create_model()
        combine_docs_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt_template)

        question_gen_prompt = PromptTemplate.from_template(
            "Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.\n\n"
            "Chat History:\n{chat_history}\nFollow Up Input: {question}\nStandalone question:"
        )
        question_generator = LLMChain(llm=llm, prompt=question_gen_prompt)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        qa_chain = ConversationalRetrievalChain(
            retriever=vectorstore.as_retriever(),
            combine_docs_chain=combine_docs_chain,
            question_generator=question_generator,
            memory=memory
        )

    st.subheader("Start Chatting")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.chat_input("Ask a question about the document...")
    if user_query:
        response = qa_chain.invoke({"question": user_query})
        answer = response["answer"]
        st.session_state.chat_history.append((user_query, answer))

    for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
        st.chat_message("user", avatar="🧑‍💻").write(user_msg)
        st.chat_message("assistant", avatar="🤖").write(ai_msg)

    # Download conversation as JSON
    if st.session_state.chat_history:
        conversation_data = [{"user": u, "assistant": a} for u, a in st.session_state.chat_history]
        json_data = json.dumps(conversation_data, indent=2)
        st.download_button(
            label="💾 Download Conversation",
            data=json_data,
            file_name="chat_conversation.json",
            mime="application/json"
        )
