#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE ais_tests_db;
    CREATE USER ais_tests_user WITH PASSWORD 'password';
    ALTER ROLE ais_tests_user SET client_encoding TO 'utf8';
    ALTER ROLE ais_tests_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ais_tests_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE ais_tests_db TO ais_tests_user;
    ALTER USER ais_tests_user CREATEDB;
EOSQL
