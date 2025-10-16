import sqlite3
import statistics

from tqdm import tqdm

from base_logger import logger


def calculate_statistics(db_path):
    """
    Calculates statistics for database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM imported_data")
        total_rows = cursor.fetchone()[0]

        if total_rows == 0:
            logger.info("Database is empty")
            return

        logger.info(f"The total number of rows in database: {total_rows:,}")

        # Сумма всех целых чисел
        cursor.execute("SELECT SUM(even_integer) FROM imported_data")
        total_sum = cursor.fetchone()[0]
        logger.info(f"Summ of all even integers: {total_sum:,}")

        cursor.execute("SELECT float_number FROM imported_data")
        float_numbers = [row[0] for row in tqdm(cursor, total=total_rows, desc="Loading data")]

        median_value = statistics.median(float_numbers)
        logger.info(f"Median of all float numbers: {median_value:.8f}")

    except Exception as e:
        logger.info(f"Calculating error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    calculate_statistics()
