import sqlite3
import os
import time
from base_logger import logger
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.models import ImportedData


# Alternative approach using SQLAlchemy
def import_file_sqlalchemy(filepath, db: Session = get_db()):
    """
    Import data from file to database using SQLAlchemy
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            total_lines = len(lines)

            logger.info(f"Строк в файле {filepath}: {total_lines}")
            imported_count = 0
            for line_index, line in enumerate(lines, 1):
                try:
                    parts = line.strip().split('||')
                    if len(parts) == 5:
                        # Convert date and prepare data
                        date_parts = parts[0].split('.')
                        sql_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}" if len(date_parts) == 3 else None

                        row = ImportedData(
                            random_date=sql_date,
                            latin_string=parts[1],
                            russian_string=parts[2],
                            even_integer=parts[3],
                            float_number=parts[4],
                            file_name=filepath
                        )
                        db.add(row)
                        db.commit()
                        imported_count += 1

                        if line_index % 1000 == 0:
                            progress = (line_index / total_lines) * 100
                            remaining = total_lines - line_index
                            logger.info(
                                f"  Прогресс: {progress:.1f}% ({line_index}/{total_lines}), осталось: {remaining}")

                except Exception as e:
                    logger.error(f"Ошибка в строке {line_index}: {e}")
                    continue

        logger.info(f"\nImport completed! Imported {imported_count} rows from {total_lines} total lines")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during import: {e}")
        raise


# Запуск
if __name__ == "__main__":
    file_path = '/Users/sweetd0ve/Work/git-sweetd0vee/Belavia-test-project/generated_files/test_0.csv'
    import_file_sqlalchemy(file_path)
