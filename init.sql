CREATE DATABASE handball_app WITH ENCODING 'UTF8';
CREATE USER mitaka ENCRYPTED PASSWORD 'mitaka1' NOSUPERUSER NOCREATEDB NOCREATEROLE;
-- ALTER USER mitaka WITH CREATEDB;
GRANT ALL PRIVILEGES ON mydatabase TO mitaka;
