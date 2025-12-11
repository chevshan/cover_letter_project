FROM python:3.11-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY requirements.lock .
RUN uv pip install --system --no-cache-dir -r requirements.lock
COPY streamlit_app.py .
EXPOSE 8501
ENV COVER_LETTER_API_URL=http://backend:8000

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]