import json
import os

import yaml
from fastapi import FastAPI


def save_openapi_schema(app: FastAPI, output_path: str = "openapi.json") -> None:
    schema = app.openapi()
    abs_path = os.path.abspath(output_path)
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    print(f"✅ OpenAPI schema saved to: {abs_path}")


def save_openapi_schema_yaml(app: FastAPI, output_path: str = "openapi.yaml") -> None:
    schema = app.openapi()
    abs_path = os.path.abspath(output_path)
    with open(abs_path, "w", encoding="utf-8") as f:
        yaml.dump(schema, f, allow_unicode=True, sort_keys=False)
    print(f"✅ OpenAPI schema saved to: {abs_path}")
