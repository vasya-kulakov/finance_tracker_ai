FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
COPY . /app

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000


ENTRYPOINT ["sh", "/app/entrypoint.sh"]
