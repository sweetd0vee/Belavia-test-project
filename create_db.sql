CREATE TABLE IF NOT EXISTS generated_data (
    id SERIAL PRIMARY KEY,
    date_column DATE,
    latin_string VARCHAR(100),
    russian_string VARCHAR(100),
    even_integer BIGINT,
    float_number DECIMAL(12,8)
);

