FROM python:3.12.6-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY src/ ./src/
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt



CMD ["python", "src/main.py"]
