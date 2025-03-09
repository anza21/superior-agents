from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "env_check": str(os.getenv("DEEPSEEK_API_KEY") is not None)
    }
