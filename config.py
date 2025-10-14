import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    DEFAULT_LINES: int = 100000
    LATIN_LENGTH: int = 10
    RUSSIAN_LENGTH: int = 10
    LATIN_CHARS: str = "abcdefghijklmnopqrstuvwxyz"
    RUSSIAN_CHARS: str = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    MIN_INT: int = 1
    MAX_INT: int = 100000000
    MIN_FLOAT: float = 1.0
    MAX_FLOAT: float = 20.0
    FLOAT_DECIMALS: int = 8
    YEARS_BACK: int = 5
    OUTPUT_DIR: str = "generated_files/"
    DELIMITER: str = "||"
