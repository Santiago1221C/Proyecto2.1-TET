FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/
COPY app.py /app/

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

EXPOSE 8084

CMD ["app:app", "python", "app.py"]