FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

EXPOSE 8084

CMD ["gunicorn", "--bind", "0.0.0.0:8084", "app:app"]