FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

EXPOSE 5002

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5002/api/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "4", "--timeout", "120", "app:app"]
