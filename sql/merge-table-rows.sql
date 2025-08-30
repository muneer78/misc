CREATE TABLE leads(
    lead_id serial PRIMARY key,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    active bool NOT NULL DEFAULT TRUE
);
CREATE TABLE customers(
    customer_id serial PRIMARY key,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    active bool NOT NULL DEFAULT TRUE
);