CREATE TABLE IF NOT EXISTS imported_data (
    id SERIAL PRIMARY KEY,
    date_column DATE,
    latin_string VARCHAR(100),
    russian_string VARCHAR(100),
    even_integer BIGINT,
    float_number DECIMAL(12,8),
    filename VARCHAR,
    imported_at TIMESTAMP -- Default current timestamp
);


-- same, but with select
select
    sum(even_integer) as total_sum
    , percentile_cont(0.5) within group (order by float_number) as median_value
from imported_data;
