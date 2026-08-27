from fastapi import FastAPI, WebSocket
import os

# Use Render's PORT env var (defaults to 8000 locally)
PORT = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=False)
