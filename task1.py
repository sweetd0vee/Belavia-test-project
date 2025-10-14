import random
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union


class Generator:
    def __init__(self, default_num_lines: int = 100000):
        self.default_num_lines = default_num_lines
        self.latin_chars = 'abcdefghijklmnopqrstuvwxyz'
        self.russian_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def date(self, years_back: int = 5) -> str:
        """Генерирует случайную дату за указанное количество лет"""
        end_date = datetime.now()
        start_date = end_date - relativedelta(years=years_back)

        total_seconds = int((end_date - start_date).total_seconds())
        random_seconds = random.randint(0, total_seconds)
        random_date = start_date + timedelta(seconds=random_seconds)

        return random_date.strftime("%d.%m.%Y")

    def latin_string(self, min_length: int = 5, max_length: int = 15) -> str:
        """Генерирует случайную строку из латинских символов"""
        length = random.randint(min_length, max_length)
        return ''.join(random.choices(self.latin_chars, k=length))

    def russian_string(self, min_length: int = 5, max_length: int = 15) -> str:
        """Генерирует случайную строку из русских символов"""
        length = random.randint(min_length, max_length)
        return ''.join(random.choices(self.russian_chars, k=length))

    def even_integer(self, min_val: int = 1, max_val: int = 100000000) -> int:
        """Генерирует случайное четное целое число в указанном диапазоне"""
        even_min = min_val if min_val % 2 == 0 else min_val + 1
        even_max = max_val if max_val % 2 == 0 else max_val - 1

        if even_min > even_max:
            raise ValueError("Невозможно сгенерировать четное число в заданном диапазоне")

        return random.randrange(even_min, even_max + 1, 2)

    def float_number(self, min_val: float = 1.0, max_val: float = 20.0,
                     decimals: int = 8) -> float:
        """Генерирует случайное число с плавающей точкой"""
        return round(random.uniform(min_val, max_val), decimals)

    def generate_line(self, sep='||') -> str:
        """Генерирует одну строку данных"""
        date = self.date()
        latin = self.latin_string()
        russian = self.russian_string()
        even_int = self.even_integer()
        float_num = self.float_number()

        return f"{date}{sep}{latin}{sep}{russian}{sep}{even_int}{sep}{float_num:.8f}\n"

    def file(self, filename: str, num_lines: int = None,
             show_progress: bool = True) -> None:
        """Генерирует файл с заданным количеством строк"""
        if num_lines is None:
            num_lines = self.default_num_lines

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.',
                    exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(num_lines):
                if show_progress and i % 10000 == 0 and i > 0:
                    print(f"Генерация {filename}: {i}/{num_lines} строк")

                line = self.generate_line()
                f.write(line)

        if show_progress:
            print(f"Файл {filename} успешно создан с {num_lines} строками")

    def multiple_files(self, filenames: list, num_lines: Union[int, list] = None) -> None:
        """Генерирует несколько файлов"""
        if isinstance(num_lines, int):
            num_lines = [num_lines] * len(filenames)
        elif num_lines is None:
            num_lines = [self.default_num_lines] * len(filenames)

        for filename, lines in zip(filenames, num_lines):
            self.file(filename, lines)


def main():
    # Создание генератора
    gen = Generator()

    # Генерация одного файла
    gen.file("test_data.txt", num_lines=1000)

    # Генерация нескольких файлов
    gen.multiple_files(
        ["file1.txt", "file2.txt", "file3.txt"],
        num_lines=[100, 500, 1000]
    )

    # Генерация одной строки для тестирования
    test_line = gen.generate_line()
    print("Пример строки:", test_line.strip())


if __name__ == "__main__":
    main()
