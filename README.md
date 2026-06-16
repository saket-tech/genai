# GenAI

This repository contains two small GenAI learning projects:

- `1_simple_llm_calling/`: a notebook that demonstrates a basic LLM call flow
- `2_health_analysis/`: a blood report analysis project with a notebook and a Streamlit app

## Project Structure

```text
.
|-- 1_simple_llm_calling/
|   `-- call_llm.ipynb
|-- 2_health_analysis/
|   |-- blood_work_analysis.ipynb
|   `-- streamlit_app/
|       `-- app.py
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

## Notes

- `2_health_analysis/blood_work.txt` is intentionally ignored by Git so local sample medical text does not get committed.
- `.env` is also ignored and should never be pushed.
