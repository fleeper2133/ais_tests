#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    DROP DATABASE IF EXISTS ais_tests_db;
    DROP DATABASE IF EXISTS test_ais_tests_db;
    DROP USER IF EXISTS ais_tests_user;
    DROP USER IF EXISTS test_ais_tests_db;
EOSQL
