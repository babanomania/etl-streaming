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
