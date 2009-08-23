DROP DATABASE chula_test;

CREATE DATABASE chula_test WITH
    OWNER = postgres
    TEMPLATE = template0
    ENCODING = 'UTF-8';

CREATE USER chula;
ALTER USER chula WITH PASSWORD 'chula';


\c chula_test

-- Test table
CREATE TABLE cars (
    uid serial NOT NULL,
    make character varying,
    model character varying
);

GRANT ALL ON cars TO chula;
GRANT ALL ON cars_uid_seq TO chula;

INSERT INTO cars (make, model) VALUES('Honda', 'Civic');
