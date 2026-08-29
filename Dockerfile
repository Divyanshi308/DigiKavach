# DigiKavach Backend - Dockerfile for reliable deployment
# Uses a fixed Python version and installs everything in one layer,
# avoiding Render's build-command / rootDir / Poetry issues entirely.

FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install (cached layer)
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole backend app
COPY backend/app ./app

# Copy run entrypoint at /app
COPY backend/run.py ./run.py

# Render provides PORT; default to 8000 for local
ENV PORT=8000

EXPOSE 8000

CMD ["python", "run.py"]
