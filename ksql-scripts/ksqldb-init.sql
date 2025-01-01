CREATE STREAM IF NOT EXISTS persons (
    name STRING,
    gender STRING,
    age INT
) 
WITH (
    KAFKA_TOPIC='person',
    VALUE_FORMAT='JSON',
    PARTITIONS=1
);

CREATE TABLE person_stats AS
SELECT 
    gender,
    COUNT(*) AS num_persons,
    ROUND(AVG(age)) AS average_age
FROM persons
GROUP BY gender

EMIT CHANGES;