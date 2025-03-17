from fastapi import FastAPI

app = FastAPI()  # Το όνομα "app" πρέπει να ταιριάζει με την εντολή uvicorn main:app

@app.get("/")
def read_root():
    return {"message": "Hello World"}
