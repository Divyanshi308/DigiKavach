#!/bin/bash
# Render.com start script for DigiKavach backend
cd /opt/render/project/src/backend
pip install -r requirements.txt --quiet
uvicorn app.main:app --host 0.0.0.0 --port $PORT
