#!/bin/sh
set -e

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
until python -c "
import socket, os, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((os.environ['DB_HOST'], int(os.environ['DB_PORT'])))
    s.close()
except OSError:
    sys.exit(1)
"; do
  sleep 1
done
echo "PostgreSQL is up."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn run:app --host 0.0.0.0 --port 8000
