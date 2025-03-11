from fastapi import FastAPI

from app.settings import user_settings  # Импортируем настройки

app = FastAPI(title="Organizer Core API")


@app.get("/")
def read_root():
    return {"message": f"Добро пожаловать в Organizer Core API! DB: {user_settings}"}
