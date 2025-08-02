# Chat with Your Document

A lightweight Streamlit application that allows you to **chat with any document** — PDF, TXT, CSV, Excel, or even a web page — using **Ollama’s LLaMA 3.1 (8B)** model and **LangChain** for intelligent retrieval and conversational memory.


## Features

- **Local LLM**: Uses the LLaMA 3.1 8B model via Ollama for fast, private, and offline inference.
- **Any Document Support**: Works with PDFs, CSVs, Excel files, TXT files, and even website links.
- **Context-aware QA**: Retains chat history using LangChain’s memory modules.
- **Simple Chat UI**: Clean and responsive chat interface built using Streamlit.
- **Chat Download**: Export your conversation history anytime.


## Tech Stack

- **[LangChain](https://www.langchain.com/)** – for retrieval, memory, and chain management  
- **[Ollama](https://ollama.com/)** – to serve the LLaMA 3.1 8B model locally  
- **[FAISS](https://github.com/facebookresearch/faiss)** – vector storage for efficient document retrieval  
- **[Streamlit](https://streamlit.io/)** – for the user-facing chat interface

---

## Installation or to start at your Local

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chat-with-your-document.git
cd chat-with-your-document
````

### Set up Python environment

```bash
conda create -n llm_env_conda python=3.10
conda activate llm_env_conda
pip install -r requirements.txt
```

### Install and Run Ollama

Make sure Ollama is installed and the LLaMA 3.1 model is pulled:

```bash
ollama run llama3:8b
```

> If you haven’t installed Ollama: [https://ollama.com/download](https://ollama.com/download)


## Running the App

```bash
streamlit run app.py
```

You’ll be able to:

* Upload documents or paste a link.
* Ask any question related to the content.
* Get accurate, context-based responses using your local LLM.

---

## Model Used

> **Model**: `llama3:8b` (Meta LLaMA 3.1)
> **Hosted via**: [Ollama](https://ollama.com/library/llama3)
> **Note**: The model runs entirely locally, ensuring privacy and low latency.

---


## Future Scopes

*  Add multi-file upload support
*  Support for chat reset
*  Option to switch models dynamically
*  Hugging Face integration for cloud inference
*  Deploying the model

---
```
