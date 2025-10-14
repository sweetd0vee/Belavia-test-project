import os


def simple_merge(input_folder, output_file, filter_string=None):
    """
    Простая функция объединения файлов
    """
    if not os.path.exists(input_folder):
        print(f"Папка '{input_folder}' не найдена!")
        return

    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    total_removed = 0
    total_lines = 0

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in files:
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as infile:
                for line in infile:
                    total_lines += 1
                    if filter_string and filter_string in line:
                        total_removed += 1
                        continue
                    outfile.write(line)

    print(f"Объединение завершено!")
    print(f"Файлов обработано: {len(files)}")
    print(f"Всего строк: {total_lines}")
    print(f"Удалено строк: {total_removed}")
    print(f"Сохранено строк: {total_lines - total_removed}")

# Пример использования:
# simple_merge("generated_files", "result.txt", "abc")