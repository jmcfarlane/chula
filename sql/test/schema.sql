DROP DATABASE chulatest;

CREATE DATABASE chulatest WITH
    OWNER = postgres
    TEMPLATE = template0
    ENCODING = 'UTF-8';

CREATE USER chula;

\c chulatest

-- Test table
CREATE TABLE cars (
    uid serial NOT NULL,
    make character varying,
    model character varying
);

GRANT ALL ON cars TO chula;
GRANT ALL ON cars_uid_seq TO chula;
