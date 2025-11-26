import json
import os
import tempfile
from pathlib import Path
from typing import Optional

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

API_URL = os.getenv("COVER_LETTER_API_URL", "http://localhost:8000")


def save_uploaded_pdf(uploaded_file) -> Optional[str]:
    if uploaded_file is None:
        return None

    temp_dir = Path(tempfile.gettempdir())
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(
        dir=temp_dir, suffix=".pdf", delete=False
    )
    temp_file.write(uploaded_file.read())
    temp_file.flush()
    temp_file.close()

    return temp_file.name


def call_backend(data: dict):
    response = requests.post(
        f"{API_URL}/generate-cover-letter",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    response.raise_for_status()
    return response.json()


def main():
    st.set_page_config(page_title="Cover Letter Generator", layout="wide")
    st.title("✉️ Cover Letter Generator")
    st.write("Download the resume (PDF only) and the link to the vacancy to receive a personalized cover letter.")

    with st.form("cover_letter_form"):
        vacancy_url = st.text_input("Link to the vacancy", value="")
        uploaded_pdf = st.file_uploader("Load the resume (PDF only)", type=["pdf"])
        submitted = st.form_submit_button("Generate")

    if submitted:
        if not vacancy_url:
            st.error("Specify the link to the vacancy.")
            return

        if not uploaded_pdf:
            st.error("Load the resume.")
            return

        resume_pdf_path = save_uploaded_pdf(uploaded_pdf)

        payload = {
            "vacancy_url": vacancy_url,
            "vacancy_text": None,
            "resume_pdf_path": resume_pdf_path,
            "resume_text": None,
            "save_cover_letter": False,
            "output_file": None,
        }

        with st.spinner("📨 Generating the cover letter..."):
            try:
                response = call_backend(payload)
            except requests.RequestException as exc:
                if resume_pdf_path:
                    try:
                        Path(resume_pdf_path).unlink(missing_ok=True)
                    except OSError:
                        pass
                st.error(f"Error calling the API: {exc}")
                return
            else:
                if resume_pdf_path:
                    try:
                        Path(resume_pdf_path).unlink(missing_ok=True)
                    except OSError:
                        st.warning("Don't able to remove the temporary resume file.")

        st.success("The cover letter is ready!")
        st.subheader("Result")
        st.text_area("The cover letter", response.get("cover_letter", ""), height=350)

        st.json(response.get("workflow_report", {}))


if __name__ == "__main__":
    main()