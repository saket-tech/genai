from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


APP_DIR = Path(__file__).resolve().parent
HEALTH_DIR = APP_DIR.parent
DEFAULT_REPORT_PATH = HEALTH_DIR / "blood_work.txt"


def load_report_text(uploaded_file: Any | None) -> str:
	if uploaded_file is not None:
		return uploaded_file.getvalue().decode("utf-8")

	if DEFAULT_REPORT_PATH.exists():
		return DEFAULT_REPORT_PATH.read_text(encoding="utf-8")

	return ""


def get_message_text(response: Any) -> str:
	if hasattr(response, "content") and response.content is not None:
		return str(response.content)
	if hasattr(response, "text") and response.text is not None:
		return str(response.text)
	return str(response)


def extract_json_payload(raw_text: str) -> str:
	text = raw_text.strip()

	if text.startswith("```"):
		text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
		text = re.sub(r"\s*```$", "", text)

	json_start = min([index for index in [text.find("["), text.find("{")] if index != -1], default=-1)
	if json_start != -1:
		text = text[json_start:]

	return text.strip()


def parse_extracted_values(raw_text: str) -> list[dict[str, Any]]:
	payload = extract_json_payload(raw_text)

	try:
		data = json.loads(payload)
	except json.JSONDecodeError:
		return []

	if isinstance(data, dict):
		data = [data]

	if not isinstance(data, list):
		return []

	normalized: list[dict[str, Any]] = []
	for item in data:
		if isinstance(item, dict):
			normalized.append(
				{
					"Test Name": item.get("Test Name") or item.get("test_name") or item.get("name") or "",
					"Value": item.get("value") or item.get("Value") or "",
					"Status": item.get("Status") or item.get("status") or "",
					"Reference": item.get("Reference") or item.get("reference") or "",
				}
			)
		elif isinstance(item, str):
			normalized.append({"Test Name": item, "Value": "", "Status": "", "Reference": ""})

	return normalized


@st.cache_resource
def get_llm() -> ChatGoogleGenerativeAI:
	load_dotenv()
	return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def build_extraction_prompt(report_text: str) -> str:
	return f"""
You are a medical data extraction assistant.

From the blood report below, extract all test values and classify each one as HIGH, LOW or NORMAL
based on the reference ranges provided in the report.

Return ONLY valid JSON as an array of objects with these keys:
- Test Name
- Value
- Status
- Reference

Blood Report:
{report_text}
""".strip()


def build_diet_prompt(extracted_values_text: str) -> str:
	return f"""
You are a clinical nutritionist specialising in Indian dietary habits.

Based on the blood work analysis below, write:
1. A short health summary in 3 lines explaining the patient's condition in simple language.
2. A short, practical Indian diet plan with only two sections:
   (1) Foods to avoid
   (2) Foods to eat more of

Do not include any other sections in the diet plan.

Blood Work Analysis:
{extracted_values_text}
""".strip()


def main() -> None:
	st.set_page_config(page_title="Health Analysis", page_icon="🩺", layout="wide")

	st.title("Health Analysis Dashboard")
	st.caption("Upload a blood report or use the sample report to generate a structured summary and diet guidance.")

	with st.sidebar:
		st.header("Input")
		uploaded_file = st.file_uploader("Upload blood report text", type=["txt"])
		use_sample = st.toggle("Use bundled sample report", value=True)
		st.divider()
		st.write("The app uses Gemini via LangChain. Make sure your Google API key is available in the environment.")

	report_text = load_report_text(uploaded_file if uploaded_file is not None else (None if use_sample else None))
	if uploaded_file is None and not use_sample:
		report_text = ""

	if use_sample and uploaded_file is None and DEFAULT_REPORT_PATH.exists():
		report_text = DEFAULT_REPORT_PATH.read_text(encoding="utf-8")

	report_text = st.text_area("Blood report", value=report_text, height=360, placeholder="Paste a blood report here or upload a .txt file.")

	col1, col2 = st.columns([1, 1])
	with col1:
		run_analysis = st.button("Analyze report", type="primary", use_container_width=True)
	with col2:
		st.download_button(
			"Download report text",
			data=report_text,
			file_name="blood_report.txt",
			mime="text/plain",
			use_container_width=True,
			disabled=not bool(report_text.strip()),
		)

	if not report_text.strip():
		st.info("Provide a report to begin.")
		return

	st.subheader("Report Preview")
	st.text(report_text[:2000] if len(report_text) > 2000 else report_text)

	if not run_analysis:
		st.stop()

	llm = get_llm()

	with st.spinner("Extracting test values..."):
		extraction_prompt = build_extraction_prompt(report_text)
		extraction_response = llm.invoke(extraction_prompt)
		extracted_values_text = get_message_text(extraction_response)

	parsed_values = parse_extracted_values(extracted_values_text)

	st.subheader("Stage 1: Extracted Values")
	if parsed_values:
		st.dataframe(parsed_values, use_container_width=True, hide_index=True)
	else:
		st.warning("The model returned text that could not be parsed as JSON. Showing the raw output instead.")
		st.code(extracted_values_text, language="json")

	with st.spinner("Generating diet guidance..."):
		diet_prompt = build_diet_prompt(extracted_values_text)
		diet_response = llm.invoke(diet_prompt)
		diet_text = get_message_text(diet_response)

	st.subheader("Stage 2: Health Summary & Diet Plan")
	st.markdown(diet_text)


if __name__ == "__main__":
	main()
