import shutil
from pathlib import Path


def clean_pycache(path="."):
    root = Path(path)
    removed = 0
    for cache_dir in root.rglob('__pycache__'):
        shutil.rmtree(cache_dir)
        removed += 1
        print(f"[-] Удалено: {cache_dir}")

    print(f"[✅] Всего удалено директорий __pycache__: {removed}")


if __name__ == "__main__":
    clean_pycache()
