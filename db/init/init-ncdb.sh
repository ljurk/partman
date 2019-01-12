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
    CREATE TABLE parts (id integer PRIMARY KEY, categoryId integer,name varchar, friendlyName varchar);
    CREATE TABLE categories (id integer PRIMARY KEY, name varchar);
    CREATE TABLE categories (id integer PRIMARY KEY, name varchar);

    INSERT INTO parts(id,categoryId,name)VALUES(1,2,'test');
EOSQL
