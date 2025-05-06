import re

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


class EmailStr(str):
    """
    Пользовательский тип EmailStr с валидацией и поддержкой JSON Schema
    """

    @classmethod
    def validate(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not EMAIL_REGEX.fullmatch(value):
            raise ValueError("Invalid email format")
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "email",
            "pattern": EMAIL_REGEX.pattern,
            "examples": ["user@example.com"],
            "description": "Custom validated email address",
        }
