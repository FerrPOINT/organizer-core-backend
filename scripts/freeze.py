import subprocess
import sys
from pathlib import Path

from loguru import logger


def freeze_requirements():
    logger.info("[⚙️] Обновляю файл зависимостей requirements.txt...")
    requirements_path = Path(__file__).parent.parent / "requirements.txt"

    with requirements_path.open("w") as req_file:
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=req_file)

    logger.info(f"[✅] Файл requirements.txt успешно обновлён: {requirements_path.resolve()}")


if __name__ == "__main__":
    freeze_requirements()
