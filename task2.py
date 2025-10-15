import os
from base_logger import logger


def files_merge(input_folder, output_file, filter_string=None):
    """
    Простая функция объединения файлов
    """
    if not os.path.exists(input_folder):
        logger.info(f"Папка '{input_folder}' не найдена!")
        return

    files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    total_lines = 0
    total_removed = 0

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for f in files:
            filepath = os.path.join(input_folder, f)
            with open(filepath, 'r', encoding='utf-8') as infile:
                for line in infile:
                    total_lines += 1
                    if filter_string and filter_string in line:
                        total_removed += 1
                        continue
                    outfile.write(line)

    logger.info(f"Файлы объединены!")
    logger.info(f"Оработано файлов: {len(files)}")
    logger.info(f"Всего строк: {total_lines}")
    logger.info(f"Удалено строк: {total_removed}")
    logger.info(f"Сохранено строк: {total_lines - total_removed}")


def main():
    # Пример использования:
    files_merge("generated_files", "result.csv", "abc")


if __name__ == "__main__":
    main()
