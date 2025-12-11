# Cover Letter FastAPI Service

This service exposes the existing LangGraph-based cover-letter workflow through a FastAPI HTTP interface.

## Quick start

1. Install dependencies (example with pip):  
   `pip install fastapi uvicorn python-dotenv requests beautifulsoup4 llama-parse groq`.
2. Set the required environment variables:  
   - `IO_CHAT_URL`, `BEARER_API_KEY`, `LLM_MODEL_NAME` (optional) for `custom_llm.py`.  
   - `LLAMA_API_KEY` for PDF parsing.  
   - `UVICORN_HOST`, `UVICORN_PORT`, `UVICORN_RELOAD` (optional overrides).
3. Launch the API:  
   `python main.py` (runs `uvicorn app.main:app --reload` with the configured host/port).

## Streamlit front-end

1. Install Streamlit (same env): `pip install streamlit`.
2. Ensure backend is running on `http://localhost:8000` or set `COVER_LETTER_API_URL`.
3. Start UI: `streamlit run streamlit_app.py`.

## API

- `GET /health` – basic health probe.
- `POST /generate-cover-letter` – generate cover letter by given url vacancy and file resume:

