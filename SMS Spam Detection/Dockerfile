FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp \
    NLTK_DATA=/usr/local/share/nltk_data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -c "import nltk; resources = ('punkt', 'punkt_tab', 'stopwords'); assert all(nltk.download(resource, download_dir='/usr/local/share/nltk_data', quiet=True) for resource in resources)"

COPY --chown=10001:10001 streamlit_app.py model.pkl vectorizer.pkl ./

EXPOSE 8501

USER 10001:10001

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501", "--browser.gatherUsageStats=false"]
