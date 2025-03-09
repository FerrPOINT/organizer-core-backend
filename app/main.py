from fastapi import FastAPI

app = FastAPI(title="Organizer Core API")

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Organizer Core API!"}
