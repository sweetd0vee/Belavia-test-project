import sqlite3
import statistics

import psycopg2
from tqdm import tqdm


def calculate_statistics_sqlite(db_path='data.db'):
    """
    Расчет статистики для SQLite базы данных
    """
    print("Подключение к SQLite базе данных...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Проверяем наличие данных
        cursor.execute("SELECT COUNT(*) FROM imported_data")
        total_rows = cursor.fetchone()[0]

        if total_rows == 0:
            print("В базе данных нет данных для анализа")
            return

        print(f"Всего строк в базе: {total_rows:,}")
        print("Выполняем расчеты...")

        # Сумма всех целых чисел
        print("\n1. Расчет суммы целых чисел...")
        cursor.execute("SELECT SUM(even_integer) FROM imported_data")
        total_sum = cursor.fetchone()[0]
        print(f"Сумма всех целых чисел: {total_sum:,}")

        # Медиана дробных чисел (метод 1 - через выборку всех данных)
        print("\n2. Расчет медианы дробных чисел...")
        cursor.execute("SELECT float_number FROM imported_data")
        float_numbers = [row[0] for row in tqdm(cursor, total=total_rows, desc="Загрузка данных")]

        median_value = statistics.median(float_numbers)
        print(f"Медиана дробных чисел: {median_value:.8f}")

    except Exception as e:
        print(f"Ошибка при расчете статистики: {e}")
    finally:
        conn.close()


# Пример использования
if __name__ == "__main__":
    print("СКРИПТ РАСЧЕТА СТАТИСТИКИ")
    print("=" * 50)

    # Для SQLite
    calculate_with_sql_only('data.db')

    # Альтернативные методы (раскомментировать при необходимости)

    # print("\n" + "="*50)
    # print("ПОЛНАЯ СТАТИСТИКА (SQLite)")
    # print("="*50)
    # calculate_statistics_sqlite('data.db')

    # print("\n" + "="*50)
    # print("ЭФФЕКТИВНЫЙ РАСЧЕТ")
    # print("="*50)
    # calculate_statistics_memory_efficient('data.db')

    # Для PostgreSQL (раскомментировать и настроить при необходимости)
    # db_config = {
    #     'host': 'localhost',
    #     'database': 'test_db',
    #     'user': 'postgres',
    #     'password': 'password',
    #     'port': '5432'
    # }
    # calculate_statistics_postgresql(db_config)
