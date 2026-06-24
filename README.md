# GenAI

This repository contains five small GenAI learning projects:

- `1_simple_llm_calling/`: a notebook that demonstrates a basic LLM call flow
- `2_health_analysis/`: a blood report analysis project with a notebook and a Streamlit app
- `3_vector_db/`: a notebook that introduces vector database basics
- `4_rag_basics/`: a notebook and source document for retrieval-augmented generation basics
- `5_simple_AI_agent/`: a notebook that explores a simple product query AI agent

## Project Structure

```text
.
|-- 1_simple_llm_calling/
|   `-- call_llm.ipynb
|-- 2_health_analysis/
|   |-- blood_work_analysis.ipynb
|   `-- streamlit_app/
|       `-- app.py
|-- 3_vector_db/
|   `-- vector_db_basics.ipynb
|-- 4_rag_basics/
|   |-- homo.pdf
|   `-- rag.ipynb
|-- 5_simple_AI_agent/
|   `-- Product_query_agent.ipynb
|-- main.py
|-- pyproject.toml
`-- uv.lock
```

## Requirements

- Python `3.13`
- A Google AI API key for Gemini access

## Setup

Create a virtual environment and install dependencies.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

If you use `uv`, you can also install from the locked project setup:

```powershell
uv sync
```

## Environment Variables

Create a `.env` file in the project root and add your API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run The Projects

### Simple LLM Calling

Open and run:

```text
1_simple_llm_calling/call_llm.ipynb
```

### Health Analysis Notebook

Open and run:

```text
2_health_analysis/blood_work_analysis.ipynb
```

### Health Analysis Streamlit App

Run:

```powershell
streamlit run 2_health_analysis/streamlit_app/app.py
```

The app:

- accepts a blood report as text or `.txt` upload
- extracts structured values from the report
- classifies markers as `HIGH`, `LOW`, or `NORMAL`
- generates a short health summary and Indian diet guidance

### Vector DB Basics

Open and run:

```text
3_vector_db/vector_db_basics.ipynb
```

This notebook introduces the core ideas behind vector embeddings, similarity search, and vector database workflows.

### RAG Basics

Open and run:

```text
4_rag_basics/rag.ipynb
```

This project uses the source document below while walking through retrieval-augmented generation basics:

```text
4_rag_basics/homo.pdf
```

### Simple AI Agent

Open and run:

```text
5_simple_AI_agent/Product_query_agent.ipynb
```

This notebook demonstrates a simple AI agent flow for handling product-related user queries.

## Notes

- `2_health_analysis/blood_work.txt` is intentionally ignored by Git so local sample medical text does not get committed.
- `.env` is also ignored and should never be pushed.
