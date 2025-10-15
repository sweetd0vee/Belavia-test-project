import sqlite3
import os
import time


def simple_import_with_progress(folder_path='generated_files', db_path='data.db'):
    """
    Упрощенная версия импорта с прогресс-баром на базовых средствах
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS imported_data (
        id SERIAL PRIMARY KEY,
        random_date DATE,
        latin_string VARCHAR(100),
        russian_string VARCHAR(100),
        even_integer BIGINT,
        float_number DECIMAL(12,8),
        file_name TEXT,
        imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    total_files = len(files)
    total_imported = 0

    print(f"Начало импорта {total_files} файлов...")

    for file_index, filename in enumerate(files, 1):
        file_path = os.path.join(folder_path, filename)
        file_imported = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            total_lines = len(lines)

            print(f"\nФайл {file_index}/{total_files}: {filename}")
            print(f"Строк в файле: {total_lines}")

            for line_index, line in enumerate(lines, 1):
                try:
                    parts = line.strip().split(' || ')
                    if len(parts) == 5:
                        # Конвертация даты
                        date_parts = parts[0].split('.')
                        sql_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"

                        cursor.execute("""
                            INSERT INTO imported_data 
                            (random_date, latin_string, russian_string, even_integer, float_number, file_name)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (sql_date, parts[1], parts[2], int(parts[3]), float(parts[4]), filename))

                        file_imported += 1

                        # Вывод прогресса каждые 1000 строк
                        if line_index % 1000 == 0:
                            progress = (line_index / total_lines) * 100
                            remaining = total_lines - line_index
                            print(f"  Прогресс: {progress:.1f}% ({line_index}/{total_lines}), осталось: {remaining}")

                except Exception as e:
                    print(f"Ошибка в строке {line_index}: {e}")
                    continue

            # Коммит после каждого файла
            conn.commit()

        total_imported += file_imported
        print(f"Импортировано из файла: {file_imported} строк")
        print(f"Всего импортировано: {total_imported} строк")

        # Прогресс по файлам
        file_progress = (file_index / total_files) * 100
        print(f"Общий прогресс: {file_progress:.1f}%")
        print("-" * 50)

    conn.close()
    print(f"\nИмпорт завершен! Всего строк в базе: {total_imported}")


# Запуск
if __name__ == "__main__":
    simple_import_with_progress()