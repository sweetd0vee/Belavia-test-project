import os
import random
from datetime import datetime, timedelta
from typing import Union

from dateutil.relativedelta import relativedelta

from base_logger import logger
from config import Config

constants = Config()


class Generator:
    def __init__(self, default_num_lines: int = constants.DEFAULT_LINES):
        self.default_num_lines = default_num_lines
        self.latin_chars = constants.LATIN_CHARS
        self.russian_chars = constants.RUSSIAN_CHARS

    def date(self, years_back: int = constants.YEARS_BACK) -> str:
        """Generates a random date for the specified number of years """
        end_date = datetime.now()
        start_date = end_date - relativedelta(years=years_back)

        total_seconds = int((end_date - start_date).total_seconds())
        random_seconds = random.randint(0, total_seconds)
        random_date = start_date + timedelta(seconds=random_seconds)

        return random_date.strftime("%d.%m.%Y")

    def latin_string(self, length: int = constants.LATIN_LENGTH) -> str:
        """Generates a random string of Latin characters"""
        return ''.join(random.choices(self.latin_chars, k=length))

    def russian_string(self, length: int = constants.RUSSIAN_LENGTH) -> str:
        """Generates a random string of Russian characters"""
        return ''.join(random.choices(self.russian_chars, k=length))

    def even_integer(self,
                     min_val: int = constants.MIN_INT,
                     max_val: int = constants.MAX_INT) -> int:
        """Generates a random even integer within the specified range"""
        even_min = min_val if min_val % 2 == 0 else min_val + 1
        even_max = max_val if max_val % 2 == 0 else max_val - 1

        if even_min > even_max:
            raise ValueError("Unable to generate an even number in the given range")

        return random.randrange(even_min, even_max + 1, 2)

    def float_number(self,
                     min_val: float = constants.MIN_FLOAT,
                     max_val: float = constants.MAX_FLOAT,
                     decimals: int = constants.FLOAT_DECIMALS) -> float:
        """Generates a random floating point number"""
        return round(random.uniform(min_val, max_val), decimals)

    def generate_line(self,
                      sep=constants.DELIMITER) -> str:
        """Generates one line of data"""
        date = self.date()
        latin = self.latin_string()
        russian = self.russian_string()
        even_int = self.even_integer()
        float_num = self.float_number()
        result = sep.join([date, latin, russian, f"{even_int}", f"{float_num:.8f}"])
        return f"{result}\n"

    def file(self,
             filename: str,
             num_lines: int = None,
             show_progress: bool = True) -> None:
        """Generates a file with a specified number of lines"""
        if num_lines is None:
            num_lines = self.default_num_lines

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.',
                    exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(num_lines):
                if show_progress and i % 50000 == 0 and i > 0:
                    logger.info(f"Generation {filename}: {i}/{num_lines} lines")

                line = self.generate_line()
                f.write(line)

        if show_progress:
            logger.info(f"File {filename} successfully created with {num_lines} number of lines")

    def multiple_files(self,
                       filenames: list,
                       num_lines: Union[int, list] = None) -> None:
        """Generates multiple files"""
        if isinstance(num_lines, int):
            num_lines = [num_lines] * len(filenames)
        elif num_lines is None:
            num_lines = [self.default_num_lines] * len(filenames)

        for filename, lines in zip(filenames, num_lines):
            self.file(filename, lines)


def main():
    path = constants.OUTPUT_DIR
    gen = Generator()

    # test_line = gen.generate_line()
    # logger.info(f"String example: {test_line.strip()}")
    # gen.file(path + "test_data.csv", num_lines=100000)

    for i in range(100):
        gen.file(path + f"test_{i}.csv", num_lines=100000)


if __name__ == "__main__":
    main()
