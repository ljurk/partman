#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER partman with encrypted password 'docker';
    CREATE DATABASE partman;
    GRANT ALL PRIVILEGES ON DATABASE partman TO partman;
    \connect partman
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO partman;
EOSQL


psql -v ON_ERROR_STOP=1 --username "partman" --dbname "partman" <<-EOSQL
    CREATE TABLE parts (id SERIAL PRIMARY KEY, categoryId integer,name varchar, description varchar);
    CREATE TABLE categories (id SERIAL PRIMARY KEY, name varchar);
    CREATE TABLE suppliers(id SERIAL PRIMARY KEY, name varchar);
    CREATE TABLE partIdsFromSuppliers(partId integer,supplierId integer, supplierPartId integer);
    CREATE TABLE amounts(partId integer PRIMARY KEY, amount integer);

    INSERT INTO parts(categoryId,name) VALUES(1,'10k');
    INSERT INTO categories(name)VALUES('resistor');
    INSERT INTO categories(name)VALUES('diode');
    INSERT INTO categories(name)VALUES('transistor');
    INSERT INTO categories(name)VALUES('ic');
    INSERT INTO categories(name)VALUES('led');
    INSERT INTO categories(name)VALUES('jack');
EOSQL
