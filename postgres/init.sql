/*
    This script is used to initialize the local PostgreSQL database.
*/
CREATE USER grafanareader WITH PASSWORD 'password';

CREATE TABLE events(
    id varchar(36),
    ts timestamp,
    email varchar(50),
    country varchar(56),
    ip varchar(39),
    uri text,
    action varchar(5),
    tags text,

    PRIMARY KEY(id)
);

GRANT SELECT ON events TO grafanareader;
