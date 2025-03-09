import subprocess

print("🔄 Обновление зависимостей...")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

print("🚀 Запуск FastAPI...")
subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], check=True)
