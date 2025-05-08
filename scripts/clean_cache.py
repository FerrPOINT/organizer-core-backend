import shutil
from pathlib import Path

from loguru import logger


def clean_pycache(path="."):
    root = Path(path)
    removed = 0
    for cache_dir in root.rglob('__pycache__'):
        shutil.rmtree(cache_dir)
        removed += 1
        logger.info(f"[-] Удалено: {cache_dir}")

    logger.info(f"[✅] Всего удалено директорий __pycache__: {removed}")


if __name__ == "__main__":
    clean_pycache()
