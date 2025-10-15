CREATE TABLE IF NOT EXISTS generated_data (
    id SERIAL PRIMARY KEY,
    date_column DATE,
    latin_string VARCHAR(100),
    russian_string VARCHAR(100),
    even_integer BIGINT,
    float_number DECIMAL(12,8),
    imported_at TIMESTAMP --DEFAULT CURRENT_TIMESTAMP
);


-- Import files procedure
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
    -- Open file
    OPEN file_handle FOR EXECUTE
        'COPY (SELECT row_number() over() as row_num, * FROM pg_read_file(''' || file_path || ''') AS line) TO STDOUT';

    -- Caculates total number of rows
    EXECUTE 'SELECT COUNT(*) FROM pg_read_file(''' || file_path || ''') AS line'
    INTO total_rows;

    start_time := CURRENT_TIMESTAMP;
    RAISE NOTICE 'Import started. Total number of lines: %', total_rows;

    -- Main loop
    LOOP
        FETCH file_handle INTO current_row;
        EXIT WHEN NOT FOUND;

        -- String parsing
        INSERT INTO generated_data (date_column, latin_string, russian_string, even_integer, float_number)
        VALUES (
            split_part(current_row.line, delimiter, 1)::DATE,
            split_part(current_row.line, delimiter, 2),
            split_part(current_row.line, delimiter, 3),
            split_part(current_row.line, delimiter, 4)::INTEGER,
            split_part(current_row.line, delimiter, 5)::DECIMAL
        );

        processed_rows := processed_rows + 1;

        -- Logging of each 5000 strings
        IF processed_rows % 5000 = 0 OR processed_rows % (total_rows / 100) = 0 THEN
            RAISE NOTICE 'Proccessed: % of % lines (%)',
                processed_rows,
                total_rows,
                ROUND((processed_rows::DECIMAL / total_rows * 100)::NUMERIC, 2);
        END IF;
    END LOOP;

    CLOSE file_handle;

    end_time := CURRENT_TIMESTAMP;
    RAISE NOTICE 'Import is finished. Proccessed % strings in %',
        processed_rows,
        end_time - start_time;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Import error: %', SQLERRM;
        IF file_handle IS NOT NULL THEN
            CLOSE file_handle;
        END IF;
END;
$$ LANGUAGE plpgsql;


-- Call function
-- SELECT import_from_file('/Users/sweetd0ve/Work/git-sweetd0vee/Belavia-test-project/generated_files/test_0.csv', '||');


-- calculates summ of all integers and median of all float numbers
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


-- same, but with select
select
    sum(even_integer) as total_sum
    , percentile_cont(0.5) within group (order by float_number) as median_value
from generated_data;
