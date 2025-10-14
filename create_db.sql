CREATE TABLE IF NOT EXISTS generated_data (
    id SERIAL PRIMARY KEY,
    date_column DATE,
    latin_string VARCHAR(100),
    russian_string VARCHAR(100),
    even_integer BIGINT,
    float_number DECIMAL(12,8)
    -- imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


/* Процедура иморта файлов */
CREATE OR REPLACE FUNCTION import_from_file(
    file_path TEXT,
    delimiter CHAR DEFAULT '||'
)
RETURNS VOID AS $$
DECLARE
    total_rows INTEGER;
    processed_rows INTEGER := 0;
    current_row RECORD;
    file_handle REFCURSOR;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    -- Открываем файл
    OPEN file_handle FOR EXECUTE
        'COPY (SELECT row_number() over() as row_num, * FROM pg_read_file(''' || file_path || ''') AS line) TO STDOUT';

    -- Получаем общее количество строк (примерно)
    EXECUTE 'SELECT COUNT(*) FROM pg_read_file(''' || file_path || ''') AS line'
    INTO total_rows;

    start_time := CURRENT_TIMESTAMP;
    RAISE NOTICE 'Начало импорта. Всего строк: %', total_rows;

    -- Основной цикл обработки
    LOOP
        FETCH file_handle INTO current_row;
        EXIT WHEN NOT FOUND;

        -- Парсинг строки (зависит от формата файла)
        -- Пример для CSV:
        INSERT INTO imported_data (date_column, latin_string, russian_string, even_integer, float_number)
        VALUES (
            split_part(current_row.line, delimiter, 1)::DATE,
            split_part(current_row.line, delimiter, 2),
            split_part(current_row.line, delimiter, 3),
            split_part(current_row.line, delimiter, 4)::INTEGER,
            split_part(current_row.line, delimiter, 5)::DECIMAL
        );

        processed_rows := processed_rows + 1;

        -- Вывод прогресса каждые 1000 строк или 1%
        IF processed_rows % 1000 = 0 OR processed_rows % (total_rows / 100) = 0 THEN
            RAISE NOTICE 'Обработано: % из % строк (%%)',
                processed_rows,
                total_rows,
                ROUND((processed_rows::DECIMAL / total_rows * 100)::NUMERIC, 2);
        END IF;
    END LOOP;

    CLOSE file_handle;

    end_time := CURRENT_TIMESTAMP;
    RAISE NOTICE 'Импорт завершен. Обработано % строк за %',
        processed_rows,
        end_time - start_time;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Ошибка при импорте: %', SQLERRM;
        IF file_handle IS NOT NULL THEN
            CLOSE file_handle;
        END IF;
END;
$$ LANGUAGE plpgsql;


/* сумму всех целых чисел и медиану всех дробных чисел */
CREATE OR REPLACE FUNCTION calculate_statistics()
RETURNS TABLE(total_sum BIGINT, median_value DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT
        SUM(even_integer) as total_sum,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY float_number) as median_value
    FROM generated_data;
END;
$$ LANGUAGE plpgsql;
